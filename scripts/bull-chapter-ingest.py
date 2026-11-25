#!/usr/bin/env python3
"""
TOC kapittel -> excerpts + context.json (utkast-parafrase fra første bokside).
Kjør bind for bind; full dekning spores i sources/innsamling/bull-toc-backlog.json.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOC_DIR = ROOT / "sources" / "toc"
EXCERPTS = ROOT / "sources" / "excerpts"
BACKLOG = ROOT / "sources" / "innsamling" / "bull-toc-backlog.json"
CONTEXT_PATH = ROOT / "data" / "context.json"
EXTRACT = ROOT / "scripts" / "extract-excerpt.py"

BIND_YEAR = {
    1: (900, 1624),
    2: (1624, 1740),
    3: (1740, 1814),
    4: (1814, 1877),
    5: (1878, 1924),
}

SKIP_TITLE = re.compile(
    r"navne|sakregister|person.*register|stedregister|illustrations|"
    r"rettelser|indhold|fra komiteen",
    re.I,
)


def slugify(title: str, bind: int) -> str:
    t = title.lower()
    t = t.replace("æ", "ae").replace("ø", "o").replace("å", "aa")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    t = re.sub(r"-+", "-", t)
    return f"bind{bind}-{t[:48].strip('-')}"


def parse_toc_file(path: Path, bind: int) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    chapters: list[dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("---"):
            continue
        if line.lower().startswith("side") or line.lower() == "indhold":
            continue
        line = re.sub(r"\s*\.\.\s*", " ", line)
        line = line.replace("—", "-").replace("–", "-").replace("'", "'")
        line = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", line)
        m = re.search(
            r"^(.+?)\s+(\d+)\s*-\s*(\d+|1G\d|[\d]+)(.*)$",
            line,
        )
        if not m:
            m2 = re.search(r"^(.+?)\s+(\d+)\s*$", line)
            if m2:
                title = re.sub(r"\s+", " ", m2.group(1)).strip()
                start = int(m2.group(2))
                chapters.append(
                    {"bind": bind, "title": title, "page_start": start, "page_end": start}
                )
            continue
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        start = int(m.group(2))
        end_raw = m.group(3).replace("G", "6")
        end_digits = re.sub(r"\D", "", end_raw) or str(start)
        end = int(end_digits[:4]) if end_digits else start
        if end < start:
            end = start
        chapters.append(
            {"bind": bind, "title": title, "page_start": start, "page_end": end}
        )
    return chapters


def load_json_items() -> tuple[set[str], set[tuple[int, str]]]:
    """context ids og (bind, pages) fra context + events."""
    covered_pages: set[tuple[int, str]] = set()
    context_ids: set[str] = set()
    if CONTEXT_PATH.is_file():
        for e in json.loads(CONTEXT_PATH.read_text(encoding="utf-8")).get("entries", []):
            context_ids.add(e["id"])
            ref = e.get("source_ref") or {}
            b = ref.get("bind")
            p = str(ref.get("pages") or "")
            if b and p:
                covered_pages.add((int(b), p))
    for name in ("events.json", "places.json"):
        p = ROOT / "data" / name
        if not p.is_file():
            continue
        key = "events" if name.startswith("events") else "places"
        for item in json.loads(p.read_text(encoding="utf-8")).get(key, []):
            ref = item.get("source_ref") or {}
            b = ref.get("bind")
            pgs = str(ref.get("pages") or "")
            if b and pgs and pgs != "supplement":
                covered_pages.add((int(b), pgs))
    return context_ids, covered_pages


def pages_key(start: int, end: int) -> str:
    if start == end:
        return str(start)
    return f"{start}-{end}"


def page_ranges_overlap(a_start: int, a_end: int, b_key: str) -> bool:
    if "-" in b_key:
        b_start, b_end = (int(x) for x in b_key.split("-", 1))
    else:
        b_start = b_end = int(re.sub(r"\D", "", b_key) or "0")
    return not (a_end < b_start or a_start > b_end)


def already_covered(bind: int, start: int, end: int, covered) -> bool:
    for b, pkey in covered:
        if b != bind:
            continue
        if page_ranges_overlap(start, end, pkey):
            return True
    return False


def infer_tags(title: str) -> list[str]:
    t = title.lower()
    tags: list[str] = []
    if any(x in t for x in ("geologi", "forhistor", "natur")):
        tags.extend(["geologi", "natur"])
    if any(x in t for x in ("klima", "pest")):
        tags.append("klima")
    if any(x in t for x in ("sosial", "arbeider", "befolkning")):
        tags.append("sosial")
    if any(x in t for x in ("handel", "havn", "brygg", "skib", "told")):
        tags.append("havn")
    if any(x in t for x in ("kirke", "biskop", "bisp", "kloster", "religi")):
        tags.append("kultur")
    if any(x in t for x in ("skole", "aandsliv", "humanist", "kultur", "statuer")):
        if "kultur" not in tags:
            tags.append("kultur")
        if "skole" in t or "aandsliv" in t:
            tags.append("utdanning")
    if any(x in t for x in ("bebygg", "reguler", "anlæg", "byutvid", "plan")):
        tags.append("bygrunn")
    if any(x in t for x in ("festning", "akershus", "beleir", "krig")):
        tags.append("festning")
    if any(x in t for x in ("styre", "administr", "kommune", "forfatning", "laug")):
        tags.append("kommune")
    if any(x in t for x in ("brann", "brand")):
        tags.append("brann")
    if any(x in t for x in ("industri", "manufaktur", "næring", "jernbane")):
        tags.append("industri")
    if not tags:
        tags = ["kultur"]
    out: list[str] = []
    for x in tags:
        if x not in out:
            out.append(x)
    return out[:4]


def infer_years(bind: int, start: int, end: int, title: str) -> tuple[int, int, str]:
    y0, y1 = BIND_YEAR[bind]
    if bind == 1 and "forhistor" in title.lower():
        return -8000, -3000, "før historisk tid"
    m = re.search(r"\((\d{3,4})\s*[-–]\s*(\d{3,4})\)", title)
    if m:
        return int(m.group(1)), int(m.group(2)), f"{m.group(1)}-{m.group(2)}"
    m2 = re.search(r"(\d{4})", title)
    if m2:
        y = int(m2.group(1))
        return y, y, str(y)
    return y0, y1, f"bind {bind}"


def extract_excerpt(bind: int, page_start: int, page_end: int, out: Path, slug: str) -> None:
    if out.is_file() and out.stat().st_size > 200:
        return
    end = min(page_end, page_start + 1)
    cmd = [
        sys.executable,
        str(EXTRACT),
        "--bind",
        str(bind),
        "--pages",
        f"{page_start}-{end}",
        "--out",
        str(out),
        "--json-id",
        slug,
    ]
    subprocess.run(cmd, check=False, cwd=ROOT)


def summary_from_excerpt(path: Path, title: str, bind: int) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    body = re.sub(r"^#.*?\n\n", "", text, count=1, flags=re.DOTALL)
    body = re.sub(r"- \*\*.*?\*\*.*\n", "", body)
    body = re.sub(r"### Bokside \d+\s*", "", body)
    body = re.sub(r"\s+", " ", body).strip()
    if len(body) < 100 or "INDHOLD" in body[:80]:
        return ""
    body = body.replace("Kristianias Historie", "").replace("KRISTIANIAS HISTORIE", "")
    body = re.sub(r"\d{1,3}\s*KRISTIANIAS HISTORIE.*", "", body)
    if len(body) < 80:
        return ""
    cut = body[:520]
    if len(body) > 520:
        cut = cut.rsplit(" ", 1)[0] + "..."
    cut = (
        cut.replace("aa", "å")
        .replace("Aa", "Å")
        .replace("oe", "ø")
        .replace("ae", "æ")
    )
    cut = re.sub(r"\bbaad\b", "båd", cut, flags=re.I)
    cut = re.sub(r"\s+", " ", cut).strip()
    if not cut.endswith((".", "!", "?")):
        cut += "."
    return cut


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", type=int, choices=range(1, 6), action="append", dest="binds")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--max-new", type=int, default=999)
    args = parser.parse_args()

    binds = list(range(1, 6)) if args.all else (args.binds or [1])
    context_ids, covered = load_json_items()
    entries = []
    if CONTEXT_PATH.is_file():
        entries = json.loads(CONTEXT_PATH.read_text(encoding="utf-8")).get("entries", [])

    backlog: dict = {"chapters": [], "updated": None}
    if BACKLOG.is_file():
        backlog = json.loads(BACKLOG.read_text(encoding="utf-8"))

    new_count = 0
    for bind in binds:
        toc_path = TOC_DIR / f"bind-{['I', 'II', 'III', 'IV', 'V'][bind - 1]}-kapitler.md"
        if not toc_path.is_file():
            print(f"Mangler TOC: {toc_path}")
            continue
        chapters = parse_toc_file(toc_path, bind)
        for ch in chapters:
            title = ch["title"]
            if SKIP_TITLE.search(title):
                ch["status"] = "skipped_meta"
                backlog["chapters"].append(ch)
                continue
            start, end = ch["page_start"], ch["page_end"]
            slug = slugify(title, bind) + f"-s{start}"
            if slug in context_ids:
                ch["status"] = "context_exists"
                backlog["chapters"].append(ch)
                continue
            if already_covered(bind, start, end, covered):
                ch["status"] = "covered_event_or_place"
                backlog["chapters"].append(ch)
                continue
            ex_name = f"bind-{['I', 'II', 'III', 'IV', 'V'][bind - 1]}-s{pages_key(start, end)}-{slug.split('-', 2)[-1][:24]}.md"
            ex_path = EXCERPTS / ex_name
            if args.write and new_count < args.max_new:
                extract_excerpt(bind, start, end, ex_path, slug)
                summary = summary_from_excerpt(ex_path, title, bind)
                if not summary:
                    extract_excerpt(bind, start + 1, min(end, start + 2), ex_path, slug)
                    summary = summary_from_excerpt(ex_path, title, bind)
                if not summary:
                    continue
                y_from, y_to, y_disp = infer_years(bind, start, end, title)
                entry = {
                    "id": slug,
                    "title": title[:120],
                    "year_from": y_from,
                    "year_to": y_to,
                    "year_display": y_disp,
                    "bind": bind,
                    "tags": infer_tags(title),
                    "place_ids": [],
                    "summary": summary,
                    "verified": False,
                    "source_ref": {
                        "bind": bind,
                        "pages": pages_key(start, end),
                        "note": f"Bind {bind}: {title} (TOC)",
                    },
                    "supplementary_note": f"sources/excerpts/{ex_name}",
                }
                entries.append(entry)
                context_ids.add(slug)
                covered.add((bind, pages_key(start, end)))
                ch["status"] = "added_context"
                new_count += 1
            else:
                ch["status"] = "pending"
            backlog["chapters"].append(ch)

    from datetime import datetime, timezone

    backlog["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    backlog["stats"] = {
        "total": len(backlog["chapters"]),
        "added_context": sum(1 for c in backlog["chapters"] if c.get("status") == "added_context"),
        "pending": sum(1 for c in backlog["chapters"] if c.get("status") == "pending"),
    }

    if args.write:
        BACKLOG.parent.mkdir(parents=True, exist_ok=True)
        BACKLOG.write_text(json.dumps(backlog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        CONTEXT_PATH.write_text(
            json.dumps({"entries": entries}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {new_count} nye context-rader -> {CONTEXT_PATH}")
        print(f"Backlog: {BACKLOG}")
    else:
        pending = sum(1 for c in backlog["chapters"] if c.get("status") == "pending")
        print(f"Tørrkjøring bind {binds}: ville lagt til ca. {pending} context (bruk --write)")


if __name__ == "__main__":
    main()