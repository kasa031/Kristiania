#!/usr/bin/env python3
"""Les data/field-notes.json og skriv kort felt-rapport til content/FELT-RAPPORT.md."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "data" / "field-notes.json"
OUT = ROOT / "content" / "FELT-RAPPORT.md"


def main() -> None:
    data = json.loads(NOTES.read_text(encoding="utf-8"))
    episodes = {e["id"]: e for e in json.loads((ROOT / "data/episodes.json").read_text(encoding="utf-8"))["episodes"]}
    lines = [
        "# Feltgåtur - rapport (autogenerert)",
        "",
        "Kilde: `data/field-notes.json`. Kjør på nytt: `python scripts/apply-field-notes.py`.",
        "Brukes sammen med steg 4 i FREMGANG - ikke erstatter avkryssing i fremgang.html.",
        "",
    ]
    done = 0
    for w in data.get("walks", []):
        eid = w.get("episode_id", "")
        title = episodes.get(eid, {}).get("title", eid)
        lines.append(f"## {title}")
        if w.get("walked_date"):
            lines.append(f"- Dato: {w['walked_date']}")
        if w.get("ok") is True:
            done += 1
            lines.append("- Status: OK")
        elif w.get("ok") is False:
            lines.append("- Status: trenger justering")
        else:
            lines.append("- Status: ikke gått ennå")
        if w.get("reorder"):
            lines.append(f"- Rekkefølge: {w['reorder']}")
        if w.get("text_too_long_stops"):
            lines.append(f"- For lang tekst ved: {', '.join(w['text_too_long_stops'])}")
        if w.get("missing_places"):
            lines.append(f"- Mangler: {w['missing_places']}")
        if w.get("notes"):
            lines.append(f"- Notater: {w['notes']}")
        lines.append("")

    lines.insert(4, f"**Gått og markert OK:** {done} av {len(data.get('walks', []))} løyper.\n")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({done}/{len(data.get('walks', []))} OK)")


if __name__ == "__main__":
    main()