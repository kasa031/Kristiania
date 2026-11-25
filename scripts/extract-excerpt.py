#!/usr/bin/env python3
"""Hent kort utdrag fra literature/*.pdf (bok-sidetall ca. = PDF-side for disse bindene)."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "literature"

PDF_BY_BIND = {
    1: "Oslos_historie1.pdf",
    2: "Kristianias_historie._Bind_II._1624-1740.pdf",
    3: "Kristianias_historie._Bind_III._1740-1814.pdf",
    4: "Kristianias_historie._Bind_IV._1814-1877.pdf",
    5: "Kristianias_historie._Bind_V._1878-1924.pdf",
}


def clean(text: str, max_len: int = 1200) -> str:
    text = re.sub(r"\s+", " ", text.replace("\r", " ")).strip()
    if len(text) > max_len:
        text = text[: max_len - 3].rsplit(" ", 1)[0] + "..."
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", type=int, required=True, choices=range(1, 6))
    parser.add_argument("--pages", required=True, help="f.eks. 485-492 eller 485")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--json-id", default="", help="sted/hendelse-id for sporbarhet")
    args = parser.parse_args()

    pdf = LIT / PDF_BY_BIND[args.bind]
    if not pdf.is_file():
        raise SystemExit(f"Mangler PDF: {pdf}")

    if "-" in args.pages:
        start, end = (int(x) for x in args.pages.split("-", 1))
    else:
        start = end = int(args.pages)

    reader = PdfReader(str(pdf))
    chunks: list[str] = []
    for book_page in range(start, end + 1):
        idx = book_page - 1
        if idx < 0 or idx >= len(reader.pages):
            continue
        raw = reader.pages[idx].extract_text() or ""
        if raw.strip():
            chunks.append(f"### Bokside {book_page}\n\n{raw.strip()}\n")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# Bind {args.bind} s. {start}"
        + (f"-{end}" if end != start else "")
        + "\n\n"
    )
    if args.json_id:
        header += f"- **JSON:** `{args.json_id}`\n"
    header += "- **Merk:** Rå PDF-tekst - parafraser til nettsiden, ikke publiser langt sitat.\n\n"
    body = clean("\n\n".join(chunks), max_len=3500) if chunks else "(Ingen tekst på disse sidene.)"
    args.out.write_text(header + body + "\n", encoding="utf-8")
    print(f"Wrote {args.out} ({len(chunks)} sider)")


if __name__ == "__main__":
    main()