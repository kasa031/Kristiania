#!/usr/bin/env python3
"""Utvid siste korte bind IV-V context-sammendrag (A14)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, str] = {
    "bind1-bispeneanders-mus-hansmule-og-hansraev-1505-37-s349": (
        "Reformasjonstiden rammet bispeborgen og geistlig makt i Oslo. Biskop Anders Mus, Hans Mule "
        "og Hans Raef måtte forvalte kirken og gods i en by der nye læresetninger og politisk press "
        "endret rollen deres etter at middelalderens strukturer brøt sammen."
    ),
    "bind4-socialeog-kulturelle-nydannelseri-1840-aarene-s277": (
        "På 1840-tallet vokste foreninger, leseselskap og nye idéer frem i hovedstaden. Sammen med "
        "utdanning og avisliv dannet de et bymiljø der borgerskap og arbeidere møttes om kultur, "
        "frivillighet og krav om mer medbestemmelse."
    ),
    "bind4-tanke-og-folelseslivfra-wergelandsdodtil-gjennem-s313": (
        "Fra Wergelands død og utover midten av 1800-tallet skiftet stemninger i byen. Romantikk, "
        "nasjonalfølelse og moralsk debatt ble båret av aviser, foredrag og gatekultur, og satte "
        "preg på hvordan folk forsto Kristiania som unionshovedstad."
    ),
    "bind4-hoikonjunktur-og-formuer-s387": (
        "Høykonjunktur og kapitalformuer på slutten av 1800-tallet forsterket klasseforskjeller i "
        "Christiania. Store villastrøk og luksus stod side om side med trange arbeiderkvarterer, "
        "og debatten om formue, skatt og anstendighet ble stadig tydeligere i byens offentlige liv."
    ),
    "bind4-det-storetidsskifte-s539": (
        "Årtusenskiftet og tiden rundt 1900 bar preg av elektrisitet, ny teknikk og urban vekst. "
        "Byen investerte i infrastruktur, transport og kulturbygg, og mange opplevde at Christiania "
        "gikk inn i en ny storbyfase før navneskiftet til Oslo."
    ),
    "bind5-forhold-og-begivenhetersidsti-otti-aarene-s169": (
        "På 1880-tallet sto byen mellom liberal fremgang og sosial uro. Arbeidskonflikter, nye "
        "organisasjoner og politiske skiftninger gjorde gatebildet mer krevende, samtidig som "
        "magistraten og staten måtte finne svar på vekst og misnøye."
    ),
    "bind5-fra-otti-ind-i-nitti-aarene-s187": (
        "Fra 1880-årene og inn i 1890-årene ble tempoet i byutviklingen høyere. Boligpress, "
        "teknisk modernisering og utvidet kommunal virksomhet hele tiden nye temaer i rådhuset, "
        "avisene og på arbeidsplassene."
    ),
    "bind5-fra-kongetogettil-systemskiftetinden-kommunen-s215": (
        "Kong Haakon og dronning Mauds ankomst i 1905 markerte et nytt politisk kapittel. Samtidig "
        "diskuterte byen radikalt systemskifte i kommunen, der skille mellom byråkrati og politikk "
        "ble et sentralt spørsmål for demokratisering og effektiv forvaltning."
    ),
    "bind5-systemskifteti-teori-og-virkelighet-indtil-utgan-s231": (
        "Ideene om et rent byråkratisk systemskifte møtte motstand og tilpasning i praksis. "
        "Kristiania forsøkte å hente inn profesjonell styring i kommunen uten å miste politisk "
        "kontroll, og debatten varte til neste tiårs skifte i lokaladministrasjonen."
    ),
    "bind5-krisen-og-densettervirkninger-s263": (
        "Etter økonomisk krise på slutten av 1890-tallet måtte byen stramme inn og ta stilling til "
        "arbeidsledighet, fattigdom og svekket skatteinntekt. Krisen satte spor i boligmarkedet, "
        "veldedighet og i tilliten mellom styre og befolkning."
    ),
    "bind5-kommunenved-utgangenav-detnittendeaarhundrede-s279": (
        "Ved 1900 sto kommunen foran elektrifisering, sanitæranlegg og stor utvidelse av offentlige "
        "tjenester. Christiania investerte i fremtiden samtidig som gamle privilegier og et statsleg "
        "preg fortsatt preget hvordan byen ble styrt."
    ),
    "bind5-nedgangsaareneog-folgerneav-demi-slutten-avunion-s313": (
        "Nedgangstiden før unionsoppløsningen rammet næringsliv og kommuneøkonomi. Spørsmål om "
        "arbeid, forsvar og nasjonal politikk ble koblet til hverdagslivet i byen, der presset mot "
        "endring ble sterkere mot slutten av unionen med Sverige."
    ),
    "bind5-kristiania-kommunegjennemkrigsaarene-477-s492": (
        "Under første verdenskrig måtte Christiania håndtere knapphet, mangel og økt statlig inngripen. "
        "Gatekøer, rasjonering og nye krav til planlegging stod på dagordenen mens byen ventet på "
        "fred og det jubileumsåret som fulgte etterpå."
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
    print(f"enrich-context-short-batch5: {n} oppdatert")


if __name__ == "__main__":
    main()