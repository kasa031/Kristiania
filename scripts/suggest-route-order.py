#!/usr/bin/env python3
"""Forslå kortere place_order for en episode (greedy + 2-opt). Kun utviklingshjelp."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def haversine(a: tuple[float, float], b: tuple[float, float]) -> float:
    R = 6371000
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    x = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def route_len(places: dict, order: list[str]) -> float:
    total = 0.0
    for i in range(len(order) - 1):
        a, b = places[order[i]], places[order[i + 1]]
        total += haversine((a["lat"], a["lng"]), (b["lat"], b["lng"]))
    return total


def two_opt(places: dict, path: list[str]) -> tuple[float, list[str]]:
    best = path[:]
    best_d = route_len(places, best)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                rev = best[:i] + best[i : j + 1][::-1] + best[j + 1 :]
                d = route_len(places, rev)
                if d + 1 < best_d:
                    best_d, best = d, rev
                    improved = True
    return best_d, best


def suggest(places: dict, order: list[str], start: str | None, end: str | None) -> tuple[float, list[str], float]:
    cur_km = route_len(places, order) / 1000
    if start and end:
        mid = [x for x in order if x not in (start, end)]
        path = [start]
        cur = start
        while mid:
            nxt = min(
                mid,
                key=lambda n: haversine(
                    (places[cur]["lat"], places[cur]["lng"]),
                    (places[n]["lat"], places[n]["lng"]),
                ),
            )
            path.append(nxt)
            mid.remove(nxt)
            cur = nxt
        path.append(end)
    else:
        start_id = start or order[0]
        mid = [x for x in order if x != start_id]
        path = [start_id]
        cur = start_id
        while mid:
            nxt = min(
                mid,
                key=lambda n: haversine(
                    (places[cur]["lat"], places[cur]["lng"]),
                    (places[n]["lat"], places[n]["lng"]),
                ),
            )
            path.append(nxt)
            mid.remove(nxt)
            cur = nxt
    new_d, new_order = two_opt(places, path)
    return cur_km, new_order, new_d / 1000


def main() -> int:
    if len(sys.argv) < 2:
        print("Bruk: python scripts/suggest-route-order.py <episode-id> [start-id] [end-id]")
        return 1
    ep_id = sys.argv[1]
    start = sys.argv[2] if len(sys.argv) > 2 else None
    end = sys.argv[3] if len(sys.argv) > 3 else None
    places = {
        p["id"]: p for p in json.loads((ROOT / "data" / "places.json").read_text(encoding="utf-8"))["places"]
    }
    ep = next(
        e
        for e in json.loads((ROOT / "data" / "episodes.json").read_text(encoding="utf-8"))["episodes"]
        if e["id"] == ep_id
    )
    order = ep["place_order"]
    cur, proposed, km = suggest(places, order, start, end)
    print(f"{ep['title']}: {cur:.2f} km -> {km:.2f} km")
    print("Forslag:")
    for pid in proposed:
        print(f"  {pid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())