#!/usr/bin/env python3
"""A14: resterende titel-led og OCR-rot i context.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, dict] = {
    # Bind I
    "bind1-bispeneorm-torkel-og-haakonstid-s91": {
        "title": "Tidlige biskoper",
        "year_display": "1000-1100-tallet",
        "place_ids": ["domkirken-oslo", "bispegarden"],
        "summary": (
            "Biskopene Orm, Torkel og Haakon bygde kirkestrukturen i Oslo i vikingtid og tidlig middelalder. "
            "Domkirken og bispegården la grunnlaget for kirke og kongemakt i byen."
        ),
    },
    "bind1-biskopandres-i-domkapitlet-s100": {
        "title": "Domkapitlet",
        "year_display": "1100-tallet",
        "place_ids": ["domkirken-oslo"],
        "summary": (
            "Domkapitlet samlet prestene rundt Oslo domkirke og knyttet byen til kirkens ledelse. "
            "Biskop Andres og kapittelet styrte liturgi, skoler og kirkens eiendommer i byen."
        ),
    },
    "bind1-haakonvfs-og-dronning-margretestid-s263": {
        "title": "Unionstid med Margrete",
        "year_display": "1300-tallet",
        "place_ids": ["akershus", "gammeltorvet"],
        "summary": (
            "Da dronning Margrete styrket unionen, hang Oslo tett sammen med kongemakt og handel. "
            "Borgermestre vekslet mellom nordmenn og utlendinger mens byen holdt sin plass i Kalmarunionen."
        ),
    },
    "bind1-biskopenejakob-og-jens-1407-52-s284": {
        "title": "Biskoper Jakob og Jens",
        "year_display": "1407-1452",
        "place_ids": ["domkirken-oslo", "bispegarden"],
        "summary": (
            "Jakob og Jens ledet kirken i Oslo før reformasjonen. "
            "De forvaltet jorder, bygg og kirkelig lov i en by preget av handel og politisk uro."
        ),
    },
    "bind1-biskopgunnar-holk-nils-kalib-og-herlog-korning-1-s323": {
        "title": "Senesmiddelalders biskoper",
        "year_display": "1453-1505",
        "place_ids": ["domkirken-oslo", "vor-frelsers"],
        "summary": (
            "Gunnar Holk, Nils Kalib og Herlog Korning styrte kirken i overgangen til tidlig moderne tid. "
            "Reformasjonen nærmet seg, og byens kirker stod sentralt i tro og administrasjon."
        ),
    },
    "bind1-bispeneanders-mus-hansmule-og-hansraev-1505-37-s349": {
        "title": "Biskoper før reformasjonen",
        "year_display": "1505-1537",
        "place_ids": ["domkirken-oslo"],
        "summary": (
            "Anders Mus, Hans Mule og Hans Ræv var blant de siste katolske biskopene i Oslo. "
            "Kirkens makt og rikdom i byen ble utfordret da reformasjonen bredte seg."
        ),
    },
    # Bind II
    "bind2-de-aeldste-laugene-i-kristiania-s199": {
        "title": "De eldste lavene",
        "year_display": "1600-tallet",
        "place_ids": ["youngstorget", "gammeltorvet"],
        "summary": (
            "Håndverkslavene organiserte borgerskapet i Christiania. "
            "Statholder og råd stridde om om borgere fikk slutte seg sammen uten kongelig tillatelse."
        ),
    },
    "bind2-byprivilegiene-av-1662-s291": {
        "title": "Byprivilegier 1662",
        "year_display": "1662",
        "place_ids": ["tollbugata-havn", "kontraskjerp"],
        "summary": (
            "Nye tollregler og skibsprivilegier fra 1662 skulle styrke norsk skipsfart og trelasthandel. "
            "Christiania fikk gunstige ordninger for innenlandske skip mot utenlands konkurranse."
        ),
    },
    "bind2-handel-og-skibsfart-i-krigs-og-nedgangstider-s417": {
        "title": "Handel i krigstid",
        "year_display": "1700-tallet",
        "place_ids": ["havn-ved-akershus", "pipervika"],
        "summary": (
            "Krig og blokader rammet skipsfart og priser i Christiania. "
            "Havnen og kjøpmennene måtte tilpasse seg nedgangstider og nye tollkrav."
        ),
    },
    "bind2-den-store-toldsvig-403-s416": {
        "title": "Den store toljsvindelen",
        "year_display": "1700-tallet",
        "place_ids": ["tollbugata-havn"],
        "summary": (
            "En stor toljsvindel skapte raseri i byen og satte tollinspektøren i et dårlig lys. "
            "Pasquiler på gatestolper viste at borgere fulgte korrupsjon og skatt tett."
        ),
    },
    # Bind IV
    "bind4-tanke-og-folelseslivfra-wergelandsdodtil-gjennem-s313": {
        "title": "Etter Wergelands død",
        "year_display": "1840-1850-årene",
        "place_ids": ["eidsvolls-plass", "var-frelsers-gravlund"],
        "summary": (
            "Da Wergeland var borte, søkte nye strømninger å overta byens offentlige liv. "
            "Pietisme og borgerlig dannelse møttes i aviser, foreninger og gravferdskultur."
        ),
    },
    "bind4-romantikog-skandinavismei-krig-og-fred-s329": {
        "title": "Romantikk og skandinavisme",
        "year_display": "1840-1860-årene",
        "place_ids": ["stortinget", "nationaltheatret"],
        "summary": (
            "Romantikken og skandinavisk samfølelse fikk fotfeste i unionstidens hovedstad. "
            "Festning, teater og politikk vevde Norden sammen i byens kulturliv."
        ),
    },
    "bind4-hoikonjunktur-og-formuer-s387": {
        "title": "Høykonjunktur og formuer",
        "year_display": "1850-årene",
        "place_ids": ["homansbyen", "paleet-christiania"],
        "summary": (
            "God konjunktur og nye formuer preget villastrøk og handelsgårder. "
            "Velstående familier flyttet vestover mens arbeidsfolk bodde tettere i eldre strøk."
        ),
    },
    "bind4-byen-og-samfundsforholdeneved-midtenav-1850-aare-s405": {
        "title": "Samfunn ved midten av 1850-årene",
        "year_display": "ca. 1855",
        "place_ids": ["christiania-spigerverk", "ankerbrua"],
        "summary": (
            "Jernbane, telegraf og engelske teknikker endret hverdagen i Christiania midt på 1850-tallet. "
            "Gasverk, rørkloakk og dampskip bandt byen til europeiske moderniseringsstrømninger."
        ),
    },
    # Bind V
    "bind5-forhold-og-begivenhetersidsti-otti-aarene-s169": {
        "title": "Slutten av 1880-årene",
        "year_display": "1888-1889",
        "place_ids": ["karl-johan-jubileet", "nationaltheatret"],
        "summary": (
            "Byggeboomen og politisk strid preget slutten av 1880-årene i hovedstaden. "
            "Nye institusjoner og gateplaner skapte både optimisme og kommunal motstand."
        ),
    },
    "bind5-fra-otti-ind-i-nitti-aarene-s187": {
        "title": "Fra 1880- til 1890-årene",
        "year_display": "1890-årene",
        "place_ids": ["oslo-sentralstasjon", "grunerlokka-folketeater"],
        "summary": (
            "Inn i 1890-årene vokste elektrisitet, trikk og arbeiderpresse i byen. "
            "Kristiania ble tettere knyttet sammen med industriområder øst og vest for elva."
        ),
    },
    "bind5-fra-kongetogettil-systemskiftetinden-kommunen-s215": {
        "title": "Kongetog og kommuneskifte",
        "year_display": "1890-årene",
        "place_ids": ["slottsplassen", "kommunegaarden-logen"],
        "summary": (
            "Kongetog og festligheter vekslet med krav om nytt kommunestyre. "
            "Byen diskuterte hvordan folkevalgte skulle styre vekst, skatt og byggesaker."
        ),
    },
    "bind5-systemskifteti-teori-og-virkelighet-indtil-utgan-s231": {
        "title": "Systemskifte i kommune",
        "year_display": "til 1896",
        "place_ids": ["kommunegaarden-logen", "gamle-raadhus-torvet"],
        "summary": (
            "Kommunen gikk fra gammelt magistratsstyre til mer moderne folkestyre på 1890-tallet. "
            "Teori og praksis møttes i debatt om budsjett, valg og tjenesteytelser."
        ),
    },
    "bind5-jobbetidenogforutsaetningernefor-denokonomiskog-s247": {
        "title": "Jobbetiden",
        "year_display": "1890-årene",
        "place_ids": ["norges-bank-bankplassen", "youngstorget"],
        "summary": (
            "Banksammenbrudd og spekulasjon preget jobbetiden etter overstrekte investeringer. "
            "Kommunen diskuterte om den skulle bygge arbeiderboliger og hvem som bar ansvaret."
        ),
    },
    "bind5-krisen-og-densettervirkninger-s263": {
        "title": "Krise og ettervirkninger",
        "year_display": "ca. 1899",
        "place_ids": ["youngstorget", "mollergata"],
        "summary": (
            "Økonomisk krise rammet handel, bank og arbeidsmarked i byen. "
            "Aviser og kommunestyre søkte løsninger på arbeidsløshet og svekket tillit til finanslivet."
        ),
    },
    "bind5-kommunenved-utgangenav-detnittendeaarhundrede-s279": {
        "title": "Kommunen ved 1900",
        "year_display": "1899-1900",
        "place_ids": ["pipervika", "kommunegaarden-logen"],
        "summary": (
            "Ved århundreskiftet la kommunen planer for kai, bolig og menighetsgrenser. "
            "Store lån og regulering skulle gjøre Kristiania klar for det nye århundret."
        ),
    },
    "bind5-den-nye-arbeidsdagog-hovedstadenindtil-bjornsons-s353": {
        "title": "Ny arbeidsdag",
        "year_display": "1900-1910",
        "place_ids": ["mollergata", "aker-mek-pipervika"],
        "summary": (
            "Fabrikker, verksteder og fagforeninger endret arbeidsdagen i hovedstaden. "
            "Streik og organisering preget byen til Bjørnsons siste år."
        ),
    },
    "bind5-traek-av-spekulationslivetunderhoikonjunkturen-s433": {
        "title": "Spekulasjon i høykonjunktur",
        "year_display": "før 1914",
        "place_ids": ["norges-bank-bankplassen", "karl-johan-jubileet"],
        "summary": (
            "Høye priser og spekulasjon i eiendom og aksjer fanget byens næringsliv før krigen. "
            "Gevinster og fall skapte både rikdom og bitterhet i gatene rundt Bankplassen."
        ),
    },
    "bind5-stemningerog-forhold-indtil-utgangenav-1918-s455": {
        "title": "Mot slutten av krigen",
        "year_display": "1918",
        "place_ids": ["stortinget", "youngstorget"],
        "summary": (
            "Krigstid, matmangel og politisk mobilisering preget Kristiania mot 1918. "
            "Stemningen i gatene speilet både solidaritet og strid om priser og fred."
        ),
    },
    "bind5-kristiania-kommunegjennemkrigsaarene-477-s492": {
        "title": "Kommunen i krigsårene",
        "year_display": "1914-1918",
        "place_ids": ["kommunegaarden-logen", "gronland-ladested"],
        "summary": (
            "Kommunen måtte holde drift og boligpolitikk i gang under første verdenskrig. "
            "Vedtak om leiegårder og planer rammet tusenvis av familier i byen."
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
    print(f"parafrase remaining: {n} oppdatert")


if __name__ == "__main__":
    main()