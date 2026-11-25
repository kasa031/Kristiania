"""Hent innholdsfortegnelse fra literature/*.pdf til sources/toc/bind-*-kapitler.md."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "literature"
OUT = ROOT / "sources" / "toc"

BINDS = [
    ("I", "Oslos_historie1.pdf", "Oslos historie fram til 1624", "Edvard Bull, 1922"),
    ("II", "Kristianias_historie._Bind_II._1624-1740.pdf", "1624-1740", "Edvard Bull"),
    ("III", "Kristianias_historie._Bind_III._1740-1814.pdf", "1740-1814", "Bull / Sønstevold"),
    ("IV", "Kristianias_historie._Bind_IV._1814-1877.pdf", "1814-1877", "Simon Christian Hammer"),
    ("V", "Kristianias_historie._Bind_V._1878-1924.pdf", "1878-1924", "Simon Christian Hammer"),
]


def find_indhold_start(reader: PdfReader) -> int | None:
    for i, page in enumerate(reader.pages[:50]):
        t = (page.extract_text() or "").upper()
        if "INDHOLD" in t or "INNHOLD" in t or "INNEHOLD" in t:
            return i
    return None


def is_toc_page(text: str) -> bool:
    if not text or len(text.strip()) < 40:
        return False
    upper = text.upper()
    if "INDHOLD" in upper or "INNHOLD" in upper:
        return True
    numbers = len(re.findall(r"\b\d{1,4}\b", text))
    lines = len([line for line in text.splitlines() if line.strip()])
    if lines < 5:
        return False
    return numbers >= 8 and len(text) < 8000


def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.replace("\r", "").splitlines() if line.strip()]
    return "\n".join(lines)


def main() -> None:
    for bind, pdf_name, period, author in BINDS:
        path = LIT / pdf_name
        if not path.is_file():
            print(f"MANGLER: {path}")
            continue
        reader = PdfReader(str(path))
        start = find_indhold_start(reader)
        if start is None:
            print(f"Bind {bind}: fant ikke INDHOLD")
            continue
        chunks: list[str] = []
        for j in range(start, min(start + 12, len(reader.pages))):
            raw = reader.pages[j].extract_text() or ""
            if j > start and not is_toc_page(raw):
                if len(raw.strip()) > 200 and len(re.findall(r"\b\d{1,4}\b", raw)) < 5:
                    break
            chunks.append(f"--- PDF side {j + 1} ---\n{clean_text(raw)}")
        body = "\n\n".join(chunks)
        fname = OUT / f"bind-{bind}-kapitler.md"
        header = (
            f"# Bind {bind} - {period} ({author})\n\n"
            f"**Status:** Utkast hentet fra `literature/{pdf_name}` (PDF-tekst).\n"
            "**Godkjenning:** Sjekk mot eget bind for endelig TOC.\n\n"
            "## Innholdsfortegnelse (autouttrekk)\n\n"
        )
        fname.write_text(header + body + "\n", encoding="utf-8")
        print(f"Bind {bind}: {len(chunks)} sider TOC -> {fname.name}")


if __name__ == "__main__":
    main()