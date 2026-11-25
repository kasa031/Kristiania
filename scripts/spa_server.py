#!/usr/bin/env python3
"""Lokal statisk server med SPA-fallback for /home, /kart og /tur."""
from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPA_ROUTES = {"/home", "/kart", "/tur"}


class SpaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in SPA_ROUTES or path.rstrip("/") in SPA_ROUTES:
            qs = ""
            if "?" in self.path:
                qs = "?" + self.path.split("?", 1)[1]
            self.path = "/index.html" + qs
        return super().do_GET()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("", args.port), SpaHandler)
    print(f"Kristiania SPA: http://localhost:{args.port}/home")
  print("Ruter: /home, /kart, /tur  (Ctrl+C avslutter)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAvslutter.")


if __name__ == "__main__":
    main()