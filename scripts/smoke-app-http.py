"""Hent kritiske app-filer over HTTP (kjør mens serve.ps1 kjører)."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

BASE = "http://localhost:8080"
PATHS = [
    "/index.html",
    "/js/app.js",
    "/css/style.css",
    "/css/theme-kristiania.css",
    "/data/places.json",
    "/data/events.json",
    "/data/episodes.json",
    "/data/site-config.json",
    "/sw.js",
]


def main() -> int:
    ok = True
    for path in PATHS:
        url = BASE + path
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                body = resp.read()
                if resp.status != 200:
                    print(f"FEIL {path}: HTTP {resp.status}")
                    ok = False
                    continue
                if path.endswith(".json"):
                    json.loads(body.decode("utf-8"))
                if path == "/index.html":
                    html = body.decode("utf-8", errors="replace")
                    for need in ("mode-tab-explore", "mode-tab-routes", "panel-routes", "walk-bar"):
                        if need not in html:
                            print(f"FEIL index.html mangler {need}")
                            ok = False
                if path == "/js/app.js":
                    js = body.decode("utf-8", errors="replace")
                    for needle in ("setSidePanelMode", "startWalk", "exitWalkMode", "walkRouteBannerHtml"):
                        if needle not in js:
                            print(f"FEIL app.js mangler {needle}")
                            ok = False
                            break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            print(f"FEIL {path}: {e}")
            ok = False
    if ok:
        print(f"smoke-app-http OK ({len(PATHS)} filer, {BASE})")
        return 0
    print("Kjør: .\\scripts\\serve.ps1")
    return 1


if __name__ == "__main__":
    sys.exit(main())