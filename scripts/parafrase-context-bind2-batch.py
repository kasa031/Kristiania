#!/usr/bin/env python3
"""A14: manuelle parafraser for bind II context (fra utdrag)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, dict] = {
    "bind2-gamlebyen-s141": {
        "title": "Gamlebyen etter 1624",
        "year_display": "1600-1700-tallet",
        "place_ids": ["domkirken-gamlebyen", "middelalderparken", "bispegarden"],
        "summary": (
            "Skole og domkapittel flyttet til Kristiania etter at gymnas og ny kirke sto ferdig. "
            "Mariakirken og Hallvardskirken i gamle Oslo forfalt og ble ruiner og bygningsmaterialer. "
            "Kjernen i Gamlebyen ble Osloladegaarden og det gamle bispeanlegget som senere ble kjent som Ladegaarden."
        ),
    },
    "bind2-forstaedene-153-s154": {
        "title": "Forstædene utenfor murene",
        "year_display": "1600-1700-tallet",
        "place_ids": ["gronland-ladested", "vaterland-bjorvika", "pipervika"],
        "summary": (
            "Utenfor kjøbmannsbyen vokste forstæder med billig trehus og husnæring. "
            "Myndighetene ville begrense ulovlig handel i Vaterland og samle folk innenfor festningen, "
            "men forstedene besto fordi topografi og bondehandel trakk bebyggelsen utover."
        ),
    },
    "bind2-pest-og-fest-s165": {
        "title": "Pest og byliv",
        "year_display": "1600-1700-tallet",
        "place_ids": ["vaterland-bjorvika", "christiania-torv"],
        "summary": (
            "Pest og brann preget byens rytme sammen med sommerliv ved havnen og vinterstille. "
            "Pestepidemien i 1654 tok mange liv; kirkegårdene tok ikke imot alle, og ny gravplass ble anlagt ved Hammersborg."
        ),
    },
    "bind2-befolkningen-53-s68": {
        "title": "Befolkning og byelite",
        "year_display": "1600-1700-tallet",
        "place_ids": ["gamle-raadhus-torvet", "radmannsgaarden"],
        "summary": (
            "Kristianias befolkning ble styrket av indvandrende kjøpmenn og embedsmenn. "
            "Familier som Gaarman og Krefting knyttet seg til skog, verk og lån til kronen, og investerte i bygninger og gods rundt byen."
        ),
    },
    "bind2-byen-og-oplandet-s123": {
        "title": "Byen og oplandet",
        "year_display": "1600-1700-tallet",
        "place_ids": ["pipervika", "tollbugata-havn"],
        "summary": (
            "Freden mellom Spania og Nederlandene i 1648 endret kontinenthandelen. "
            "Hollendere formidlet norsk trelast videre mot Sør-Europa, og Kristiania sto i et nett av sjøfart som bandt byen til oplandet."
        ),
    },
    "bind2-privilegiene-s173": {
        "title": "Privilegier og byens rammer",
        "year_display": "1600-1700-tallet",
        "place_ids": ["gammeltorvet", "vaterland-bjorvika"],
        "summary": (
            "Bylivet svingte mellom travl sommer ved havnen og stille vintre, avbrutt av marked og hofflige seremonier. "
            "Pest og brann viste at byen ennå ikke hadde lært å begrense de store ulykkene som traff en hovedstad ved fjorden."
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
    print(f"parafrase bind II context: {n} oppdatert")


if __name__ == "__main__":
    main()