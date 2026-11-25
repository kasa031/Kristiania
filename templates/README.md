# Maler for nytt innhold

Kopier en mal, fyll ut, og legg objektet inn i riktig fil under `data/`.

## Steg for ny gåtur-løype

1. Opprett steder i `data/places.json` (bruk `place-template.json`).
2. Opprett hendelser i `data/events.json` (bruk `event-template.json`). Knytt `place_ids` til steder.
3. Opprett eller utvid episode i `data/episodes.json` med `place_order` i gårekkefølge.
4. Bruk eksisterende `tags` fra `data/tags.json`, eller legg til ny tag der hvis nødvendig.

## Kvalitetssjekk før publisering

- [ ] `lat` / `lng` sjekket på kart (OpenStreetMap)
- [ ] `source_ref` med bind og sidetall fra **dine** bind
- [ ] Sammendrag er parafrasert, ikke langt sitat
- [ ] Minst én hendelse per pin i løypa