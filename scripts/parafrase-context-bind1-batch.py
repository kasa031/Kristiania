#!/usr/bin/env python3
"""A14: bind I mellomalder-kapitler med kartkobling."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, dict] = {
    "bind1-byensstyre-s107": {
        "title": "Byens styre og strid",
        "year_display": "1200-tallet",
        "place_ids": ["middelalderparken", "domkirken-gamlebyen", "akershus"],
        "summary": (
            "Vårblokkene og birkebeinerne kjempet om kongemakten i Oslo by. "
            "Slaget ved kirkegårdsledet og Martestokker bandt festning, kirker og gater i byens eldste politiske drama."
        ),
    },
    "bind1-haakonv-s-tid-s137": {
        "title": "Hanse og handel",
        "year_display": "1200-1300-tallet",
        "place_ids": ["gammeltorvet", "kontraskjerp"],
        "summary": (
            "Tyske hankjøpmenn fra Rostock og andre havner knyttet Oslo til kontinentets handelsnett. "
            "Privilegier og konkurransen mellom byborgere og utenlandske kjøpmenn preget torv og kaianlegg."
        ),
    },
    "bind1-syvaarskrigen-s423": {
        "title": "Festning under syvårskrigen",
        "year_display": "1560-årene",
        "place_ids": ["akershus", "domkirken-gamlebyen"],
        "summary": (
            "Syvårskrigen økte behovet for moderne forsvar på Akershus. "
            "Munketårnet og nye murer ble bygget med stein fra nedrevne kirker i det gamle Oslo."
        ),
    },
    "bind1-kampenfor-handelsmonopolet-s451": {
        "title": "Kampen om handelsmonopol",
        "year_display": "1500-tallet",
        "place_ids": ["gammeltorvet", "kontraskjerp"],
        "summary": (
            "Kjøpmenn og kronen stridde om kontroll over handel i byen. "
            "Monopol og privilegier regulerte hvem som fikk kjøpe og selge på torv og kai."
        ),
    },
    "bind1-byvedtaegteneav-1595-s465": {
        "title": "Byvedtekten 1595",
        "year_display": "1595",
        "place_ids": ["gammeltorvet", "stortorvet"],
        "summary": (
            "Byens ordensregler fra 1595 skulle holde orden på brannfare, renovasjon og offentlig oppførsel. "
            "Vedtektene viser hvordan magistrat og borgere styrte dagliglivet i Christiania på slutten av 1500-tallet."
        ),
    },
    "bind1-borgermestererik-olssonssak-og-jensholms-kampmot-s503": {
        "title": "Borgermesterstrid",
        "year_display": "1600-tallet",
        "place_ids": ["gamle-raadhus-torvet", "garmanngaarden-raadhus"],
        "summary": (
            "Erik Olssønssak og Jens Holm kjempet mot kongelige og lokale maktpersoner om byens selvstyre. "
            "Konflikten om borgermesterembetet viste at borgerne ikke lot seg styre uten motstand."
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
    print(f"parafrase bind I context: {n} oppdatert")


if __name__ == "__main__":
    main()