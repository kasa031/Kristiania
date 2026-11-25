#!/usr/bin/env bash
# Samme filkrav som Prepare app bundle i static-pages.yml - kjør før push.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
for path in index.html sw.js manifest.webmanifest CNAME css js data icons; do
  if [[ ! -e "$path" ]]; then
    echo "FEIL: mangler $path (kreves av GitHub Pages-workflow)"
    exit 1
  fi
done
echo "check-pages-bundle OK"