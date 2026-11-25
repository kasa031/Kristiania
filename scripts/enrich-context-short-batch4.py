#!/usr/bin/env python3
"""Utvid korte bind I-V context-sammendrag (A14), batch 4."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "data" / "context.json"

PATCHES: dict[str, str] = {
    "bind1-biskop-eystein-1385-1407-s275": (
        "Biskop Eystein organiserte kirkegårder, sykehus og peterskap i det gamle Oslo og ble "
        "husket som en av de mest virksomme kirkelige byggerne før reformasjonen. Hans tid faller "
        "sammen med at kongemakten på nytt tok bolig på Akershus, mens byen på vanlig vis bar "
        "preg av borgere, handel og trange år når pest og knapphet rammet."
    ),
    "bind1-rostockernei-osloi-det15-aarh-s303": (
        "Kjøpmenn fra Rostock og andre hanseater konkurrerte med lokale borgere om handel ved "
        "Oslo-torvet og kaianleggene. Konfliktene om toll, privilegier og hvem som fikk kjøpe og selge "
        "på torget preget middelalderbyens økonomi lenge før Christian IV la grunnen til nye Kristiania."
    ),
    "bind1-syvaarskrigen-s423": (
        "Under syvårskrigen på 1560-tallet måtte Akershus forsterkes med nye murer og det såkalte "
        "munketårnet. Stein fra nedrevne kirker i gamle Oslo ble brukt i arbeidet, og forsvarsvridet "
        "bandt sammen festning, borg og den krisen kysten sto i mot Sverige og Danmark."
    ),
    "bind2-den-store-toldsvig-403-s416": (
        "En omfattende toljsvindel satte hele Christiania i opprør rundt 1705. Da toldinspektøren og "
        "en embetsmann ble arrestert, hang vrede pasquiler på kirken og gapestokken, og byen levde i "
        "uro mens kommisjonen og generalfiskalen forfulgte saken ved tollboden og i gatene."
    ),
    "bind3-byen-og-oplandet-s103": (
        "De tolv utvalgte kjøpmenn møttes jevnlig fra 1780-årene og talte byens interesser overfor "
        "magistraten og kongen. De diskuterte veier, laug og budsjett, og høsten 1788 reiste de sterkt "
        "mot Bernt Ankers oppkjøp av slakt i Aker fordi det truet forsyningene til byens fattigste."
    ),
    "bind4-menneskerog-forhold-ide-forste-selvstaendighetsa-s27": (
        "Sommeren 1814 kom stormaktiges sendebud til Christiania og bodde blant annet i Collettgården "
        "ved Kirkegata. Forhandlingene med Christian Frederik og ultimatumet 7. juli satte press på "
        "avisene og gatene, mens byen fulgte spørsmålet om union, fred og norsk selvstendighet."
    ),
    "bind4-de-forste-kommunestyrerog-deresgrundsyn-socialto-s227": (
        "Etter formannskapsloven av 1837 fikk Kristiania folkevalgte styremenn med ansvar for skoler, "
        "fattigvesen, veier og økonomi. De første kommunestyrene la grunnlaget for moderne lokalstyre "
        "og skulle balansere mellom byens vekst, fattigdom og nye sosiale krav."
    ),
    "bind5-bryggeforholdog-havnereguleringeromkring-aarhund-s297": (
        "Ved århundreskiftet lånte kommunen tungt for kai-anlegg, havneforlengelser og opplag langs "
        "Pipervika og inn mot sentrum. Debatt om eiendomskjøp, renter og magistratens finansplan preget "
        "hvordan Christiania skulle vinne plass til moderne havne- og jernbanebygg."
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
    print(f"enrich-context-short-batch4: {n} oppdatert")


if __name__ == "__main__":
    main()