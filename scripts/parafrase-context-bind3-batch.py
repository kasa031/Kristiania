#!/usr/bin/env python3
"""A14: manuelle parafraser for bind III context (1740-1814)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, dict] = {
    "bind3-forfatnings-og-forvaltningsutviklingen-fra-1740-s35": {
        "title": "Forvaltning fra 1740",
        "year_display": "1740-årene",
        "place_ids": ["stortinget", "kommunegaarden-logen"],
        "summary": (
            "Etter 1740 ble embetsstrukturen og byforvaltningen styrket i takt med sentralmaktens krav. "
            "Kristiania utviklet seg som administrasjonssenter der magistrat, embedsmenn og kongelig myndighet møttes."
        ),
    },
    "bind3-privilegiene-s87": {
        "title": "Byens privilegier og skatt",
        "year_display": "1700-tallet",
        "place_ids": ["gammeltorvet", "youngstorget"],
        "summary": (
            "Kjøpmannsbyen regulerte handel, skatt og fattigvesen gjennom privilegier og offentlige kunngjøringer. "
            "Borgerne fikk vite hvordan byens utgifter og ligning skulle beregnes og fordeles."
        ),
    },
    "bind3-byen-og-oplandet-s103": {
        "title": "By og opland",
        "year_display": "1700-1800-tallet",
        "place_ids": ["pipervika", "akerselva-utløp", "nydalens-compagnie"],
        "summary": (
            "Kristiania levde av koblingen mellom fjord, elv og skog i omlandet. "
            "Trelast, fløting og handel på havnen bandt byborgerne til distriktene rundt fjorden."
        ),
    },
    "bind3-befolkningen-s159": {
        "title": "Befolkningsvekst",
        "year_display": "1700-1800-tallet",
        "place_ids": ["st-hanshaugen-haugen", "gronland-ladested"],
        "summary": (
            "Byen vokste med håndverk, tjenestefolk og folk utenfor de gamle bygrensene. "
            "Folketellinger viser flere tusen innbyggere og et sosialt spekter fra kjøpmenn til dagleiere."
        ),
    },
    "bind3-offentlighet-s175": {
        "title": "Folketelling og samfunnslag",
        "year_display": "ca. 1801",
        "place_ids": ["stortorvet", "stortinget"],
        "summary": (
            "Folketellingen i 1801 delte byen i yrkesgrupper: kjøpmenn, håndverkere, tjenestefolk og soldater. "
            "Tallene viser en by på vei mot unionshovedstad, med tusenvis av innbyggere fordelt på arbeid og embed."
        ),
    },
    "bind3-handel-og-skibsfart-i-revolutionstiden-s375": {
        "title": "Handel og sjøfart i krigstid",
        "year_display": "Napoleonskrigenes tid",
        "place_ids": ["havn-ved-akershus", "tollbugata-havn"],
        "summary": (
            "Europeiske kriger rammet norsk sjøfart og varestrømmer. "
            "Reglene om flagg, blokade og salg av skip preget livet på havnen og handlerne i Kristiania."
        ),
    },
    "bind3-laugene-s453": {
        "title": "Laug og uro i byen",
        "year_display": "1795",
        "place_ids": ["youngstorget", "lo-bygget-storgata"],
        "summary": (
            "Spenninger rundt håndverkslaug og forsyninger kunne utløse folkemengder og vakthold i gatene. "
            "Myndigheten fryktet opprør og brukte militær støtte når konflikten mellom folk og embetsmenn ble skarp."
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
    print(f"parafrase bind III context: {n} oppdatert")


if __name__ == "__main__":
    main()