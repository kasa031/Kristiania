# Innsamling (bøker i `literature/`)

**For AI:** Les `status.json` før du utvider `data/places.json` eller `data/events.json`.

| Fil | Formål |
|-----|--------|
| [manifest.json](manifest.json) | Hvilket PDF, hvilken TOC, hvilke løyper - og `toc_reviewed` per bind |
| [status.json](status.json) | Autogenerert: hva som mangler, hva du har lov til å gjøre |
| [gaps.json](gaps.json) | Alle JSON-poster med utkast-sidetall |
| [INNSAMLING.md](INNSAMLING.md) | Menneskelesbar tabell (samme innhold som status) |

Oppdater:

```powershell
python scripts/literature-status.py
```

Når du har sjekket TOC mot fysisk bind: sett `"toc_reviewed": true` for bindet i `manifest.json`, og kjør scriptet på nytt.