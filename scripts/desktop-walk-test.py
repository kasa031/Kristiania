#!/usr/bin/env python3
"""Desktop-validering av løyper, avstander og koordinater (erstatter feltgåtur i utviklingsfase)."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "DESKTOP-TEST.md"
WALK_SPEED_KM_H = 4.8
DWELL_MIN_PER_STOP = 5


def haversine(a: tuple[float, float], b: tuple[float, float]) -> float:
    R = 6371000
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    x = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def coord_ok(lat: float | None, lng: float | None) -> bool:
    if lat is None or lng is None:
        return False
    return 59.85 <= lat <= 60.05 and 10.6 <= lng <= 10.95


def main() -> None:
    places = {p["id"]: p for p in json.loads((ROOT / "data/places.json").read_text(encoding="utf-8"))["places"]}
    episodes = json.loads((ROOT / "data/episodes.json").read_text(encoding="utf-8"))["episodes"]

    lines = [
        "# Desktop-test (autogenerert)",
        "",
        f"Kjør på nytt: `python scripts/desktop-walk-test.py`",
        "",
        "## Løyper",
        "",
        "| Løype | Stopp | Gangavstand (ca.) | Tid (ca.) | Merknad |",
        "|-------|------:|------------------:|----------:|---------|",
    ]

    issues: list[str] = []

    for ep in episodes:
        order = ep.get("place_order") or []
        if len(order) < 2:
            lines.append(f"| {ep['title']} | {len(order)} | - | - | for få stopp |")
            continue
        dist = 0.0
        for i in range(len(order) - 1):
            a, b = places[order[i]], places[order[i + 1]]
            if not a or not b:
                issues.append(f"Mangler sted i {ep['id']}: {order[i]} eller {order[i+1]}")
                continue
            dist += haversine((a["lat"], a["lng"]), (b["lat"], b["lng"]))
        km = dist / 1000
        walk_min = (km / WALK_SPEED_KM_H) * 60
        total_min = walk_min + len(order) * DWELL_MIN_PER_STOP
        if total_min < 60:
            time_s = f"{round(total_min)} min"
        else:
            h = int(total_min // 60)
            m = int(round(total_min % 60))
            time_s = f"{h} t {m} min" if m else f"{h} t"
        note = "OK" if km < 9 else "lang rute - vurder rekkefølge"
        if km > 9:
            issues.append(f"{ep['id']}: {km:.1f} km mellom stopp")
        lines.append(f"| {ep['title']} | {len(order)} | {km:.1f} km | {time_s} | {note} |")

    lines.extend(["", "## Steder", ""])
    for p in places.values():
        sp = "ja" if p.get("standpoint") else "nei"
        coord_st = "ja" if coord_ok(p.get("lat"), p.get("lng")) else "nei"
        if coord_st == "nei":
            issues.append(f"Koordinat utenfor Oslo: {p['id']}")
        lines.append(f"- **{p['name']}** (`{p['id']}`): standpoint {sp}, koordinat {coord_st}")

    if issues:
        lines.extend(["", "## Avvik", ""])
        for i in issues:
            lines.append(f"- {i}")
    else:
        lines.extend(["", "Ingen avvik funnet.", ""])

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(issues)} issues)")


if __name__ == "__main__":
    main()