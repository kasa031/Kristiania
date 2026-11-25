#!/usr/bin/env python3
"""Forsøk hente Blå skilt-punkter fra Mapme (viewer.mapme.com/blaaskilt)."""
from __future__ import annotations

import json
import re
import urllib.request

URL = "https://viewer.mapme.com/blaaskilt"


def main() -> None:
    html = urllib.request.urlopen(URL, timeout=45).read().decode("utf-8", "replace")
    print("html bytes", len(html))
    for pat in (
        r"https://cdn\.mapme\.com/[^\"'\s]+",
        r"mapId[\"']?\s*:\s*[\"']([^\"']+)",
        r"api[^\"'\s]+blaaskilt[^\"'\s]*",
    ):
        hits = re.findall(pat, html)
        if hits:
            print(pat, hits[:5])
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
    for s in scripts:
        if "latitude" in s or "coordinates" in s or "locations" in s:
            print("script snippet", s[:500])


if __name__ == "__main__":
    main()