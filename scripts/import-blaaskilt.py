#!/usr/bin/env python3
"""Importer Blå skilt fra seed.tsv (Nominatim) og koble til places.json."""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "sources" / "supplementary" / "blaaskilt" / "seed.tsv"
CACHE = ROOT / "sources" / "supplementary" / "blaaskilt" / "geocode-cache.json"
LINKS = ROOT / "sources" / "supplementary" / "blaaskilt" / "place-links.json"
OUT = ROOT / "data" / "blue-signs.json"
PLACES = ROOT / "data" / "places.json"
UA = "OsloHistorieKristiania/1.0 (edu project; kontakt via repo)"


def slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return f"blaaskilt-{s[:40]}"


def geocode(address: str, cache: dict) -> tuple[float, float] | None:
    key = address.strip().lower()
    if key in cache:
        return cache[key]
    q = urllib.parse.urlencode({"q": address, "format": "json", "limit": 1, "countrycodes": "no"})
    url = f"https://nominatim.openstreetmap.org/search?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    except OSError:
        return None
    if not data:
        cache[key] = None
        return None
    lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
    cache[key] = [lat, lon]
    time.sleep(1.1)
    return lat, lon


def main() -> None:
    cache = {}
    if CACHE.is_file():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    links_doc = json.loads(LINKS.read_text(encoding="utf-8"))
    link_ids = set(links_doc.get("place_ids") or [])
    places_doc = json.loads(PLACES.read_text(encoding="utf-8"))
    place_by_id = {p["id"]: p for p in places_doc["places"]}
    signs: list[dict] = []
    linked: set[str] = set()

    for line in SEED.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("name\t"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        name, address = parts[0].strip(), parts[1].strip()
        place_id = parts[2].strip() if len(parts) > 2 else ""
        if place_id and place_id in place_by_id:
            link_ids.add(place_id)
            linked.add(place_id)
            continue
        coords = geocode(address, cache)
        if not coords:
            print(f"HOPPER: {name} ({address})")
            continue
        lat, lng = coords
        signs.append(
            {
                "id": slug(name),
                "name": name,
                "address": address,
                "lat": round(lat, 5),
                "lng": round(lng, 5),
                "year_from": 1800,
                "year_to": 1924,
                "tags": ["blaa-skilt", "kultur"],
                "summary": f"Blått skilt fra Oslo Byes Vel ved {address}. Teksten på skiltet forteller kulturhistorie i kortform der den henger.",
                "verified": False,
                "source_ref": {
                    "bind": 5,
                    "pages": "supplement",
                    "note": "Oslo Byes Vel: Blå skilt i Oslo",
                },
                "supplementary_note": "sources/supplementary/blaaskilt/README.md",
                "place_id": None,
            }
        )

    for pid in link_ids:
        p = place_by_id.get(pid)
        if not p:
            print(f"UKJENT place_id: {pid}")
            continue
        p["blaa_skilt"] = True
        tags = list(p.get("tags") or [])
        if "blaa-skilt" not in tags:
            tags.append("blaa-skilt")
        p["tags"] = tags
        if not any(s.get("place_id") == pid for s in signs):
            signs.append(
                {
                    "id": f"blaaskilt-place-{pid}",
                    "name": p["name"],
                    "address": p.get("standpoint") or p["name"],
                    "lat": p["lat"],
                    "lng": p["lng"],
                    "year_from": p.get("year_from"),
                    "year_to": p.get("year_to"),
                    "tags": ["blaa-skilt", "kultur"],
                    "summary": p.get("summary", "")[:320],
                    "verified": False,
                    "source_ref": {
                        "bind": p.get("bind", 5),
                        "pages": "supplement",
                        "note": "Oslo Byes Vel: Blå skilt (koblet kartstopp)",
                    },
                    "place_id": pid,
                    "supplementary_note": "sources/supplementary/blaaskilt/README.md",
                }
            )

    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT.write_text(json.dumps({"signs": signs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PLACES.write_text(json.dumps(places_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"blue-signs: {len(signs)} | blaa_skilt places: {len(link_ids)}")


if __name__ == "__main__":
    main()