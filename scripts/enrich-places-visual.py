#!/usr/bin/env python3
"""Fyll standpoint og finjusterte koordinater for alle steder (visuelt = minikart i appen)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Legacy PATCHES may list image; applied fields exclude image (minikart i appen).
WIKI = "https://upload.wikimedia.org/wikipedia/commons/thumb"

PATCHES: dict[str, dict] = {
    "klemenskirken": {
        "lat": 59.9054,
        "lng": 10.7668,
        "standpoint": "Middelalderparken ved ruinene. Se retning mot fjorden og Akershus.",
        "image": {
            "url": f"{WIKI}/8/8d/Klemenskirken_Oslo.JPG/640px-Klemenskirken_Oslo.JPG",
            "credit": "Wikimedia Commons",
        },
    },
    "mariakirken-spor": {
        "lat": 59.9048,
        "lng": 10.7682,
        "standpoint": "I parken der Mariakirkens grunnmur er markert.",
        "image": {"url": f"{WIKI}/2/2e/Middelalderparken_Oslo.jpg/640px-Middelalderparken_Oslo.jpg", "credit": "Wikimedia Commons"},
    },
    "middelalderparken": {
        "lat": 59.9043,
        "lng": 10.7685,
        "standpoint": "Sti mellom ruinene. Her møtes kirker, gravrider og elvebredd.",
        "image": {"url": f"{WIKI}/2/2e/Middelalderparken_Oslo.jpg/640px-Middelalderparken_Oslo.jpg", "credit": "Wikimedia Commons"},
    },
    "bispegarden": {
        "lat": 59.9058,
        "lng": 10.7672,
        "standpoint": "Bispeallmenningen ved Bispegata. Tenk bispens makt i middelalderbyen.",
        "image": {"url": f"{WIKI}/2/2e/Middelalderparken_Oslo.jpg/640px-Middelalderparken_Oslo.jpg", "credit": "Wikimedia Commons"},
    },
    "domkirken-gamlebyen": {
        "lat": 59.9067,
        "lng": 10.766,
        "standpoint": "Oslo domkirke (Gamlebyen). Utsikt mot Akerselva og fjorden.",
        "image": {"url": f"{WIKI}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg", "credit": "Wikimedia Commons"},
    },
    "vippetangen-hovedoya": {
        "lat": 59.9025,
        "lng": 10.7405,
        "standpoint": "Vippetangen mot bryggene og Inner Oslofjord.",
        "image": {"url": f"{WIKI}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg", "credit": "Wikimedia Commons"},
    },
    "skjellebekk-gamlebyen": {
        "lat": 59.9035,
        "lng": 10.7698,
        "standpoint": "Skjellebekk ved Akerselva utløp. Hør vannet mot Gamlebyen.",
        "image": {"url": f"{WIKI}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg", "credit": "Wikimedia Commons"},
    },
    "akershus": {
        "lat": 59.9075,
        "lng": 10.7367,
        "standpoint": "Festningsplassen foran Akershus. Slottskvartalet og fjorden i ett blikk.",
        "image": {"url": f"{WIKI}/a/a9/Akershus_Festning_Oslo.jpg/640px-Akershus_Festning_Oslo.jpg", "credit": "Wikimedia Commons"},
    },
    "kontraskjerp": {
        "lat": 59.9088,
        "lng": 10.7389,
        "standpoint": "Kontraskjerp på Akershus. Utsikt mot Pipervika og havnen.",
        "image": {"url": f"{WIKI}/a/a9/Akershus_Festning_Oslo.jpg/640px-Akershus_Festning_Oslo.jpg", "credit": "Wikimedia Commons"},
    },
    "christiania-torv": {
        "lat": 59.9112,
        "lng": 10.7435,
        "standpoint": "Christiania torv ved Kvadraturen. Se planlagte gater og torg.",
        "image": {"url": f"{WIKI}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg", "credit": "Wikimedia Commons"},
    },
    "gammeltorvet": {
        "lat": 59.9105,
        "lng": 10.7455,
        "standpoint": "Gammeltorvet. Handel og liv i det tidlige Christiania.",
        "image": {"url": f"{WIKI}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg", "credit": "Wikimedia Commons"},
    },
    "vor-frelsers": {
        "lat": 59.9126,
        "lng": 10.7469,
        "standpoint": "Vor Frelsers kirke (Oslo domkirke). Spir i bybildet fra 1600-tallet.",
        "image": {"url": f"{WIKI}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg", "credit": "Wikimedia Commons"},
    },
    "kirkeristen": {
        "lat": 59.9121,
        "lng": 10.7478,
        "standpoint": "Kirkeristen langs domkirken. Nærhet mellom gravplass og handel.",
        "image": {"url": f"{WIKI}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg", "credit": "Wikimedia Commons"},
    },
    "tukthuset": {
        "lat": 59.9133,
        "lng": 10.7492,
        "standpoint": "Tukthusområdet i Kvadraturen. Institution og moral i planbyen.",
        "image": {"url": f"{WIKI}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg", "credit": "Wikimedia Commons"},
    },
    "pipervika": {
        "lat": 59.9098,
        "lng": 10.7345,
        "standpoint": "Pipervika mot fjorden. Skipsfart og arbeid ved brygga.",
        "image": {"url": f"{WIKI}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg", "credit": "Wikimedia Commons"},
    },
    "bentsebru": {
        "lat": 59.9265,
        "lng": 10.7575,
        "standpoint": "Bentse bru over Akerselva. Bro mellom verk og boligkvarter.",
        "image": {"url": f"{WIKI}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg", "credit": "Wikimedia Commons"},
    },
    "hollaenderbrua": {
        "lat": 59.9218,
        "lng": 10.7595,
        "standpoint": "Hollenderbrua. Fabrikklandskap langs elva.",
        "image": {"url": f"{WIKI}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg", "credit": "Wikimedia Commons"},
    },
    "akerselva-utløp": {
        "lat": 59.9078,
        "lng": 10.7532,
        "standpoint": "Der Akerselva munner i fjorden ved Vaterland.",
        "image": {"url": f"{WIKI}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg", "credit": "Wikimedia Commons"},
    },
    "universitetsplassen": {
        "lat": 59.9198,
        "lng": 10.7324,
        "standpoint": "Universitetsplassen foran Gamle festsal. Embetskultur og vitenskap.",
        "image": {"url": f"{WIKI}/1/1a/Universitetet_i_Oslo.jpg/640px-Universitetet_i_Oslo.jpg", "credit": "Wikimedia Commons"},
    },
    "domkirken-oslo": {
        "lat": 59.9126,
        "lng": 10.7469,
        "standpoint": "Oslo domkirke (Vor Frelsers). Pilegrimspunkt mellom slottskvartal og universitet.",
        "image": {"url": f"{WIKI}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg", "credit": "Wikimedia Commons"},
    },
    "myrens-verk": {
        "image": {"url": f"{WIKI}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg", "credit": "Wikimedia Commons"},
    },
}


def main() -> None:
    path = ROOT / "data" / "places.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in doc["places"]}
    n = 0
    for pid, patch in PATCHES.items():
        if pid in by_id:
            patch = {k: v for k, v in patch.items() if k != "image"}
            by_id[pid].update(patch)
            n += 1
    for p in doc["places"]:
        p.pop("image", None)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {n} places with visual/position data.")


if __name__ == "__main__":
    main()