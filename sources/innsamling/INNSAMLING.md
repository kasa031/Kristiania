# Innsamling - bind I-V

*Autogenerert 2026-11-25T19:10:20Z. Kjør på nytt: `python scripts/literature-status.py`.*

Dette er **kilde-/boksporing** (supplement til [FREMGANG.md](../../content/FREMGANG.md)), ikke en parallel oppgaveliste.

## Kan AI utvide JSON nå?

| Bind | PDF | TOC | TOC sjekket | Draft sidetall | Nytt innhold OK? |
|------|:---:|:---:|:-----------:|:--------------:|:----------------:|
| I | ja | ja | nei | 0 | ja |
| II | ja | ja | nei | 0 | ja |
| III | ja | ja | nei | 0 | ja |
| IV | ja | ja | nei | 0 | ja |
| V | ja | ja | nei | 0 | ja |

**Prioritet for sidetall-arbeid:** bind -

## Neste steg per bind

### Bind I - Oslos historie
Løyper: middelalder-oslo, 1624-ny-by
- Sammenlign TOC med fysisk bind; sett toc_reviewed i manifest.json
- Sluttkontroll: verified mot bind (etter feltgatur)

### Bind II - Kristiania 1624-1740
Løyper: 1624-ny-by, kvadraturen-1600, akerselva-tidlig
- Sammenlign TOC med fysisk bind; sett toc_reviewed i manifest.json
- Sluttkontroll: verified mot bind (etter feltgatur)

### Bind III - Kristiania 1740-1814
Løyper: akerselva-tidlig, 1814-hovedstaden
- Sammenlign TOC med fysisk bind; sett toc_reviewed i manifest.json
- Sluttkontroll: verified mot bind (etter feltgatur)

### Bind IV - Kristiania 1814-1877
Løyper: 1814-hovedstaden, mot-1924
- Sammenlign TOC med fysisk bind; sett toc_reviewed i manifest.json
- Sluttkontroll: verified mot bind (etter feltgatur)

### Bind V - Kristiania 1878-1924
Løyper: mot-1924
- Sammenlign TOC med fysisk bind; sett toc_reviewed i manifest.json
- Sluttkontroll: verified mot bind (etter feltgatur)

## Filer

| Fil | Rolle |
|-----|--------|
| [manifest.json](manifest.json) | Forventninger, pdf-navn, `toc_reviewed` (du/AI) |
| [status.json](status.json) | Maskinlesbar status (AI leser denne) |
| [gaps.json](gaps.json) | Lister over draft `source_ref` |
| `literature/*.pdf` | Lokale boker (gitignorert) |
| [sources/toc/](../toc/) | Innholdsfortegnelser |
| [sources/excerpts/](../excerpts/) | Korte utdrag ved behov |
