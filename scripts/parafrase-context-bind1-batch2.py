#!/usr/bin/env python3
"""A14: bind I biskoper, privilegier og bystyre."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, dict] = {
    "bind1-de-aeldstebyprivilegiene-s229": {
        "title": "De eldste byprivilegier",
        "year_display": "middelalder",
        "place_ids": ["gammeltorvet", "stortorvet"],
        "summary": (
            "Kongelige brev ga Oslo rett til selvstyre, handel og skatt på torvet. "
            "Privilegiene la grunnlaget for byens magistrat og borgeres rettigheter."
        ),
    },
    "bind1-administration-og-embedsmaendi-senmiddelalderen-s239": {
        "title": "Embetsmenn i senmiddelalder",
        "year_display": "1300-1500",
        "place_ids": ["gamle-raadhus-torvet", "domkirken-oslo"],
        "summary": (
            "Fogeder, fehirder og borgermestre styret skatt, rettsvesen og forsvar fra Akershus og rådhuset. "
            "Oslo var administrasjonssenter der kongemakt og kirke møtte hverandre."
        ),
    },
    "bind1-biskopsalomonstid-1322-51-s253": {
        "title": "Biskop Salomon og Akershus",
        "year_display": "1322-1351",
        "place_ids": ["akershus", "bispegarden"],
        "summary": (
            "Reform av kongens finanser knyttet fehird på Akershus tett til politisk makt. "
            "Borgensherrer som Torgils Smidsson styrte både festning og skatteoppkreveri i byen."
        ),
    },
    "bind1-bispenesigfrid-hallvard-og-jon-1352-85-s268": {
        "title": "Biskoper i unionsårene",
        "year_display": "1352-1385",
        "place_ids": ["domkirken-oslo", "bispegarden"],
        "summary": (
            "Biskop Sigfrid, Hallvard og Jon ledet kirken i Oslo da union og pest preget Østlandet. "
            "Domkirken og bispegården var sentre for tro, skrift og byens vitnesbyrd om middelalderen."
        ),
    },
    "bind1-biskop-eystein-1385-1407-s275": {
        "title": "Biskop Eystein",
        "year_display": "1385-1407",
        "place_ids": ["domkirken-oslo", "gamle-aker-kirke"],
        "summary": (
            "Biskop Eystein arbeidet for kirkegårder, hospital og sosial omsorg i byen. "
            "Han fikk plass i Oslo historie som en fremtredende kirkelig bygger og administrator."
        ),
    },
    "bind1-privilegiene-av-7-januar1508-s381": {
        "title": "Privilegier 7. januar 1508",
        "year_display": "1508",
        "place_ids": ["gammeltorvet", "kontraskjerp"],
        "summary": (
            "Nye privilegier i 1508 styrket byens handel og selvstyre på overgangen til reformasjonstiden. "
            "Kjøpmenn fikk tydeligere rammer for toll, torghandel og borgernes plikter."
        ),
    },
    "bind1-rostockernei-osloi-det15-aarh-s303": {
        "title": "Rostock-kjøpmenn i Oslo",
        "year_display": "1400-tallet",
        "place_ids": ["kontraskjerp", "gammeltorvet"],
        "summary": (
            "Tyske kjøpmenn fra Rostock var dypt inne i handelen ved Oslo. "
            "Konkurransen med hansaforbundet og lokale borgere preget kaianlegg og torv i middelalderbyen."
        ),
    },
}


def main() -> None:
    doc = json.loads(CTX.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in doc.get("entries", [])}
    n = 0
    for eid, patch in PATCHES.items():
        if eid in by_id:
            by_id[eid].update(patch)
            n += 1
    CTX.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"parafrase bind I batch2: {n} oppdatert")


if __name__ == "__main__":
    main()