# Historisk vandringskart - Kristiania

Kart, posisjon og korte historier fra Oslos/Christianias historie. Statisk nettside (HTML, CSS, JSON) - ingen app-butikk.

**Publisert:** [tagoslo.no/home](https://tagoslo.no/home) (når DNS er satt) · speil: `https://kasa031.github.io/Kristiania/home`

## Kjør lokalt (fullt utviklingsrepo)

Hele prosjektet med FREMGANG, kilder og scripts ligger lokalt (ikke på offentlig GitHub). Fra prosjektmappa:

```powershell
.\scripts\serve.ps1
```

Åpne [http://localhost:8080/home](http://localhost:8080/home) (krever `spa_server.py` via `serve.ps1`, ikke vanlig `python -m http.server`).

## Sjekk at alt stemmer

| Hva | Hvor / kommando |
|-----|------------------|
| Data og UI-validering | `python scripts/verify-deliverable.py` (lokal, full repo) |
| HTTP-smoke (server må kjøre) | `.\scripts\serve.ps1` i ett vindu, deretter `python scripts/smoke-app-http.py` |
| Knapp- og id-smoke | `python scripts/smoke-ui-ids.py` og `python scripts/smoke-ui-buttons-static.py` |
| Gåtur-ruter (avstand) | `python scripts/desktop-walk-test.py` - les `content/DESKTOP-TEST.md` (lokal) |
| GitHub Actions deploy | [Actions på Kristiania](https://github.com/kasa031/Kristiania/actions) - grønn workflow etter push |
| Siste commit på GitHub | [main](https://github.com/kasa031/Kristiania) - `index.html` skal ha `?v=106` (eller nyere) i css/js |
| Live (etter DNS) | [tagoslo.no/home](https://tagoslo.no/home) - **må** peke til GitHub Pages, ikke annen host |

**Merk domene:** `CNAME` i repoet er `tagoslo.no`. GitHub Pages videresender `*.github.io/Kristiania` dit. Hvis `tagoslo.no/home` gir 404 (f.eks. Netlify/Next.js), er DNS/host feil - fiks hos registrar eller fjern motstridende Netlify-deploy på samme domene.

## Publisering

Dette repoet inneholder **kun app-filer** som deployes med GitHub Actions.

1. Push til `main`.
2. Repo **Settings → Pages → Build: GitHub Actions**.
3. **Custom domain** (valgfritt): `CNAME` i repo + DNS hos registrar.

`literature/`, `content/`, `sources/` og `scripts/` er lokale (gitignore).

## Kart

Standard: OpenStreetMap / Carto (ingen nøkkel). Valgfritt Mapbox lokalt via `data/map-config.local.json` (lokal fil, ikke i git).