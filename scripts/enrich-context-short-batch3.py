#!/usr/bin/env python3
"""Utvid korte bind II/V context-sammendrag (A14)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, str] = {
    "bind2-de-aeldste-laugene-i-kristiania-s199": (
        "Håndverkslavene og kjøbmennene i Christiania kjempet mot råd og stattholder om privilegier, "
        "toldfrihet og hvem som fikk bestemme i byen. I 1651 leverte borgerskapet en lang klage om "
        "ulovlig handel, skatter og bymarken - og striden endte først i et skjørt forlik i 1652."
    ),
    "bind1-de-aeldstebyprivilegiene-s229": (
        "De gamle kjøpstadsprivilegiene ga borgere enerett på handel og satte rammer for hvem som "
        "fikk drive næring i Christiania. Bestemmelsene bandt byen til kronen og skapte grunnlag "
        "for århundrer med strid om marked, toll og forsteder."
    ),
    "bind3-handel-og-skibsfart-i-revolutionstiden-s375": (
        "Under revolusjonskrigen på slutten av 1700-tallet måtte Christianias handel og sjøfart "
        "finne nye veier. Blokader, priser og politisk uro gjorde byens kjøpmenn og skip til "
        "pionerer i et farlig handelsmiljø."
    ),
    "bind4-romantikog-skandinavismei-krig-og-fred-s329": (
        "Romantikken og skandinavismen fikk fotfeste i hovedstaden samtidig som Norden gikk inn i "
        "krig og fred med hverandre. Stemninger i kulturlivet vekslet med union, press og ny "
        "selvbevissthet i byen."
    ),
    "bind5-stemningerog-forhold-indtil-utgangenav-1918-s455": (
        "Før første verdenskrig sluttet, bar Christiania preg av krise, knapphet og fornyet tro på "
        "fremtid. Stemninger i pressen og gatene speilte en by som var vant til storpolitikk, men "
        "nå skulle definere hverdagen på nytt."
    ),
    "bind5-literaturensog-virkelighetenskristiania-s523": (
        "På 1920-tallet møttes litteratur og hverdagsliv i en by i vekst. Forfattere, aviser og "
        "teater speilet storbyens karakter, samtidig som jubileet og navneskiftet minnet folk om "
        "at Kristiania og Oslo var samme bys ulike kapitler."
    ),
}


def main() -> None:
    doc = json.loads(CTX.read_text(encoding="utf-8"))
    n = 0
    for e in doc.get("entries", []):
        key = e.get("id", "")
        if key in PATCHES:
            e["summary"] = PATCHES[key]
            n += 1
    CTX.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"enrich-context-short-batch3: {n} oppdatert")


if __name__ == "__main__":
    main()