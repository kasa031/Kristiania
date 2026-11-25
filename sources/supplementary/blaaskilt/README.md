# Blå skilt (Oslo Byes Vel)

Kilde: [Oslo Byes Vel – Blå skilt i Oslo](https://www.oslobyesvel.no/blaa-skilt-i-oslo) og kartet [viewer.mapme.com/blaaskilt](https://viewer.mapme.com/blaaskilt).

Boka *Blå skilt i Oslo* (2021, 428 skilt) er primærtekst. Appen bruker korte parafraser og `source_ref.pages: supplement`.

## Data

- `seed.tsv` – navn og adresse for import (tab-separert)
- `geocode-cache.json` – Nominatim-cache (ikke commit store diff uten grunn)
- `place-links.json` – kobling blå skilt ↔ eksisterende `places.json`

## Import

```text
python scripts/import-blaaskilt.py
```

Fyller `data/blue-signs.json` og setter `blaa_skilt: true` på koblede steder.

## Status (B11)

- Mål: ~500 skilt (samme som OBV-kartet)
- Appen oppdateres etter hver import-kjøring