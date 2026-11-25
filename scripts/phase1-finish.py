"""Fase 1: fullfør løyper bind I-V, steder og hendelser."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

places = json.loads((ROOT / "data/places.json").read_text(encoding="utf-8"))
events = json.loads((ROOT / "data/events.json").read_text(encoding="utf-8"))
milestones = json.loads((ROOT / "data/milestones.json").read_text(encoding="utf-8"))
episodes = json.loads((ROOT / "data/episodes.json").read_text(encoding="utf-8"))

new_places = [
    {
        "id": "oslo-sentralstasjon",
        "name": "Oslo sentralstasjon (østbanen)",
        "lat": 59.9112,
        "lng": 10.7524,
        "bind": 4,
        "year_from": 1854,
        "year_to": 1924,
        "tags": ["havn", "bygrunn"],
        "episode_id": "mot-1924",
        "related_events": ["jernbanen-1854", "christiania-vokser-elva"],
        "related_people": [],
        "summary": "Jernbanen knyttet Christiania til riket og utlandet. Hammer beskriver hvordan transportårer forandret byens tempo og utbredelse.",
        "verified": False,
        "source_ref": {"bind": 4, "pages": "349-380", "note": "Bind IV: jernbane og telegraf kap."},
        "external_links": [],
    },
    {
        "id": "grunerlokka-folketeater",
        "name": "Grünerløkka (storbykvarter)",
        "lat": 59.9228,
        "lng": 10.7589,
        "bind": 5,
        "year_from": 1878,
        "year_to": 1924,
        "tags": ["bygrunn", "kommune"],
        "episode_id": "mot-1924",
        "related_events": ["byutvidelse-1878", "arbeiderkultur-1890"],
        "related_people": [],
        "summary": "Østkanten vokste fram med arbeiderboliger og næring. Hammer i bind V følger storbyvekst, utfart og sosiale brytninger i 1880- og 1890-årene.",
        "verified": False,
        "source_ref": {"bind": 5, "pages": "99-132", "note": "Bind V: storbyvekst og 1880-årene"},
        "external_links": [],
    },
    {
        "id": "karl-johan-jubileet",
        "name": "Karl Johans gate (jubileumsåret 1924)",
        "lat": 59.9143,
        "lng": 10.7395,
        "bind": 5,
        "year_from": 1900,
        "year_to": 1924,
        "tags": ["kultur", "kommune"],
        "episode_id": "mot-1924",
        "related_events": ["jubileum-1924"],
        "related_people": [],
        "summary": "300-årsjubileet for Christiania i 1924 var kulminasjonen på bind V. Hammer skildrer fest, minner og byens moderne selvbilde.",
        "verified": False,
        "source_ref": {"bind": 5, "pages": "413-432", "note": "Bind V: jubileumsåret"},
        "external_links": [],
    },
]

ids = {p["id"] for p in places["places"]}
for np in new_places:
    if np["id"] not in ids:
        places["places"].append(np)

place_up = {
    "sagene-loken": ("209-226", 3, "Bind III: forstæderne"),
    "honse-lovisas-hus": ("1-34", 3, "Bind III: bebyggelse"),
    "bentsebru": ("103-158", 3, "Bind III: byen og oplandet"),
    "myrens-verk": ("227-316", 3, "Bind III: handel 1740-1776"),
    "hollaenderbrua": ("209-226", 3, "Bind III: forstæder"),
    "akerselva-utløp": ("135-140", 2, "Bind II: havnen"),
    "slottsplassen": ("485-556", 3, "Bind III: krigsaarene 1807-1814"),
    "stortinget": ("1-26", 4, "Bind IV: grunnlovsaaret 1814"),
    "universitetsplassen": ("125-140", 4, "Bind IV: vekst i kultur"),
    "domkirken-oslo": ("205-208", 3, "Bind III: religiøse forhold"),
}
for p in places["places"]:
    if p["id"] in place_up:
        pages, bind, note = place_up[p["id"]]
        p["source_ref"] = {"bind": bind, "pages": pages, "note": note}

new_events = [
    {
        "id": "jernbanen-1854",
        "title": "Jernbanen til Christiania",
        "year": 1854,
        "year_display": "1854",
        "bind": 4,
        "tags": ["havn", "bygrunn"],
        "episode_id": "mot-1924",
        "place_ids": ["oslo-sentralstasjon", "akerselva-utløp"],
        "summary": "Banen gjorde Christiania til knutepunkt. Hammer beskriver jernbane og telegraf som bærere av storbytid.",
        "verified": False,
        "source_ref": {"bind": 4, "pages": "349-380", "note": "Bind IV kap. jernbane"},
    },
    {
        "id": "byutvidelse-1878",
        "title": "Byutvidelsen 1878",
        "year": 1878,
        "year_display": "1878",
        "bind": 5,
        "tags": ["bygrunn", "kommune"],
        "episode_id": "mot-1924",
        "place_ids": ["grunerlokka-folketeater"],
        "summary": "Utvidelsen økte arealet og befolkningen kraftig. Hammer åpner bind V med kommunenes økonomiske utfordringer.",
        "verified": False,
        "source_ref": {"bind": 5, "pages": "1-18", "note": "Bind V: byutvidelsen"},
    },
    {
        "id": "arbeiderkultur-1890",
        "title": "Arbeiderkultur og storby",
        "year": 1890,
        "year_display": "1880-1890-årene",
        "bind": 5,
        "tags": ["kommune"],
        "episode_id": "mot-1924",
        "place_ids": ["grunerlokka-folketeater"],
        "summary": "Arbeiderfamilier samlet seg lengre øst. Hammer beskriver boligkøer, fagorganisering og kulturliv i en hastigt voksende by.",
        "verified": False,
        "source_ref": {"bind": 5, "pages": "19-34", "note": "Bind V: arbeiderbefolkningen"},
    },
    {
        "id": "jubileum-1924",
        "title": "300-årsjubileet for Christiania",
        "year": 1924,
        "year_display": "1924",
        "bind": 5,
        "tags": ["kultur", "kommune"],
        "episode_id": "mot-1924",
        "place_ids": ["karl-johan-jubileet", "slottsplassen"],
        "summary": "Jubileet feiret grunnleggelsen i 1624 og avsluttet verkets kronologi. Hammer skildrer paradefester og historiske utstillinger.",
        "verified": False,
        "source_ref": {"bind": 5, "pages": "413-432", "note": "Bind V: jubileumsåret"},
    },
]
eids = {e["id"] for e in events["events"]}
for ne in new_events:
    if ne["id"] not in eids:
        events["events"].append(ne)

events["events"].sort(key=lambda x: (x["year"], x["id"]))

for ep in episodes["episodes"]:
    if ep["id"] == "mot-1924":
        ep["place_order"] = [
            "stortinget",
            "oslo-sentralstasjon",
            "grunerlokka-folketeater",
            "karl-johan-jubileet",
            "slottsplassen",
        ]
        ep["description"] = (
            "Fra unionshovedstad via jernbane og arbeiderkvarter til jubileumsåret 1924 - Hammer bind IV-V."
        )

for m in milestones["milestones"]:
    if m["id"] == "jernbanen-1854":
        m["status"] = "utkast"
        m["event_id"] = "jernbanen-1854"
    if m["id"] == "jubileum-1924":
        m["status"] = "utkast"
        m["event_id"] = "jubileum-1924"

(ROOT / "data/places.json").write_text(json.dumps(places, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "data/events.json").write_text(json.dumps(events, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "data/episodes.json").write_text(json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "data/milestones.json").write_text(json.dumps(milestones, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK", len(places["places"]), "places", len(events["events"]), "events")