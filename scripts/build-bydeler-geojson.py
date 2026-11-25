#!/usr/bin/env python3
"""Lag bydeler.geojson fra districts.json bbox."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    districts = json.loads((ROOT / "data" / "districts.json").read_text(encoding="utf-8"))[
        "districts"
    ]
    features = []
    for d in districts:
        min_lat, min_lng, max_lat, max_lng = d["bbox"]
        ring = [
            [min_lng, min_lat],
            [max_lng, min_lat],
            [max_lng, max_lat],
            [min_lng, max_lat],
            [min_lng, min_lat],
        ]
        center_lat = (min_lat + max_lat) / 2
        center_lng = (min_lng + max_lng) / 2
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "id": d["id"],
                    "name": d["name"],
                    "center_lat": round(center_lat, 5),
                    "center_lng": round(center_lng, 5),
                },
                "geometry": {"type": "Polygon", "coordinates": [ring]},
            }
        )
    out = {"type": "FeatureCollection", "features": features}
    path = ROOT / "data" / "bydeler.geojson"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {path} ({len(features)} bydeler)")


if __name__ == "__main__":
    main()