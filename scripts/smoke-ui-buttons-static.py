"""Statisk sjekk: faste knapp-ID-er i index.html og at app.js binder dem."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
APP = ROOT / "js" / "app.js"

CLICK_IDS = [
    "home-btn-search",
    "home-btn-routes",
    "btn-back-home",
    "mode-tab-explore",
    "mode-tab-routes",
    "walk-prev",
    "walk-next",
    "walk-exit",
    "btn-map-locate",
    "btn-reset-filters",
]

def app_binds_click(app: str, element_id: str) -> bool:
    if f'"{element_id}")?.addEventListener("click"' in app:
        return True
    if element_id == "btn-map-locate":
        return 'locateBtn.addEventListener("click"' in app
    needle = f'getElementById("{element_id}")'
    idx = app.find(needle)
    if idx < 0:
        return False
    return 'addEventListener("click"' in app[idx : idx + 1200]


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    missing_dom = [i for i in CLICK_IDS if f'id="{i}"' not in html and f"id='{i}'" not in html]
    if missing_dom:
        print("MANGLER knapp-ID i index.html:", ", ".join(missing_dom))
        return 1
    unbound = [i for i in CLICK_IDS if not app_binds_click(app, i)]
    if unbound:
        print("MANGLER click-handler i app.js for:", ", ".join(unbound))
        return 1
    if 'id="btn-map-search"' not in html:
        print("MANGLER btn-map-search")
        return 1
    if 'map-search-form' not in app or "submit" not in app.split("map-search-form")[1][:200]:
        print("MANGLER søk-submit-handler")
        return 1
    print(f"smoke-ui-buttons-static OK ({len(CLICK_IDS)} faste knapper + søk)")
    return 0


if __name__ == "__main__":
    sys.exit(main())