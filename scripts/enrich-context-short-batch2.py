#!/usr/bin/env python3
"""Utvid korte context-sammendrag (A14) fra utdrag/notater."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, str] = {
    "bind2-handel-og-skibsfart-i-krigs-og-nedgangstider-s417": (
        "Etter en stor tollsak i 1705 ble kjøbmenn og skippsførere kalt inn til forhør og truet med "
        "at bøker og regnskap skulle granskes. Vicegouverør Gabel mente mange var uskyldige, men "
        "undersøkelsen skapte panikk: handelen stanset opp, kreditten sviktet, og borgerskapet fryktet "
        "både ruin og å måtte sverge seg til forklaringer de ikke stod inne for. Slikt satte preg på "
        "Christianias handel i krigs- og nedgangstider ved havnen."
    ),
    "bind1-biskopenejakob-og-jens-1407-52-s284": (
        "Biskop Jakob kom til Oslo i 1407 og ble fulgt av biskop Jens i 1408. De førte kirken gjennom "
        "unionstida og sorte pest, kjempet mot reformatoriske strømninger og måtte forvalte "
        "bispegårdens jorder og lemninger når pesten tømte byen. Deres tid binder sammen kirke, "
        "geistlig makt og det myrdede middelalder-Oslo."
    ),
    "bind1-kampenfor-handelsmonopolet-s451": (
        "Kronen, Hansaen og innenlandske kjøpmenn konkurrerte om hvem som skulle få kjøpe og selge "
        "korn og trelast. Privilegier og monopol regulerte torvhandel og utenrikshandel; kampen handlet "
        "om inntekter til kronen og om hvem som kontrollerte Oslos knutepunkt mot fjorden."
    ),
    "bind5-den-nye-arbeidsdagog-hovedstadenindtil-bjornsons-s353": (
        "På slutten av 1800-tallet ble arbeidsdagen preget av fabrikk og verksted, fagforeninger og "
        "streiker. I hovedstaden møttes gamle laugtradisjoner og ny organisering; arbeidere slo seg "
        "sammen i gate, presse og møterom inntil krigen og Bjørnsons siste år."
    ),
}


def main() -> None:
    doc = json.loads(CTX.read_text(encoding="utf-8"))
    n = 0
    by_id = {e["id"]: e for e in doc.get("entries", [])}
    for eid, summary in PATCHES.items():
        if eid in by_id:
            by_id[eid]["summary"] = summary
            n += 1
    CTX.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"enrich-context-short-batch2: {n} oppdatert")


if __name__ == "__main__":
    main()