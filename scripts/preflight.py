#!/usr/bin/env python3
"""En kommando for deg og AI for arbeidsstart: innsamling, data-validering, tall."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_literature_status() -> int:
    script = ROOT / "scripts" / "literature-status.py"
    print("=== literature-status ===")
    return subprocess.call([sys.executable, str(script)], cwd=ROOT)


def validate_data() -> bool:
    print("=== data-validering ===")
    places = json.loads((ROOT / "data" / "places.json").read_text(encoding="utf-8"))["places"]
    events = json.loads((ROOT / "data" / "events.json").read_text(encoding="utf-8"))["events"]
    episodes = json.loads((ROOT / "data" / "episodes.json").read_text(encoding="utf-8"))["episodes"]
    place_ids = {p["id"] for p in places}
    event_ids = {e["id"] for e in events}
    ok = True

    for ep in episodes:
        for pid in ep.get("place_order") or []:
            if pid not in place_ids:
                print(f"FEIL: episode {ep['id']} place_order ukjent sted {pid}")
                ok = False
        for pid in ep.get("map_place_order") or []:
            if pid not in place_ids:
                print(f"FEIL: episode {ep['id']} map_place_order ukjent sted {pid}")
                ok = False

    for e in events:
        for pid in e.get("place_ids") or []:
            if pid not in place_ids:
                print(f"FEIL: event {e['id']} peker på ukjent sted {pid}")
                ok = False

    dup_place = len(place_ids) != len(places)
    dup_event = len(event_ids) != len(events)
    if dup_place:
        print("FEIL: duplikat id i places.json")
        ok = False
    if dup_event:
        print("FEIL: duplikat id i events.json")
        ok = False

    author_voice = []
    author_pat = re.compile(
        r"\bBull\b|\bBulls\b|Bull og Hammer|i Bulls\b|\bHammer i bind|\bHammer (?:beskriver|skildrer)",
        re.I,
    )
    for x in places + events:
        sm = x.get("summary", "") or ""
        if author_pat.search(sm):
            author_voice.append(x["id"])
    if author_voice:
        print(f"ADVARSEL: forfatter-stemme i summary (app): {', '.join(author_voice[:8])}")
        if len(author_voice) > 8:
            print(f"  ... og {len(author_voice) - 8} til")
        print("  Kjør: python scripts/normalize-reader-text.py")

    missing_src = [
        x["id"]
        for x in places + events
        if not (x.get("source_ref") or {}).get("pages")
    ]
    if missing_src:
        print(f"ADVARSEL: mangler source_ref.pages: {', '.join(missing_src[:8])}")
        if len(missing_src) > 8:
            print(f"  ... og {len(missing_src) - 8} til")

    district_path = ROOT / "data" / "districts.json"
    finds_path = ROOT / "data" / "finds.json"
    if district_path.is_file() and finds_path.is_file():
        districts = {
            d["id"] for d in json.loads(district_path.read_text(encoding="utf-8")).get("districts", [])
        }
        for f in json.loads(finds_path.read_text(encoding="utf-8")).get("finds", []):
            if f.get("district_id") not in districts:
                print(f"FEIL: find {f.get('id')} ukjent district_id")
                ok = False

    people_path = ROOT / "data" / "people.json"
    context_path = ROOT / "data" / "context.json"
    people = []
    if people_path.is_file():
        people = json.loads(people_path.read_text(encoding="utf-8")).get("people", [])
        people_ids = {p["id"] for p in people}
        for p in people:
            for pid in p.get("place_ids") or []:
                if pid not in place_ids:
                    print(f"FEIL: person {p.get('id')} peker på ukjent sted {pid}")
                    ok = False
        for pl in places:
            for ref in pl.get("related_people") or []:
                if ref in people_ids:
                    continue
                if not any(x["id"] == ref or x.get("name") == ref for x in people):
                    pass
    ctx_n = 0
    if context_path.is_file():
        for c in json.loads(context_path.read_text(encoding="utf-8")).get("entries", []):
            ctx_n += 1
            for pid in c.get("place_ids") or []:
                if pid not in place_ids:
                    print(f"FEIL: context {c.get('id')} peker på ukjent sted {pid}")
                    ok = False

    active_eps = sum(1 for e in episodes if e.get("place_order"))
    find_n = 0
    if finds_path.is_file():
        find_n = len(json.loads(finds_path.read_text(encoding="utf-8")).get("finds", []))
    blue_n = 0
    blue_path = ROOT / "data" / "blue-signs.json"
    if blue_path.is_file():
        for sign in json.loads(blue_path.read_text(encoding="utf-8")).get("signs", []):
            blue_n += 1
            pid = sign.get("place_id")
            if pid and pid not in place_ids:
                print(f"FEIL: blue-sign {sign.get('id')} peker på ukjent sted {pid}")
                ok = False
    print(
        f"OK tall: {len(places)} steder, {len(events)} hendelser, {find_n} funn, "
        f"{len(people)} personer, {ctx_n} bakgrunn, {blue_n} blaa-skilt, {active_eps} aktive løyper",
    )
    return ok


def main() -> int:
    code = run_literature_status()
    data_ok = validate_data()
    status = json.loads((ROOT / "sources" / "innsamling" / "status.json").read_text(encoding="utf-8"))
    s = status["summary"]
    print("=== oppsummering ===")
    print(f"PDF {s['pdfs_on_disk']}/{s['pdfs_expected']} | draft sidetall {s['draft_refs_total']}")
    print(f"Prioritet bind for sidetall: {s.get('priority_bind_for_page_work')}")
    if not data_ok:
        print("Preflight: data-feil - reparer før du publiserer eller utvider.")
        return 1
    if code != 0:
        return code
    print("Preflight OK. Start nettside: .\\scripts\\serve.ps1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())