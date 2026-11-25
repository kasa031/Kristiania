#!/usr/bin/env python3
"""Juster tags og episode-metadata for tydeligere kategorier (kjør etter innholdsendringer)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ADD_TAGS = {
    "sagene-loken": ["industri"],
    "myrens-verk": ["industri"],
    "hollaenderbrua": ["industri"],
    "bentsebru": ["industri"],
    "honse-lovisas-hus": ["arbeid"],
    "akerselva-utløp": ["industri"],
    "oslo-sentralstasjon": ["transport"],
    "grunerlokka-folketeater": ["arbeid"],
    "universitetsplassen": ["utdanning"],
    "domkirken-oslo": [],
    "stortinget": [],
    "karl-johan-jubileet": [],
}

EVENT_ADD = {
    "sag-og-molle": ["industri"],
    "manufaktur-myrens": ["industri"],
    "christiania-vokser-elva": ["industri"],
    "arbeiderkultur-akerselva": ["arbeid", "industri"],
    "honse-lovisa-fortelling": ["arbeid", "kultur"],
    "jernbanen-1854": ["transport"],
    "universitetet-1827": ["utdanning"],
    "byutvidelse-1878": ["bygrunn"],
    "arbeiderkultur-1890": ["arbeid", "kultur"],
    "jubileum-1924": ["kultur"],
}

REMOVE_TAGS = {
    "sagene-loken": {"havn"},
    "myrens-verk": {"havn"},
    "manufaktur-myrens": {"havn"},
    "jernbanen-1854": {"havn"},
    "oslo-sentralstasjon": set(),
}

EPISODE_ERA = {
    "middelalder-oslo": "middelalder",
    "1624-ny-by": "kristiania",
    "kvadraturen-1600": "kvadratur",
    "akerselva-tidlig": "elva",
    "1814-hovedstaden": "hovedstad",
    "mot-1924": "storby",
}


def dedupe(tags: list[str]) -> list[str]:
    out: list[str] = []
    for t in tags:
        if t not in out:
            out.append(t)
    return out


def apply_tags(items: list[dict], add_map: dict, remove_map: dict | None = None) -> int:
    n = 0
    remove_map = remove_map or {}
    for item in items:
        iid = item["id"]
        tags = list(item.get("tags") or [])
        changed = False
        for t in remove_map.get(iid, set()):
            if t in tags:
                tags.remove(t)
                changed = True
        for t in add_map.get(iid, []):
            if t not in tags:
                tags.append(t)
                changed = True
        if changed:
            item["tags"] = dedupe(tags)
            n += 1
    return n


def main() -> None:
    places_path = ROOT / "data" / "places.json"
    events_path = ROOT / "data" / "events.json"
    episodes_path = ROOT / "data" / "episodes.json"

    places_doc = json.loads(places_path.read_text(encoding="utf-8"))
    events_doc = json.loads(events_path.read_text(encoding="utf-8"))
    episodes_doc = json.loads(episodes_path.read_text(encoding="utf-8"))

    pn = apply_tags(places_doc["places"], ADD_TAGS)
    en = apply_tags(events_doc["events"], EVENT_ADD, REMOVE_TAGS)

    for ep in episodes_doc["episodes"]:
        era = EPISODE_ERA.get(ep["id"])
        if era:
            ep["era_id"] = era

    episodes_doc["episodes"].sort(
        key=lambda e: (
            list(EPISODE_ERA.keys()).index(e["id"])
            if e["id"] in EPISODE_ERA
            else 99,
            e.get("title", ""),
        )
    )

    places_path.write_text(json.dumps(places_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    events_path.write_text(json.dumps(events_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    episodes_path.write_text(json.dumps(episodes_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated places tags: {pn}, events tags: {en}, episodes era_id: {len(EPISODE_ERA)}")


if __name__ == "__main__":
    main()