#!/usr/bin/env python3
"""Rydd OCR-ledd i context.json: mellomrom, norsk tegn, korte ledband."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"
MANUAL_PREFIXES = (
    "bind1-geologi",
    "bind1-sosial",
    "bind1-byanlaeg",
    "bind1-oslo-bispedom",
    "bind1-bispeborg",
    "bind1-handel",
    "bind1-nederlandsk",
    "bind1-reformationen",
    "bind1-ladestedene",
    "bind1-oslo-humanistene",
)


def ocr_spacing(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"(\d)\s*([a-zA-ZæøåÆØÅ])", r"\1 \2", text)
    text = re.sub(r"(?<=[a-zæøå])(?=[A-ZÆØÅ])", " ", text)
    text = re.sub(r"(?<=[.!?])\s*([A-ZÆØÅÆ])", r" \1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def looks_like_ocr(s: str) -> bool:
    if len(s) < 40:
        return False
    caps = sum(1 for c in s if c.isupper())
    if caps / max(len(s), 1) > 0.22:
        return True
    if re.search(r"[a-zæøå][A-ZÆØÅ]", s):
        return True
    if "  " in s and s.isupper():
        return True
    spaces = s.count(" ")
    if spaces < len(s) / 18:
        return True
    if re.search(r"\w{22,}", s):
        return True
    return False


def sentences_from_excerpt(note: str) -> str:
    if not note or not note.startswith("sources/"):
        return ""
    path = ROOT / note.replace("/", "\\") if "\\" in note else ROOT / note
    if not path.is_file():
        path = ROOT / note
    if not path.is_file():
        return ""
    body = path.read_text(encoding="utf-8", errors="replace")
    body = re.sub(r"^#.*?\n\n", "", body, count=1, flags=re.DOTALL)
    body = re.sub(r"- \*\*.*?\n", "", body)
    body = re.sub(r"### Bokside \d+\s*", "", body)
    body = ocr_spacing(body)
    for junk in ("INDHOLD", "KRISTIANIAS HISTORIE", "OSLOS HISTORIE"):
        body = body.replace(junk, " ")
    body = re.sub(r"\s+", " ", body).strip()
    parts = re.split(r"(?<=[.!?])\s+", body)
    good: list[str] = []
    for p in parts:
        p = p.strip()
        if len(p) < 35 or len(p) > 320:
            continue
        if re.match(r"^\d", p):
            continue
        if looks_like_ocr(p) and len(p) > 120:
            p = ocr_spacing(p)
        good.append(p)
        if len(good) >= 2:
            break
    return " ".join(good)


def humanize_title(title: str) -> str:
    t = re.sub(r"\s+", " ", title).strip()
    t = re.sub(r"([a-z])([A-ZÆØÅ])", r"\1 \2", t)
    t = re.sub(r"([a-zæøå])(og)([A-ZÆ])", r"\1 \2 \3", t, flags=re.I)
    t = re.sub(r"(?<=[a-z])og(?=[A-ZÆ])", " og ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_summary(entry: dict) -> str:
    title = humanize_title(entry.get("title") or "Kapittelet")
    b = entry.get("bind")
    pages = (entry.get("source_ref") or {}).get("pages", "")
    yr = entry.get("year_display") or ""
    if yr and not yr.startswith("bind"):
        return (
            f"{title} gir bakgrunn om Oslos utvikling i perioden {yr}. "
            f"Stoffet hører til byhistorien og kan leses i tidslinjen."
        )
    return (
        f"{title} tar for seg byen og samfunnet i sin tid. "
        f"Les mer i bakgrunnkortet i tidslinjen."
    )


def bind_label(b: int | None) -> bool:
    return b is not None


def main() -> None:
    doc = json.loads(CTX.read_text(encoding="utf-8"))
    n_ocr, n_title = 0, 0
    for e in doc.get("entries", []):
        eid = e.get("id", "")
        if e.get("title"):
            e["title"] = humanize_title(e["title"])
        if any(eid.startswith(p) for p in MANUAL_PREFIXES):
            continue
        sm = e.get("summary", "")
        if (
            not looks_like_ocr(sm)
            and len(sm) > 80
            and "bygger på kilden" not in sm
            and "I bind " not in sm
            and not sm.endswith("...")
        ):
            continue
        from_ex = sentences_from_excerpt(e.get("supplementary_note", ""))
        if from_ex and not looks_like_ocr(from_ex):
            e["summary"] = from_ex[:420].rstrip() + ("..." if len(from_ex) > 420 else "")
            n_ocr += 1
        else:
            e["summary"] = title_summary(e)
            n_title += 1
        if looks_like_ocr(e.get("summary", "")):
            e["summary"] = title_summary(e)
    CTX.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"context.json: {n_ocr} fra utdrag, {n_title} titel-led")


if __name__ == "__main__":
    main()