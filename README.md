# Historisk vandringskart - Kristiania

Kart, posisjon og korte historier fra Oslos/Christianias historie. Statisk nettside (HTML, CSS, JSON) - ingen app-butikk.

**Publisert:** [tagoslo.no/home](https://tagoslo.no/home) (når DNS er satt) · speil: `https://kasa031.github.io/Kristiania/home`

## Kjør lokalt (fullt utviklingsrepo)

Hele prosjektet med FREMGANG, kilder og scripts ligger lokalt (ikke på offentlig GitHub). Fra prosjektmappa:

```powershell
.\scripts\serve.ps1
```

Åpne `http://localhost:8080/home`

## Publisering

Dette repoet inneholder **kun app-filer** som deployes med GitHub Actions.

1. Push til `main`.
2. Repo **Settings → Pages → Build: GitHub Actions**.
3. **Custom domain** (valgfritt): `CNAME` i repo + DNS hos registrar.

`literature/`, `content/`, `sources/` og `scripts/` er lokale (gitignore).

## Kart

Standard: OpenStreetMap / Carto (ingen nøkkel). Valgfritt Mapbox lokalt via `data/map-config.local.json` (lokal fil, ikke i git).