# Data for nettsiden

Strukturert innhold lastes av `index.html` via `fetch()`. Alt har `source_ref` (bind + sider) og `verified` (standard `false` til kildegjennomgang).

## Filer

| Fil | Inneholder |
|-----|------------|
| `places.json` | Steder (lat/lng, sammendrag, tags, episode_id) |
| `events.json` | Hendelser (år, sted-kobling, episode_id) |
| `episodes.json` | Gåtur-løyper (`place_order`) |
| `tags.json` | Tema-filter (10 tema i 3 grupper) |
| `eras.json` | Tidsrom for løyper og århundre-filter |
| `bind-sources.json` | Lenker til faksimiler |
| `milestones.json` | Oversikt i header (følger FREMGANG) |
| `site-config.json` | App-visning (kilde/badges av/på) |
| `map-config.json` | Kartlag; token i `map-config.local.json` |
| `schema.json` | JSON-kontrakt |
| `walks/` | Løype-notater (systematikk, kapittelkobling) |

## Oppdateringsrekkefølge

1. TOC i `sources/toc/`
2. Løype-notat i `data/walks/<id>.md`
3. `events.json` / `places.json`
4. `milestones.json` ved milepæl-status