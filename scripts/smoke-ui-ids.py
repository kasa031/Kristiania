"""Sjekk at index.html har alle element-ID-er app.js forventer."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

REQUIRED = [
    "map-search-form",
    "map-search",
    "map-search-suggest",
    "map-search-status",
    "btn-map-search",
    "btn-map-locate",
    "map-layer",
    "map-place-count",
    "nearby-wrap",
    "nearby-status",
    "nearby-list",
    "filters-wrap",
    "filters-summary-text",
    "filters-advanced",
    "filter-destination",
    "filter-episode",
    "filter-district",
    "filter-century",
    "filter-tag",
    "filter-chronology",
    "year-min",
    "year-max",
    "btn-reset-filters",
    "detail-panel",
    "timeline-list",
    "walk-bar",
    "walk-progress",
    "walk-prev",
    "walk-next",
    "walk-exit",
    "mode-tab-explore",
    "mode-tab-routes",
    "panel-explore",
    "panel-routes",
    "episode-cards",
    "map",
    "home-screen",
    "home-btn-search",
    "home-btn-routes",
    "masthead-title",
    "btn-back-home",
    "panel-top-nav",
]


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")
    found = set(re.findall(r'\bid="([^"]+)"', html))
    missing = [i for i in REQUIRED if i not in found]
    if missing:
        print("MANGLER ID i index.html:", ", ".join(missing))
        return 1
    print(f"smoke-ui-ids OK ({len(REQUIRED)} id-er)")
    return 0


if __name__ == "__main__":
    sys.exit(main())