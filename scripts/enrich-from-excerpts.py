#!/usr/bin/env python3
"""Patch JSON: sidetall, tekster og stedsfelter etter TOC/utdrag (kjør etter extract-excerpt)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    places_path = ROOT / "data" / "places.json"
    events_path = ROOT / "data" / "events.json"

    places_doc = json.loads(places_path.read_text(encoding="utf-8"))
    events_doc = json.loads(events_path.read_text(encoding="utf-8"))

    events = {e["id"]: e for e in events_doc["events"]}
    places = {p["id"]: p for p in places_doc["places"]}

    event_patches = {
        "sag-og-molle": {
            "source_ref": {
                "bind": 3,
                "pages": "209-226",
                "note": "TOC: Forstæderne; utdrag bind-III-s227-229-handel.md",
            },
            "summary": (
                "Forstæder som Grønland og Sagene var friere for byens kjøbmannsprivilegier. "
                "Husnæring og håndverk langs Akerselva la grunnlag for arbeiderkvarterer ved elva."
            ),
        },
        "manufaktur-myrens": {
            "source_ref": {
                "bind": 3,
                "pages": "227-316",
                "note": "TOC: Handel og skibsfart 1740-1776 (utkast)",
            },
        },
        "arbeiderkultur-akerselva": {
            "source_ref": {
                "bind": 3,
                "pages": "427-452",
                "note": "TOC: Sociale uroligheter 1780- og 1790-årene",
            },
        },
        "hovedstad-1814": {
            "source_ref": {
                "bind": 3,
                "pages": "485-556",
                "note": "TOC: Kristiania i krigsaarene 1807-1814; utdrag s527-532",
            },
            "summary": (
                "Krigsårene 1807-1814 tvang Christiania til å være forsyningsknutepunkt for Østlandet. "
                "Bull beskriver korn, handel og sammenbrudd som bakgrunn for byens rolle da riket formet seg på nytt i 1814."
            ),
        },
        "slotsanlegget-1814": {
            "source_ref": {
                "bind": 3,
                "pages": "485-556",
                "note": "TOC: Krigsaarene og slottskvartalet (utkast)",
            },
        },
        "jubileum-1924": {
            "source_ref": {
                "bind": 5,
                "pages": "513-522",
                "note": "TOC: Kristianias 300-aarsjubilæum; utdrag s513-516",
            },
            "summary": (
                "300-årsjubileet i 1924 sammenlignet byen med 1814: sprukne grenser, bolignød og storbytempo. "
                "Hammer lar milepælen 31. desember markerer både fest og utvidelsesdebatt."
            ),
        },
    }

    place_patches = {
        "oslo-sentralstasjon": {
            "lat": 59.911,
            "lng": 10.7525,
            "standpoint": "Stå på Jernbanetorget mot inngangen til Østbanen. Se spor og bygningsmassen.",
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Oslo_S_train_station.jpg/640px-Oslo_S_train_station.jpg",
                "credit": "Wikimedia Commons",
            },
        },
        "grunerlokka-folketeater": {
            "name": "Folketeateret (Storgata)",
            "lat": 59.9149,
            "lng": 10.7515,
            "standpoint": "Foran Folketeateret: her møttes arbeiderkultur og storbyliv på østkanten.",
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Folketeateret_Oslo.jpg/640px-Folketeateret_Oslo.jpg",
                "credit": "Wikimedia Commons",
            },
            "summary": (
                "Omkring Storgata og Grünerløkka vokste et tett bymiljø fram. Hammer knytter teater, "
                "utfart og arbeiderboliger til Christianias modernisering før jubileumsåret."
            ),
        },
        "karl-johan-jubileet": {
            "lat": 59.9133,
            "lng": 10.7402,
            "standpoint": "Midt på Karl Johans gate mot Slottet. Tenk parader og fest i 1924.",
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
                "credit": "Wikimedia Commons",
            },
        },
        "stortinget": {
            "lat": 59.9139,
            "lng": 10.7376,
            "standpoint": "Lovbakken: se fasaden mot Eidsvolls plass.",
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Stortinget_Oslo.jpg/640px-Stortinget_Oslo.jpg",
                "credit": "Wikimedia Commons",
            },
        },
        "slottsplassen": {
            "lat": 59.9169,
            "lng": 10.7265,
            "standpoint": "Slottsplassen med utsikt mot Slottet og parken.",
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Slottet_i_Oslo.jpg/640px-Slottet_i_Oslo.jpg",
                "credit": "Wikimedia Commons",
            },
        },
        "sagene-loken": {
            "lat": 59.9348,
            "lng": 10.7625,
            "standpoint": "Ved Akerselva ved Sagene bru. Lytt etter fossen og se fabrikkbygg langs elva.",
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
                "credit": "Wikimedia Commons",
            },
        },
        "myrens-verk": {
            "lat": 59.9231,
            "lng": 10.761,
            "standpoint": "Myren-området: gå langs elva mellom gamle verkbygg.",
            "source_ref": {
                "bind": 3,
                "pages": "227-316",
                "note": "TOC: handel og industri (utkast)",
            },
        },
        "honse-lovisas-hus": {
            "lat": 59.9244,
            "lng": 10.7588,
            "standpoint": "Ved Hønse-Lovisas hus på Sandaker. Klassisk motiv langs Akerselva.",
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/H%C3%B8nse-Lovisas_hus.jpg/640px-H%C3%B8nse-Lovisas_hus.jpg",
                "credit": "Wikimedia Commons",
            },
        },
    }

    for eid, patch in event_patches.items():
        if eid in events:
            events[eid].update(patch)

    for pid, patch in place_patches.items():
        if pid in places:
            places[pid].update(patch)

    places_path.write_text(
        json.dumps(places_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    events_path.write_text(
        json.dumps(events_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Enriched places and events from excerpt workflow.")


if __name__ == "__main__":
    main()