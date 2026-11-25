#!/usr/bin/env python3
"""Hent forenklet GeoJSON for Oslo bydeler fra Overpass/OSM."""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bydeler.geojson"

QUERY = """
[out:json][timeout:90];
area["name"="Oslo"]["admin_level"=4]->.searchArea;
(
  relation["boundary"="administrative"]["admin_level"="8"](area.searchArea);
);
out geom;
"""


def relation_to_feature(el: dict) -> dict | None:
    tags = el.get("tags") or {}
    name = tags.get("name")
    if not name:
        return None
    rid = tags.get("name:en") or name
    slug = (
        name.lower()
        .replace("ø", "o")
        .replace("å", "a")
        .replace("æ", "ae")
        .replace(" ", "-")
        .replace("(", "")
        .replace(")", "")
    )
    slug = slug.replace("grunerlokka", "grunerlokka").replace("sondre", "sondre")

    def ring_from_way(nodes: list) -> list:
        coords = []
        for n in nodes:
            if isinstance(n, dict) and "lat" in n and "lon" in n:
                coords.append([n["lon"], n["lat"]])
        return coords

    polygons: list = []
    for mem in el.get("members") or []:
        if mem.get("type") != "way" or mem.get("role") not in ("outer", ""):
            continue
        geom = mem.get("geometry")
        if not geom:
            continue
        ring = ring_from_way(geom)
        if len(ring) >= 4:
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            polygons.append([ring])

    if not polygons:
        return None

    geometry = {"type": "Polygon", "coordinates": polygons[0]} if len(polygons) == 1 else {
        "type": "MultiPolygon",
        "coordinates": polygons,
    }

    lats = [c[1] for poly in (polygons if geometry["type"] == "MultiPolygon" else [polygons[0]]) for ring in poly for c in ring]
    lngs = [c[0] for poly in (polygons if geometry["type"] == "MultiPolygon" else [polygons[0]]) for ring in poly for c in ring]
    center_lat = sum(lats) / len(lats)
    center_lng = sum(lngs) / len(lngs)

    return {
        "type": "Feature",
        "properties": {
            "id": slug,
            "name": name,
            "center_lat": round(center_lat, 5),
            "center_lng": round(center_lng, 5),
        },
        "geometry": geometry,
    }


def main() -> int:
    req = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=urllib.parse.urlencode({"data": QUERY}).encode(),
        method="POST",
        headers={"User-Agent": "OsloHistorieApp/1.0 (educational)"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode())

    features = []
    for el in data.get("elements") or []:
        if el.get("type") != "relation":
            continue
        feat = relation_to_feature(el)
        if feat:
            features.append(feat)

    if not features:
        print("Ingen bydeler fra Overpass", file=sys.stderr)
        return 1

    features.sort(key=lambda f: f["properties"]["name"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({len(features)} bydeler)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())