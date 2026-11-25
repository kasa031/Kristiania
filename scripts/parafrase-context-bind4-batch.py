#!/usr/bin/env python3
"""A14: manuelle parafraser for bind IV context (1814-1877)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, dict] = {
    "bind4-menneskerog-forhold-ide-forste-selvstaendighetsa-s27": {
        "title": "1814 i hovedstaden",
        "year_display": "1814",
        "place_ids": ["stortinget", "eidsvolls-plass", "slottsplassen"],
        "summary": (
            "Da Norge ble løsrevet fra Danmark, tok livet i hovedstaden et mer politisk preg. "
            "Aviser, embetsmenn og offentlig debatt fulgte freden og grunnlovsåret tett."
        ),
    },
    "bind4-socialeog-kulturelle-motsaetninger-s47": {
        "title": "Sosiale og kulturelle motsetninger",
        "year_display": "1814-1840",
        "place_ids": ["universitetsplassen", "homansbyen"],
        "summary": (
            "Embetskultur, borgerskap og nye strømninger støtte mot hverandre i unionshovedstaden. "
            "Utdanning og offentlig ordelagte premisser for hvem som ble hørt i byens debatter."
        ),
    },
    "bind4-hovedstadenog-17-mai-til-og-medtorvslaget-s107": {
        "title": "17. mai og Torvslaget",
        "year_display": "1820-årene",
        "place_ids": ["stortorvet", "stortinget"],
        "summary": (
            "17. mai-feiring og politisk uro rundt stortorget skapte spanning mellom folk og myndigheter. "
            "Konflikten som ble kjent som Torvslaget viste at nasjonaldagen ikke var uproblematisk i hovedstaden."
        ),
    },
    "bind4-arbeiderkaarog-arbeidsforholdi-1820-og-1830-aare-s175": {
        "title": "Arbeid og bolig",
        "year_display": "1820-1830-årene",
        "place_ids": ["gronland-ladested", "sagene-loken"],
        "summary": (
            "Arbeidsfolk i forstedene bodde trangt med ett kjøkken til flere familier. "
            "Undersøkelser viser tette leiligheter, lav boligkvalitet og birente for mange hustruer."
        ),
    },
    "bind4-branden14-april-1858-s423": {
        "title": "Bybrannen 14. april 1858",
        "year_display": "1858",
        "place_ids": ["skippergata", "christiania-torv", "gammeltorvet"],
        "summary": (
            "Den store brannen i april 1858 herjet et omfattende område i Kvadraturen. "
            "Slukningsmannskap trakk seil over hustak i Kongens gate, men ilden blusset opp igjen ved Peter Petersens gård før den ble stanset mot formiddag."
        ),
    },
    "bind4-havnenog-havnelivetfra-1830-til-1860-aarene-s439": {
        "title": "Havn og havneliv",
        "year_display": "1830-1860",
        "place_ids": ["havn-ved-akershus", "tollbugata-havn", "pipervika"],
        "summary": (
            "Havnen vokste med handel, dampskip og trevareomlasting i årene før århundreskiftet. "
            "Molene og bryggene ved Pipervika og Akershus holdt byen i stadig kontakt med sjøen."
        ),
    },
    "bind4-de-forste-kommunestyrerog-deresgrundsyn-socialto-s227": {
        "title": "Første kommunestyrer",
        "year_display": "1837",
        "place_ids": ["kommunegaarden-logen", "gamle-raadhus-torvet"],
        "summary": (
            "Formannskapsloven ga byen folkevalgte styremenn med ansvar for skole, fattigvesen og gater. "
            "Det la grunnlaget for moderne kommunal styring i Kristiania."
        ),
    },
    "bind4-byutvidelsenav-1877-og-forutsaetningernefor-den-s555": {
        "title": "Byutvidelsen 1877",
        "year_display": "1877",
        "place_ids": ["st-hanshaugen-haugen", "grunerlokka-folketeater"],
        "summary": (
            "Utvidelsen i 1877 gjorde store deler av bymarken til en del av byen. "
            "Nye bydeler som Grünerløkka og Sagene kom inn i det regulerte bykartet etter hard politisk strid."
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
    print(f"parafrase bind IV context: {n} oppdatert")


if __name__ == "__main__":
    main()