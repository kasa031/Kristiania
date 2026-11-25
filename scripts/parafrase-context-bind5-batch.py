#!/usr/bin/env python3
"""A14: bind V context (1878-1924, storby og jubileum)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, dict] = {
    "bind5-statuerog-mennesker-s35": {
        "title": "Statuer og monumenter",
        "year_display": "1880-årene",
        "place_ids": ["eidsvolls-plass", "stortinget", "slottsplassen"],
        "summary": (
            "Offentlige statuer og minnesmerker ble et samlingspunkt for debatt om nasjon og kultur. "
            "Byen diskuterte hvem som fortjente et monument og hvordan gater og plasser skulle pyntes."
        ),
    },
    "bind5-tidsaandenog-forholdeneomkring-1880-s55": {
        "title": "Kulturkampen rundt 1880",
        "year_display": "1880-1882",
        "place_ids": ["eidsvolls-plass", "universitetsplassen", "nationaltheatret"],
        "summary": (
            "Diskusjonen om et Eidsvollsmonument og feiring av kronprinsparet viste dyp splittelse i byens kulturliv. "
            "Venstre og høyre strid om Wergeland og nasjonssymboler preget avisene og studentmiljøet."
        ),
    },
    "bind5-muligheterog-tillop-s69": {
        "title": "Muligheter og tilløp",
        "year_display": "1880-årene",
        "place_ids": ["karl-johan-jubileet", "youngstorget"],
        "summary": (
            "Ny teknologi, handel og foreningsliv ga hovedstaden et mer moderne preg på 1880-tallet. "
            "Tilløp til industri, bankvesen og byliv skapte både optimisme og konkurransetenkning."
        ),
    },
    "bind5-kommunestyretog-oppositioneni-begyndelsenav-1880-s85": {
        "title": "Nybygging i sentrum",
        "year_display": "1880-1881",
        "place_ids": ["norges-bank-bankplassen", "tollbugata-havn", "christiania-torv"],
        "summary": (
            "Storebrand, Handelsstandsforeningen og Steen og Strøm reiste nye fasader i kvadraturen. "
            "Gjennombrudd i Slottsgate og Schweigaards bro bandt Bjørvika og Pipervika til et moderne gatebilde."
        ),
    },
    "bind5-okonomisketiltak-og-forskyvninger-i-begyndelsena-s133": {
        "title": "Økonomi i storbytiden",
        "year_display": "1880-årene",
        "place_ids": ["norges-bank-bankplassen", "youngstorget"],
        "summary": (
            "Banker, aksjer og konjunkturer satte preg på byens økonomi da Kristiania vokste raskt. "
            "Kommunen og næringslivet måtte finne balanse mellom vekst, lån og nedgangstider."
        ),
    },
    "bind5-byen-og-det-begyndendesocial-demokrati-s149": {
        "title": "Aksjer og arbeiderbevegelse",
        "year_display": "ca. 1880",
        "place_ids": ["youngstorget", "mollergata"],
        "summary": (
            "Aksieomsætning og nye pengeinstitutter vokste side om side med industri og håndverk. "
            "Samtidig begynte sosialdemokratiske strømninger å samle arbeidsfolk i byens presserom og gater."
        ),
    },
    "bind5-bryggeforholdog-havnereguleringeromkring-aarhund-s297": {
        "title": "Havn og kommunefinans",
        "year_display": "1899-1900",
        "place_ids": ["tollbugata-havn", "pipervika", "oslo-sentralstasjon"],
        "summary": (
            "Kommunen lånte tungt for kai-anlegg og regulering mot århundreskiftet. "
            "Debatt om eiendomsinnkjøp og finansplan preget magistratens styring av havneutviklingen."
        ),
    },
    "bind5-nedgangsaareneog-folgerneav-demi-slutten-avunion-s313": {
        "title": "Nedgang og unionsavslutning",
        "year_display": "1900-1905",
        "place_ids": ["grunerlokka-folketeater", "akerselva-utløp"],
        "summary": (
            "Øst for Akerselva ble utbygging og kommunale kjøp viktige grep da økonomien svingte. "
            "Unionstidens slutt endret både investeringer og byens politiske puls."
        ),
    },
    "bind5-kristiania-i-1905-s327": {
        "title": "Kristiania i 1905",
        "year_display": "1904-1905",
        "place_ids": ["stortinget", "var-frelsers-gravlund"],
        "summary": (
            "Brann i Kongens gate, banksammenbrudd og valgpreget gatenes stemning rundt unionskrisen. "
            "Byen fulgte Stortinget og finansverdenen tett mens Norge løsnet fra unionen med Sverige."
        ),
    },
    "bind5-fra-unionsbruddettil-jubilaeumsaaret1914-s375": {
        "title": "Mot jubileumsåret 1914",
        "year_display": "1908-1914",
        "place_ids": ["eidsvolls-plass", "nationaltheatret", "var-frelsers-gravlund"],
        "summary": (
            "Wergelandsdag, nye monumenter og nasjonale minner la grunnlag for 300-årsjubileet. "
            "Kristiania brukte festtaler, teater og statuer til å markere byens plass i fedrelandshistorien."
        ),
    },
    "bind5-kommunenog-boligsporsmaalet-s393": {
        "title": "Bolig og kommune",
        "year_display": "1910-årene",
        "place_ids": ["gronland-ladested", "grunerlokka-folketeater"],
        "summary": (
            "Bolignød og leiegårder ble et hovedspørsmål da folketallet vokste inn i jubileumsårene. "
            "Kommunen bygde leieboliger og diskuterte grenser mot Akers for å få plass til arbeidsfolk."
        ),
    },
    "bind5-de-sidstefernaarfor-navnskiftet-s493": {
        "title": "Før navnet ble Oslo",
        "year_display": "1920-1924",
        "place_ids": ["karl-johan-jubileet", "stortinget"],
        "summary": (
            "De siste årene som Kristiania ble preget av boligbygging, grenseutvidelse og modernisering. "
            "Byen nærmet seg 1924-jubileet og det kommende navneskiftet til Oslo."
        ),
    },
    "bind5-hovedstadenved-indledningentil-unionskrisen-s201": {
        "title": "Før unionskrisen",
        "year_display": "1890-årene",
        "place_ids": ["stortinget", "paleet-christiania"],
        "summary": (
            "Hovedstaden fulgte unionsspørsmål og kommunal byggelov med stigende spenning før 1905. "
            "Magistrat og Storting diskuterte både arkitektur og den politiske balansen i unionen."
        ),
    },
    "bind5-literaturensog-virkelighetenskristiania-s523": {
        "title": "Litteratur og byliv",
        "year_display": "1900-årene",
        "place_ids": ["nationaltheatret", "henrik-ibsen-hjem"],
        "summary": (
            "Forfattere og teater skildret Kristiania som både drøm og virkelighet. "
            "Byen i romaner og på scenen speilet bolignød, fest og klasseforskjeller."
        ),
    },
    "bind5-kristianias-ordforere1837-1924-s533": {
        "title": "Ordførere 1837-1924",
        "year_display": "1837-1924",
        "place_ids": ["kommunegaarden-logen", "gamle-raadhus-torvet"],
        "summary": (
            "Fra formannskapsloven til jubileumsåret førte en rekke ordførere kommunen gjennom vekst og reform. "
            "Deres beslutninger om skoler, gater og bolig satte spor i gatebildet vi går i i dag."
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
    print(f"parafrase bind V context: {n} oppdatert")


if __name__ == "__main__":
    main()