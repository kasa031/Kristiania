#!/usr/bin/env python3
"""A14: bind IV context batch 2 (gjenværende titel-led)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, dict] = {
    "bind4-byen-og-statsmagterne-s67": {
        "title": "Byen og statsmakten",
        "year_display": "1815-1820",
        "place_ids": ["stortinget", "youngstorget"],
        "summary": (
            "I de første unionsårene preget skandaler, handelsmoral og trykkefrihet offentligheten i hovedstaden. "
            "Avisene fulgte kjøpmenn, studenter og embedsmenn tett, og stemningen var ofte sarkastisk og opphisset."
        ),
    },
    "bind4-brandenpaabordtomterne-s79": {
        "title": "Brannen på bordtomtene",
        "year_display": "ca. 1820",
        "place_ids": ["vaterland-bjorvika", "oslo-sentralstasjon", "paleet-christiania"],
        "summary": (
            "Brannen brøt ut på utfylte tomter mellom byen og Vaterland, der jernbanetorvet senere kom. "
            "Borgerlige brannsvender, garnison og frivillige rykket ut, men vannledningene holdt ikke, og flammene truet både fattige og velstående strøk."
        ),
    },
    "bind4-kristiania-oppositionenav-1821-og-forutsaetninge-s91": {
        "title": "Opposisjonen 1821",
        "year_display": "1821",
        "place_ids": ["stortinget", "paleet-christiania"],
        "summary": (
            "Politisk motsetning mellom embedsmenn og reformvennlige grupper preget hovedstaden rundt 1821. "
            "Debatt om union, økonomi og byens selvstendige interesser fikk stor plass i avisene og på Stortinget."
        ),
    },
    "bind4-kongeboligenog-byen-s141": {
        "title": "Kongeboligen og byen",
        "year_display": "1820-årene",
        "place_ids": ["slottsplassen", "paleet-christiania"],
        "summary": (
            "Nytt kongelig bygg og byens voksende kulturliv endret hverdagsbildet i unionshovedstaden. "
            "Kvinners utdanning og husflid ble diskutert, blant annet gjennom forslag om håndverksskole for piker i byen."
        ),
    },
    "bind4-okonomisketiltak-og-forskyvninger-gjennem1820-aa-s157": {
        "title": "Økonomi i 1820-årene",
        "year_display": "1820-årene",
        "place_ids": ["youngstorget", "norges-bank-bankplassen"],
        "summary": (
            "Statsbankerott og gjeldssanering preget handel og forventninger i byen etter Napoleonskrigene. "
            "Nye økonomiske tiltak og skiftende konjunkturer preget hovedstadens borgeres hverdag."
        ),
    },
    "bind4-hovedstadenog-dennye-tidsaand-s189": {
        "title": "Ny tidsånd",
        "year_display": "1828-1830-årene",
        "place_ids": ["gronland-ladested", "universitetsplassen"],
        "summary": (
            "Aviser og reisende beskrev trange skjul i forstedene og synlig fattigdom blant arbeidsfolk. "
            "Samtidig vokste offentlig debatt om sedelighet, bolig og forskjellen mellom Bergen og Kristiania."
        ),
    },
    "bind4-reguleringsproblemetog-denoffentlige-mening-s245": {
        "title": "Regulering og kommuneøkonomi",
        "year_display": "1838-1840",
        "place_ids": ["pipervika", "kommunegaarden-logen"],
        "summary": (
            "Formannskapet gikk varsomt frem med utgifter til skoler og offentlige anlegg, også i Pipervika. "
            "Kommunen ville ikke ta unødige lån, men ønsket forbedringer trinnvis der behovet var størst."
        ),
    },
    "bind4-stromningerog-bakevjer-henimotslutten-av-wergela-s259": {
        "title": "Mot slutten av Wergelands tid",
        "year_display": "1840-årene",
        "place_ids": ["stortorvet", "eidsvolls-plass"],
        "summary": (
            "Yngre forfattere og offentlige strømninger utfordret Wergelands generasjon i byens kulturliv. "
            "Politisk og litterær debatt foregikk side om side med gatepreget hverdagsliv i sentrum."
        ),
    },
    "bind4-socialeog-kulturelle-nydannelseri-1840-aarene-s277": {
        "title": "Nydannelser på 1840-tallet",
        "year_display": "1840-årene",
        "place_ids": ["universitetsplassen", "nationaltheatret"],
        "summary": (
            "Foreninger, teater og folkeopplysning fikk fotfeste i byen på 1840-tallet. "
            "Nye sosiale og kulturelle skikkelser supplerte det gamle embets- og borgerskapet."
        ),
    },
    "bind4-storfolk-og-smaafolki-1840-aarene-s297": {
        "title": "Storfolk og småfolk",
        "year_display": "1840-årene",
        "place_ids": ["gronland-ladested", "homansbyen"],
        "summary": (
            "Skillene mellom velstående gatestrøk og trange forsteder ble tydeligere i 1840-årene. "
            "Borgerliv og arbeiderboliger fantes få kvartaler fra hverandre i den voksende hovedstaden."
        ),
    },
    "bind4-tidsaandenog-forholdenefor-og-efter-branden-s459": {
        "title": "Etter brannen i 1858",
        "year_display": "1858-1860",
        "place_ids": ["skippergata", "tollbugata-havn"],
        "summary": (
            "Etter den store brannen ble havn, losseforhold og navngiving diskutert med ny selvtillit i byen. "
            "Trang kaiplass og tungvint utløsning preget havnen inntil reguleringen ble utvidet."
        ),
    },
    "bind4-kristiania-skandinavismenog-denationaleminder-s521": {
        "title": "Skandinavisme og monumenter",
        "year_display": "1860-1870-årene",
        "place_ids": ["eidsvolls-plass", "stortinget"],
        "summary": (
            "Skandinavisk samfølelse og nasjonale minnesmerker fikk plass i bybildet i andre halvdel av 1800-tallet. "
            "Monumenter og festligheter knyttet hovedstaden til hele Norden."
        ),
    },
    "bind4-det-storetidsskifte-s539": {
        "title": "Det store tidsskifte",
        "year_display": "1870-årene",
        "place_ids": ["grunerlokka-folketeater", "st-hanshaugen-haugen"],
        "summary": (
            "Industri, jernbane og ny bebyggelse tegnet et bykart i rivende endring før utvidelsen i 1877. "
            "Gamle småbyvaner møtte storbyens krav til infrastruktur og bolig."
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
    print(f"parafrase bind IV batch2: {n} oppdatert")


if __name__ == "__main__":
    main()