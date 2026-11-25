#!/usr/bin/env python3
"""Enkel sjekk av norsk UI-tekst: apostrof og typiske skrivefeil."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UI_FILES = [
    ROOT / "data" / "site-config.json",
    ROOT / "index.html",
    ROOT / "manifest.webmanifest",
]

# Engelsk apostrof-genitiv i norsk UI (Oslo's, Bull's)
APOSTROPHE_GENITIVE = re.compile(r"\b[A-ZÆØÅa-zæøå]+'s\b")

# Vanlig feilstavelse
TYPO = {
    "jubeleum": "jubileum",
    "interaktivt historisk": "fjern «interaktivt» i header hvis bevisst",
}


def scan_text(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    for m in APOSTROPHE_GENITIVE.finditer(text):
        issues.append(f"{path.name}: engelsk apostrof-genitiv: {m.group(0)}")
    lower = text.lower()
    for bad, hint in TYPO.items():
        if bad in lower and "interaktivt" in bad:
            continue
        if bad in lower:
            issues.append(f"{path.name}: mulig skrivefeil «{bad}» ({hint})")
    return issues


INTERNAL_HREF = re.compile(
    r"href=[\"'](?:\.\./)?(?:theme-preview|content/fremgang|content/prosjekt|prosjektplan|prosjektrapport)",
    re.IGNORECASE,
)


def main() -> int:
    issues: list[str] = []
    index = ROOT / "index.html"
    if index.is_file():
        raw = index.read_text(encoding="utf-8")
        if INTERNAL_HREF.search(raw):
            issues.append(f"{index.name}: intern lenke i app-UI (fjern eller flytt ut av index)")
    for path in UI_FILES:
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        issues.extend(scan_text(path, raw))
        if path.suffix == ".json":
            try:
                doc = json.loads(raw)
                for key in (
                    "app_footer",
                    "home_headline",
                    "home_lead",
                    "masthead_dek",
                    "masthead_rubric",
                    "routes_panel_lead",
                ):
                    if isinstance(doc.get(key), str):
                        issues.extend(scan_text(path, doc[key]))
            except json.JSONDecodeError:
                issues.append(f"{path.name}: ugyldig JSON")
    if issues:
        for line in issues:
            print(line)
        return 1
    print("lint-ui-tekst OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())