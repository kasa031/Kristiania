#!/usr/bin/env python3
"""Utvid funn med trofaste parafraser fra Bull bind I (s. 21-24, 219-221)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDS_PATH = ROOT / "data" / "finds.json"

VIKING_BASE = (
    "Gravfunn fra vikingtiden viser vanlig bygdebebyggelse og jordbruk i Aker, "
    "ikke tegn på markedsplass før Oslo ble anlagt. Mye er ødelagt av senere bygging og rot i grunnen."
)

SUMMARIES: dict[str, str] = {
    "funn-skivespaiter-torshov": (
        "De tidligste menneskespor her går tilbake til tapestiden, da havet sto langt høyere og strandlinjen "
        "lå oppe ved området som nå er Torshovjordet. En flintskivespaiter - et redskap til skjæring og hogging - "
        "er funnet på jordet innenfor dagens bygrense, i omkring 70 meters høyde over havet, altså ikke langt fra "
        "den gamle kyststripen."
    ),
    "funn-nostvet-daeleneng": (
        "I Dælenenggaten er det gjort et funn fra samme fjerne tid som på Torshov: omkring førti økser av "
        "Nøstvettypen, flintstykker, slipestensstumper, østerskaller og tildsrest. Dette tyder på fast boplass, "
        "ikke bare flakkende jegere. Folk bodde ikke der det senere ble Oslo - det lå under vann - men langs "
        "fjorden der landet var tørt. Fundet ligger noen meter lavere enn på Torshov, så strandlinjen kan ikke "
        "beregnes helt nøyaktig. Området har også vært et viktig gravningsfelt for arkeologer."
    ),
    "funn-netstikke-jernbanetorvet": (
        "I 1917 ble det ved Jernbanetorvet, på tomten til et nytt hus, funnet en netstikke av ben - et primitivt "
        "redskap til fiskegarn. Den er antatt fra en svært gammel tid, eldre enn steinalderfunnene på Torshov "
        "og Dæleneng."
    ),
    "funn-teisen-solv-1844": (
        "På Teisen i Østre Aker ble det i 1844 funnet en stor mengde sølvsaker i jordskorpen: mest ringer, "
        "men også barrer og stenger. Med sølvet lå kufiske mynter fra kalifene østover - betalingsmidler "
        "som nådde Norden via øst-europeisk handel. De yngste myntene er fra omkring år 920. Skatten kan "
        "sannsynligvis ikke være gravlagt før midten av 900-tallet; den kan tenkes knyttet til uroen på "
        "960-tallet, da rivaler kjempet om Viken. Funnet viser tett bebyggelse og samferdsel med fremmede "
        "land ved fjordbunnen."
    ),
    "funn-grav-viking-st-hanshaugen": (
        VIKING_BASE
        + " Flere gravfunn er kjent fra distriktet omkring St. Hanshaugen. En gravhaug på selve St. Hanshaugen "
        "er senere forsvunnet fordi byen bygde og gravde uten å ta vare på oldsaker."
    ),
    "funn-grav-viking-kampen": (
        VIKING_BASE
        + " Fra Kampen er det gravfunn fra vikingtiden. På toppen av Kampen lå også en gravhaug som i dag er borte."
    ),
    "funn-grav-viking-frogner": (
        VIKING_BASE
        + " Flere gravfunn fra vikingtiden er dokumentert fra Frogner, i de øvre bydelene langs bygden."
    ),
    "funn-grav-viking-pilestredet": (
        VIKING_BASE + " Det er gravfunn fra vikingtiden ved Pilestrædet, i det øvre Kristiania-området."
    ),
    "funn-grav-viking-ullevaal": (
        VIKING_BASE
        + " Det er gravfunn fra vikingtiden langs Ullevålsveien, i de øvre bydelene."
    ),
    "funn-grav-viking-disen": (
        VIKING_BASE + " To ulike gravfunn fra vikingtiden er registrert ved Disen i Østre Aker."
    ),
    "funn-grav-viking-sinsen": (
        VIKING_BASE + " Ett gravfunn fra vikingtiden er kjent fra Sinsen."
    ),
    "funn-grav-viking-ulven": (
        VIKING_BASE + " To ulike gravfunn fra vikingtiden er dokumentert ved Ulven i Østre Aker."
    ),
    "funn-grav-viking-frydenberg": (
        VIKING_BASE + " To gravfunn fra vikingtiden er gjort ved Frydenberg ved Hasle."
    ),
    "funn-grav-viking-bjolsen": (
        VIKING_BASE + " Det er gravfunn fra vikingtiden ved Bjølsen i Vestre Aker."
    ),
    "funn-grav-viking-nydalen": (
        VIKING_BASE + " Det er gravfunn fra vikingtiden ved Nydalen i Vestre Aker."
    ),
    "funn-grav-viking-bestum": (
        VIKING_BASE + " Det er gravfunn fra vikingtiden ved Bestum i Vestre Aker."
    ),
    "funn-grav-viking-rod": (
        VIKING_BASE + " Det er gravfunn fra vikingtiden ved Rød."
    ),
    "funn-grav-viking-taasen": (
        VIKING_BASE + " Det er gravfunn fra vikingtiden ved Taasen."
    ),
    "funn-grav-viking-hov": (
        VIKING_BASE + " Det er gravfunn fra vikingtiden ved Hov i Vestre Aker."
    ),
}

VAULT_IMG = {
    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Middelalderrom_Osloladegard.jpg/640px-Middelalderrom_Osloladegard.jpg",
    "credit": "Wikimedia Commons - middelalderrom Osloladegård (illustrasjon)",
}

BARROW_IMG = {
    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Viking_Age_grave_mound.jpg/640px-Viking_Age_grave_mound.jpg",
    "credit": "Wikimedia Commons - gravhaug (illustrasjon)",
}

NEW_FINDS = [
    {
        "id": "funn-gravhaug-blaasen",
        "title": "Gravhaug på Blåsen (forsvunnet)",
        "year_from": 500,
        "year_to": 1100,
        "year_display": "forhistorisk gravhaug",
        "chronology_era_id": "jernalder",
        "district_id": "st-hanshaugen",
        "lat": 59.951,
        "lng": 10.688,
        "summary": (
            "Innenfor dagens bygrense fantes flere gravhauger som er borte i dag. På Blåsen lå en slik haug som "
            "forsvant når byen bygde og gravde i grunnen uten å ta vare på det som dukket opp. Gull og sølv ble "
            "gjerne tatt av folk; annet ble kastet."
        ),
        "verified": False,
        "source_ref": {"bind": 1, "pages": "23", "note": "Bull bind I: forsvunnede gravhauger"},
        "image": BARROW_IMG,
    },
    {
        "id": "funn-gravhaug-ostre-aker-kirke",
        "title": "Gravhaug ved Østre Aker kirke",
        "year_from": 500,
        "year_to": 1100,
        "year_display": "bevart gravhaug",
        "chronology_era_id": "jernalder",
        "district_id": "grorud",
        "lat": 59.958,
        "lng": 10.843,
        "summary": (
            "Ved Østre Aker kirke står en stor gravhaug fortsatt bevart. I motsetning til mange hauger i byen "
            "er den ikke revet ned av bygging, men det er ikke gjort funn inne i den."
        ),
        "verified": False,
        "source_ref": {"bind": 1, "pages": "23", "note": "Bull bind I: bevart haug uten funn"},
        "image": BARROW_IMG,
    },
    {
        "id": "funn-bispeborg-utgravning-1917",
        "title": "Utgravning av bispeborgen (1917)",
        "year_from": 1917,
        "year_to": 1917,
        "year_display": "utgravning 1917",
        "chronology_era_id": "middelalder",
        "district_id": "gamle-oslo",
        "lat": 59.9058,
        "lng": 10.7672,
        "summary": (
            "Da man gravde i Ladegårdshaven i 1917, kom rester av bispeborgen frem: ringmur, kjellervelvinger og "
            "rom i middelalderens geistlige festning. Det som er funnet, er eldre enn Akershus som vi kjenner det "
            "etter Håkon V, men mer komplekst enn den tidlige bispeborgen fra 1200-tallet. Utgravningene bidro til "
            "å forstå festningen som ble brent i 1287."
        ),
        "verified": False,
        "source_ref": {"bind": 1, "pages": "219-221", "note": "Bull bind I: bispeborg og utgravning"},
        "image": VAULT_IMG,
    },
]


def main() -> None:
    data = json.loads(FINDS_PATH.read_text(encoding="utf-8"))
    finds = data.get("finds", [])
    ids = {f["id"] for f in finds}
    updated = 0
    for f in finds:
        key = f.get("id", "")
        if key in SUMMARIES:
            f["summary"] = SUMMARIES[key]
            updated += 1
    for nf in NEW_FINDS:
        if nf["id"] not in ids:
            finds.append(nf)
            ids.add(nf["id"])
    data["finds"] = finds
    FINDS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"enrich-finds-bind1: oppdatert {updated} oppsummeringer, {len(finds)} funn totalt")


if __name__ == "__main__":
    main()