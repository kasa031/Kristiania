# Historisk vandringskart - Kristiania

Kart, posisjon og korte historier fra Oslos/Christianias historie. Statisk nettside (HTML, CSS, JSON) - ingen app-butikk.

**Publisert:** [tagoslo.no/home](https://tagoslo.no/home) (når DNS er satt) · speil: `https://kasa031.github.io/Kristiania/home`

## Kjør lokalt (fullt utviklingsrepo)

Hele prosjektet med FREMGANG, kilder og scripts ligger lokalt (ikke på offentlig GitHub). Fra prosjektmappa:

```powershell
.\scripts\serve.ps1
```

**Anbefalt lokalt:** `.\scripts\open-local-app.ps1` (port **8808**, åpner nettleser). SPA-ruter `/home`, `/kart`, `/tur` krever `spa_server.py` - ikke vanlig `python -m http.server`.

**Viktig:** Hvis du har **Anki** installert, holder AnkiConnect ofte **port 8765** på `127.0.0.1`. Da får du bare JSON (`{"apiVersion":"AnkiConnect..."}`) i nettleseren - ikke kartet. Bruk scriptet over (8808), ikke 8765.

## Test-URLer (app)

### Fungerer nå (lokal på PC-en din)

| Hva | Lenke |
|-----|--------|
| **Forside** | [http://127.0.0.1:8808/home](http://127.0.0.1:8808/home) |
| Direkte `index.html` | [http://127.0.0.1:8808/index.html](http://127.0.0.1:8808/index.html) |
| Kart (søk) | [http://127.0.0.1:8808/kart](http://127.0.0.1:8808/kart) |
| Gåtur | [http://127.0.0.1:8808/tur](http://127.0.0.1:8808/tur) |

Start: `.\scripts\open-local-app.ps1`. Alternativ: `.\scripts\serve.ps1` (port 8808, terminal med Ctrl+C).

### Offentlig (GitHub Pages) - for tiden ødelagt pga. domene

Repo har `CNAME` → **tagoslo.no**. Da sender GitHub alle `kasa031.github.io/Kristiania/...` videre til `tagoslo.no`, og `http://tagoslo.no/home` gir **404** inntil DNS peker riktig mot GitHub Pages.

| Hva | Lenke | Merk |
|-----|--------|------|
| Pages (redirect) | [https://kasa031.github.io/Kristiania/home](https://kasa031.github.io/Kristiania/home) | 301 → tagoslo.no |
| Planlagt eget domene | [https://tagoslo.no/home](https://tagoslo.no/home) | Feil sertifikat/DNS (`ERR_CERT_COMMON_NAME_INVALID`) til hosting er riktig satt |
| Deploy-status | [https://github.com/kasa031/Kristiania/actions](https://github.com/kasa031/Kristiania/actions) | Siste run må være grønn etter push |

Etter `git push`: vent på grønn Actions-run før live nett viser ny `?v=` i `index.html`. For å teste på github.io uten redirect må `CNAME` midlertidig fjernes (egen beslutning).

## Sjekk at alt stemmer

Før du tester manuelt i nettleser:

```powershell
.\scripts\qa-app.ps1
```

Det kjører `verify-deliverable` (data, UI-id-er, sikkerhet, SPA-ruter, bilder, løyper).

| Hva | Hvor / kommando |
|-----|------------------|
| Data og UI-validering | `python scripts/verify-deliverable.py` (lokal, full repo) |
| HTTP-smoke (server må kjøre) | `.\scripts\serve.ps1` i ett vindu, deretter `python scripts/smoke-app-http.py` |
| Knapp- og id-smoke | `python scripts/smoke-ui-ids.py` og `python scripts/smoke-ui-buttons-static.py` |
| Gåtur-ruter (avstand) | `python scripts/desktop-walk-test.py` - les `content/DESKTOP-TEST.md` (lokal) |
| GitHub Actions deploy | [Actions på Kristiania](https://github.com/kasa031/Kristiania/actions) - grønn workflow etter push |
| Siste commit på GitHub | [main](https://github.com/kasa031/Kristiania) - `index.html` skal ha nyeste `?v=` i css/js (sjekk mot lokal `index.html`) |
| Live (etter DNS) | [tagoslo.no/home](https://tagoslo.no/home) - **må** peke til GitHub Pages, ikke annen host |

**Merk domene:** `CNAME` i repoet er `tagoslo.no`. GitHub Pages videresender `*.github.io/Kristiania` dit. Hvis `tagoslo.no/home` gir 404 (f.eks. Netlify/Next.js), er DNS/host feil - fiks hos registrar eller fjern motstridende Netlify-deploy på samme domene.

## Publisering

Dette repoet inneholder **kun app-filer** som deployes med GitHub Actions.

1. Før push: `python scripts/verify-deliverable.py` og `bash .github/check-pages-bundle.sh`.
2. Push til `main`.
3. **Sjekk Actions:** siste run for commiten skal være **grønn** ([Actions](https://github.com/kasa031/Kristiania/actions)). Ved feil: les logg på jobben **Deploy**, fiks, push på nytt.
4. Repo **Settings → Pages → Build: GitHub Actions**.
5. **Custom domain** (valgfritt): `CNAME` i repo + DNS hos registrar.

`literature/`, `content/`, `sources/` og `scripts/` er lokale (gitignore).

## Kart

Standard: OpenStreetMap / Carto (ingen nøkkel). Valgfritt Mapbox lokalt via `data/map-config.local.json` (lokal fil, ikke i git).