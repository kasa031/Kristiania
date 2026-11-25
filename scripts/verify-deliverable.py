#!/usr/bin/env python3
"""Sjekk at leveransen er komplett (kjøres etter endringer og før publisering)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(msg: str) -> None:
    print(f"FEIL: {msg}")
    sys.exit(1)


def main() -> int:
    required = [
        "index.html",
        "js/app.js",
        "css/style.css",
        "data/places.json",
        "data/events.json",
        "data/site-config.json",
        "data/map-config.json",
        "content/FREMGANG.md",
        "manifest.webmanifest",
        "sw.js",
        ".github/workflows/static-pages.yml",
    ]
    for rel in required:
        if not (ROOT / rel).is_file():
            fail(f"mangler fil {rel}")

    cfg = json.loads((ROOT / "data" / "site-config.json").read_text(encoding="utf-8"))
    if cfg.get("primary_mode") != "explore":
        fail("site-config primary_mode skal være explore")

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    if "mode-tab-explore" not in html or "mode-tab-routes" not in html or "nearby-panel" not in html:
        fail("index.html mangler hovedmodus (Se kart / Gå rute)")

    pre = subprocess.call([sys.executable, str(ROOT / "scripts" / "preflight.py")], cwd=ROOT)
    if pre != 0:
        fail("preflight feilet")

    desk = subprocess.call([sys.executable, str(ROOT / "scripts" / "desktop-walk-test.py")], cwd=ROOT)
    if desk != 0:
        fail("desktop-walk-test feilet")

    smoke = subprocess.call([sys.executable, str(ROOT / "scripts" / "smoke-ui-ids.py")], cwd=ROOT)
    if smoke != 0:
        fail("smoke-ui-ids feilet")

    buttons = subprocess.call(
        [sys.executable, str(ROOT / "scripts" / "smoke-ui-buttons-static.py")],
        cwd=ROOT,
    )
    if buttons != 0:
        fail("smoke-ui-buttons-static feilet")

    print("verify-deliverable OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())