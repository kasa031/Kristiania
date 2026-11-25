#!/usr/bin/env python3
"""Kartminiatyr per sted (OSM) - fungerer uten eksterne bilde-URL-problemer."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def thumb(lat: float, lng: float) -> dict:
    q = quote(f"center={lat},{lng}&zoom=16&size=640x280&markers={lat},{lng},red-pushpin", safe=",=")
    return {
        "url": f"https://staticmap.openstreetmap.de/staticmap.php?{q}",
        "credit": "OpenStreetMap",
    }


def main() -> None:
    path = ROOT / "data" / "places.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    for p in doc["places"]:
        p["image"] = thumb(p["lat"], p["lng"])
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Set map thumbnails for {len(doc['places'])} places.")


if __name__ == "__main__":
    main()