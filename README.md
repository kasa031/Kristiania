# Oslo-historie: kart og historie

Gatekart, din posisjon, trykk for å lese - kuratert fra Edvard Bulls *Kristianias historie* (bind I-V).  
Statisk nettside (HTML + JSON), ikke app-butikk.  
**Prosjekt:** Karina Sætersdal Nilssen (dedikert til Thomas, Alma og Celia).

## Hva som leveres (nov. 2025)

| Del | Innhold |
|-----|---------|
| **Hovedopplevelse** | Utforsk kartet, «Min posisjon», «Nær deg», trykk gater/merker for historie |
| **Ekstra** | Tidslinje, filtre, valgfri kuratert gåtur (lukket boks) |
| **Data** | **31** steder, **44** hendelser, `source_ref`, `verified: false` (utkast) |
| **Kilder** | TOC bind I-V; PDF lokalt i `literature/` (gitignorert) |
| **Fremdrift** | [content/FREMGANG.md](content/FREMGANG.md) - inkl. **autonom fullføringsplan** for AI |

## Dokumentasjon

| Dokument | Formål |
|----------|--------|
| [FREMGANG.md](content/FREMGANG.md) | Én oppgaveliste + autonome beslutningsregler |
| [fremgang.html](content/fremgang.html) | Avkryssing i nettleser |
| [PROSJEKTPLAN.md](content/PROSJEKTPLAN.md) | Visjon og sluttmål |
| [PROSJEKTRAPPORT.md](content/PROSJEKTRAPPORT.md) | APA 7 rapport |

## Kjør lokalt

```powershell
cd "c:\Users\Karina\OneDrive - Kristiania\Skrivebord\Oslo_Historie"
.\scripts\serve.ps1
```

Åpne `http://localhost:8080/`. Geolocation krever HTTPS eller localhost.

### Leveransesjekk (før du deler)

```powershell
python scripts\verify-deliverable.py
```

## Kart

- Standard: **Carto Voyager** (gater og bygg). **Ingen API-nøkkel nødvendig.**
- Valgfritt: `data/map-config.local.json` med Mapbox-token (se `data/map-config.local.json.example` og `data/KONFIGURASJON.md`).

## Publisere på web

Repo inneholder **GitHub Actions** (`.github/workflows/static-pages.yml`).

1. Push til GitHub (`literature/` følger ikke med - gitignore).
2. Repo **Settings - Pages - Build: GitHub Actions**.
3. Etter vellykket workflow: nettsiden på `https://<bruker>.github.io/<repo>/`.

Netlify/Cloudflare: last opp rotmappa (samme filer, uten `literature/`).

## Mapper

- `data/` - places, events, `site-config.json` (`primary_mode: explore`)
- `sources/excerpts/` - korte utdrag/notater
- `scripts/verify-deliverable.py` - preflight + desktop-test + filsjekk