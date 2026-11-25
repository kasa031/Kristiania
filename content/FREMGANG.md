# Fremgang - Oslo-historie

**Dette er den eneste listen du skal følge.** Alt annet (README, JSON, nettsiden) er støtte til denne filen.

**Lesbar utgave (avkryssing):** [fremgang.html](fremgang.html)

Sist oppdatert: 25.11.2025

---

## Autonom fullføringsplan (AI trenger ikke spørre deg)

Disse reglene gjelder når du sier «ferdigstill» eller «neste steg». AI skal **gjøre valet OG levere**, ikke spørre om retning.

| # | Beslutning | Standard valg (uten avklaring) |
|---|------------|--------------------------------|
| A0 | **Arbeidsområde** | **Kun app** til Karina sier noe annet: `index.html`, `css/`, `js/`, `data/*.json`, `icons/`, `sw.js`, supplement-notater appen trenger. **Ikke:** TOC-indeksering, innsamling, MASTERLISTE, prosjektplan/rapport-oppdateringer |
| A1 | **Produktets hovedmodus** | Kart først (`primary_mode: explore`); gåtur valgfritt, skjult i `details` |
| A2 | **Nye steder/hendelser** | Bull der `status.json` gir dekning (TOC-sidetall) **eller** supplement (`sources/supplementary/`); kort parafrase; `verified: false` |
| A3 | **verified: true** | **Aldri** uten at du har sjekket fysisk bind - forblir `[ ]` på F5 |
| A4 | **Innhold uten utdrag** | Bruk TOC + korte parafraser; lag `sources/excerpts/*.md` som notat, ikke lang OCR |
| A5 | **Publisering** | GitHub Actions `static-pages.yml` + README-seksjon; du trenger bare `git push` og Pages på i repo |
| A6 | **Kartlag** | OpenStreetMap default (ingen nøkkel); Carto/Mapbox valgfritt i `map-config.local.json` |
| A7 | **Kvalitet før «ferdig»** | Kjør `python scripts/verify-deliverable.py` (preflight + desktop-test + filsjekk) |
| A8 | **Dokumentasjon** | Oppdater FREMGANG + README + PROSJEKTPLAN/PROSJEKTRAPPORT (MD og HTML-sammendrag) i samme omgang |
| A9 | **Scope** | Ikke ny backend, ikke fulltekst Bull, ikke parallelle todo-filer, ikke dokumentjobb mens A0 gjelder |
| A10 | **Innholdsvekst** | 3-5 nye kartstopp per økt (supplement + Bull); deretter `verify-deliverable` |
| A11 | **Brukertekst** | Ingen «Bull/Hammer beskriver» i `summary`/UI; fortell historien direkte. Kilde i `source_ref` og rapport, ikke i app-stemme |
| A15 | **Historisk vandringskart** | Header/footer: «Historisk vandringskart». Ingen bind/Bull/bøker i UI; intern kildesporing kun i JSON-notater |
| A16 | **Les regler først** | Workspace + `.cursor/rules` før endringer; ingen interne lenker i `index.html` (theme-preview, fremgang, plan) |
| A14 | **Parafrase** | `summary` = **norsk gjengivelse av kilde**, ikke tolkning eller mock. Bull: utdrag/TOC + sidetall; supplement: notat med URL. Ingen datoer eller «fakta» uten kilde. |
| A12 | **Supplement** | Nye steder: notat i `sources/supplementary/notater/` + `pages: supplement`; ingen ny TOC-jobbing |
| A13 | **App først** | Ikke utvide innsamling/MASTERLISTE/rapport før app-innhold er bra nok ute |

**Eneste ting som står igjen hos deg (kan ikke automatiseres):** F5 sluttkildekontroll mot bind på hylla; valgfri `toc_reviewed` i `manifest.json`; valgfri live URL etter push.

---

## Visjon (sluttmål)

**Hele Oslo som interaktivt vandringskart**, bygget ut fra informasjon i **Bull bind I-V** (supplement der boken mangler adresse eller bilde):

| I byen (gå / utforsk) | Uten fast punkt (les i tidslinje) |
|-----------------------|-----------------------------------|
| Steder, hendelser, funn, personers hus/arbeidssted | Bakgrunn (geologi, klima, sosial, m.m.) |
| Bilder med kreditt der kilden gir det | Tema-filter og år slik Bull kapittlene ligger |

**To måter å bruke kartet:** fri **Se kart** (posisjon, nær deg, søk) og **Gå rute** (ferdig rekkefølge med tid og avstand). Løypene er utsnitt; målet er at nesten all byhistorikk skal finnes på kartet eller i tidslinjen når B4-B6 er ferdig faset inn.

---

## NÅ (app-fase - historie på kartet)

**Fokus:** bare nettsiden. Bull bind I-V er grunnmur; **flere steder** kan fylles med supplementære kilder (byleksikon, SNL, kulturminner). **Ikke** full re-indeksering av TOC/PDF.

| # | Gjør dette | Ferdig |
|---|------------|:------:|
| F1 | TOC `sources/toc/` | [x] |
| F2 | Alle løyper med `place_order` og `data/walks/` | [x] |
| F3 | Sidetall i JSON fra TOC (utkast) | [x] |
| F4 | Desktop-test av løyper | [x] |
| F5 | Sluttkildekontroll (`verified: true`) | [ ] **kun Karina** |
| F6 | Utdrag `sources/excerpts/` + parafrase i JSON | [x] |
| F7 | `standpoint` + minikart i detalj | [x] |
| F8 | Koordinater desktop | [x] utkast |
| F9 | Utforsk-modus (posisjon, nær deg, kartklikk) | [x] |
| F10 | Autonom plan (denne seksjonen) | [x] |
| F11 | Publisering klar (workflow + README) | [x] |
| F12 | PWA-ikon + `verify-deliverable.py` | [x] |
| F13 | 3 nye utforsk-steder bind II (Grønland, bymark, 1716) | [x] |
| F14 | Bind IV utdrag-notat + dokument synk | [x] |
| F15 | `sources/supplementary/` + app-steder uten full Bull-side | [x] start |
| F16 | Historisk kvalitet (parafrase, notat, `verified` når du sjekker) | [ ] løpende |

**Tall:** 85 steder, 90 hendelser, 22 funn (med illustrasjon), 6 personer, 97 bakgrunn, 50 blå skilt (alle i seed koblet).

**Test:** `.\scripts\serve.ps1` · app først, rapport (F5) senere.

**Neste (autonom):** ta fra **App-TODO** nedenfor - én rad om gangen eller hele økten etter tabellen.

---

## App-TODO (aktiv - kun nettsiden)

Gjelder til du sier at noe annet skal prioriteres. Kryss av i [fremgang.html](fremgang.html) eller her.

| # | Oppgave | Hvor | Ferdig |
|---|---------|------|:------:|
| T1 | **3-5 nye steder/hendelser** (supplement eller Bull-sidetall) | `data/places.json`, `data/events.json`, `sources/supplementary/notater/` | [x] +3 sentrum/grønland 25.11 (Treschow, Olympen, LO) |
| T2 | **Tekstkvalitet** - trofast parafrase (A14), ingen mock; Bull-bind gjennomgås ved sidetall | `data/*.json`, `sources/excerpts/` | [ ] løpende (Paulus-kirke-bilde rettet 25.11) |
| T3 | **Casual UI** - bind/side ikke synlig for lesere; «Les mer» for supplement | `js/app.js`, `css/style.css` | [x] |
| T4 | **Kart og detalj** - mobil høyde, scroll, marker/klikk, nær deg | `css/style.css`, `js/app.js` | [x] masthead ren tekst, filtre grid, markør 36px mobil |
| T5 | **Koble nye steder** - `related_*`, episoder/filter der det gir mening | `data/episodes.json`, `site-config.json` | [x] rådhus-løype |
| T6 | **Leveransesjekk** etter hver innholdsøkt | `python scripts/verify-deliverable.py` | [x] rutine |
| T7 | **Dekning kart** - pri: Kvadraturen, Akerselva, havn, 1800-/1900-tall | supplement + eksisterende bind | [ ] løpende (+Collett oljemølle Bjølsen, Akerselva map-stopp 25.11) |
| T8 | **Merkevare og bevegelse** - navn Kristiania, typografi, animasjon, avis+slotts tema | `css/theme-kristiania.css`, `site-config.json`, `data/KONFIGURASJON.md` | [x] |
| T11 | **Blå skilt** - destinasjonsfilter, `blue-signs.json`, import fra OBV-liste | `data/`, `scripts/import-blaaskilt.py`, `js/app.js` | [~] 58 i app, seed 58/58 koblet |
| T12 | **Gåtur-UX** - tydelig start/slutt, fane Gå rute, reiseforbindelse ved posisjon | `js/app.js`, `index.html`, `site-config.json` | [x] Gåvei + Entur-lenke over 600 m |
| T13 | **Reiseforbindelse v2** - kollektiv/turvariant, entur/OSM-rute i app (ikke bare ekstern lenke) | `js/app.js`, supplement | [~] Entur + OSM fotrute-lenke; innebygd rute senere |

### Bull-full (bind I-V i appen)

| # | Mål | Status |
|---|-----|:------:|
| B0 | Plan: sted / hendelse / person / bakgrunn / bilde | [x] [BULL-DEKNING.md](BULL-DEKNING.md) |
| B1 | `people.json` + kartstopp + lesbar biografi | [x] pilot Ibsen |
| B2 | `context.json` + tema (geologi, klima, natur, sosial) | [x] pilot bind I |
| B3 | Bilder (`image` med kreditt) på sted/person/funn | [x] 77/77 steder (`patch-place-images.py`) |
| B4 | TOC bind I → backlog bakgrunn og steder | [x] via B7-B8 |
| B5 | Bind II-V innholdsvekst + illustrasjonsliste | [ ] |
| B6 | Hele Bull gjennom (årvis, uten full OCR) | [ ] langt løp |
| B7 | TOC bind I-V → `bull-toc-backlog.json` + ingest-script | [x] 147 kap. sporet |
| B8 | Alle kapittel i tidslinje (`context.json` fra TOC) | [x] 97 bakgrunn |
| B9 | Parafrase A14 kapittel for kapittel (erstatt titel-led) | [~] titel-led fjernet 25.11; enkeltkap. kan poleres ved F5 |
| B10 | Sted/person/bilde per kapittel + illustrasjonslister | [ ] |
| B11 | **Blå skilt** (Oslo Byes Vel) – alle ~500, filter + kart | [~] 85 i app, seed utvides |

**Kjørsel:** `python scripts/bull-chapter-ingest.py --all --write` · deretter `python scripts/improve-context-summaries.py` · sporing i `sources/innsamling/bull-toc-backlog.json`.

**Pause (til ny beskjed):** F5 `verified: true`, feltgåtur som krav, ny TOC/PDF-indeksering, rapport/plan-vedlikehold.

---

## De 7 stegene (i rekkefølge)

| Steg | Navn | Status |
|:----:|------|:------:|
| 1 | Innholdsfortegnelse inn | [x] |
| 2 | Løype 1624 + systematisering | [x] |
| 3 | Middelalder + Kvadraturen | [x] |
| 4 | Gåtur validert (desktop-test) | [x] |
| 5 | Akerselva + 1814 | [x] innhold |
| 6 | Løype Mot 1924 | [x] innhold |
| 7 | Publisering / deling | [x] klar (push + GitHub Pages) |

---

## Løyper på nettsiden (status)

| Løype | Stopp | Bind | Nettside | Kvalitet |
|-------|-------|------|:---:|----------|
| 1624 - nye Kristiania | 8 | I-II | ja | TOC-sidetall |
| Middelalder-Oslo | 7 | I | ja | TOC-sidetall |
| Kvadraturen 1600-1700 | 12 | II | ja | TOC + supplement (+Kontraskjerp) |
| Akerselva tidlig industri | 15 | II-III | ja | TOC + supplement (+havn ved Akershus) |
| 1814-hovedstaden | 8 | III-IV | ja | TOC + supplement |
| Mot 300-årsjubileet | 14 gå / 37 kart | IV-V | ja | `map_place_order` for Filipstad m.m.; gåtur ca. 8 km |

---

## Kildeinnsamling (bøker i `literature/`)

| | |
|--|--|
| Oversikt | [sources/innsamling/INNSAMLING.md](../sources/innsamling/INNSAMLING.md) |
| AI leser | `sources/innsamling/status.json` |
| Oppdater | `python scripts/literature-status.py` |

---

## Arbeidsregler (deg + AI)

1. **Én liste:** Oppdater bare denne filen når «neste steg» endres.
2. **Autonom plan:** Følg A0-A13 ved «ferdigstill» / «neste steg» - ikke spør om retning.
3. **Før JSON:** Les `status.json`; avhuking her først.
4. **Verifisering:** `verified: true` kun etter fysisk sjekk (F5).
5. **Sitater:** Ingen lange sitater uten utdrag.

---

## Presentasjon: formater som passer innholdet

| Innhold | Beste format | Hvorfor |
|---------|--------------|---------|
| Gatekart / bygg | Raster-kart (Carto), zoom 16-19 | Leserorientering ute; hele skjermen på mobil |
| Ett sted | Tittel + 2-4 setninger + «Se herfra» + lite kartutsnitt | Leses stående; ikke lang essay |
| Hendelse (mange) | Tidslinje-kort, max 3 linjer teaser | Oversikt; fulltekst i detalj ved valg |
| Liste «nær deg» | Knapper (navn + avstand) | Rask valg uten å scrolle hele siden |
| Filtre / gåtur | Lukket `details` | Sekundært; skal ikke ta plass fra kart |
| Kilde (bind/side) | JSON `source_ref`, skjult i app | For rapport og F5, ikke for casual lesere |
| Prosjektdokumenter | Markdown + HTML/PDF | Rapport og plan, ikke i kart-appen |

Layout-regel: **én skjermhøyde** - kart og historie scroller hver for seg (`app-main`), ikke hele nettsiden.

## Teknikk

| Verktøy | Hva det gjør |
|---------|----------------|
| `python scripts/verify-deliverable.py` | Full leveransesjekk |
| `python scripts/preflight.py` | Innsamling + JSON |
| `.\scripts\serve.ps1` | Lokal server :8080 |
| `python scripts/desktop-walk-test.py` | Løyper og koordinater |

### Publisering (steg 7)

1. Push repo til GitHub (uten `literature/`).
2. **Settings - Pages - Source: GitHub Actions.**
3. Workflow `.github/workflows/static-pages.yml` deployer statiske filer.

---

## Logg

- 25.11 - TOC autouttrekk; literature/ i .gitignore
- 25.11 - Fase 1: 6 løyper, PWA, innsamling, preflight
- 25.11 - F9 utforsk-modus; F4 desktop; minikart
- 25.11 - Autonom plan F10-F14; 31 steder; GitHub Pages workflow; verify-deliverable
- 25.11 - A11: leserstemme uten Bull/Hammer i app-tekst; `normalize-reader-text.py`
- 25.11 - App-fase 2: supplement (Nationaltheatret, Vulkan, Gamle Aker); tekstkvalitet; SW v6; ingen TOC-jobb
- 25.11 - A0 kun app + App-TODO T1-T7 i FREMGANG/fremgang.html
- 25.11 - A14 trofast parafrase; supplement rettet mot SNL/byleksikon; Grünerbrua lagt til
- 25.11 - Bull-utdrag s203-221, s477; Bentse Brug, Norges Bank; parafrase rettinger
- 25.11 - App-navn **Kristiania**; Fraunces/Source Sans 3; `motion.css` + `motion.js`; SW v11
- 25.11 - 5 gravfunn (Bull s. 23); 3 rådhussteder (SNL); Kvadraturen/mot-1924 løype; SW v12
- 25.11 - Tema avis 1880 + slottsfarge 1848; KONFIGURASJON (ingen API krav); SW v13
- 25.11 - Dronningensgate-tema; Mapbox local; OSM/Carto-fallback; 4 gravfunn + Tollbugata; SW v15-16
- 25.11 - GitHub Pages workflow: rsync-bundle (uten upload-pages exclude); Vaterland/Bjørvika; SW v17
- 25.11 - Youngstorget, Nylands Verksted, havn ved Akershus; mot-1924 løype; mobil markører; SW v18
- 25.11 - Nydalen, Rådmannsgården, Klingenberg; Grønland-tekst Bull III; nær deg mobil; SW v19
- 25.11 - Spigerverk, Paleet, Aker Pipervika; 1716-parafrase; mobildetalj; SW v20
- 25.11 - UX: hurtigstart-løyper, nullstill filtre, færre kart-hop, nær deg; SW v21
- 25.11 - UX: enklere filtre, tidslinje-scroll, 3 steder (Eidsvolls plass m.fl.); SW v22
- 25.11 - Søkefelt (sted/adresse + nål); kartbakgrunn under «Bakgrunn»; SW v23
- 25.11 - Ingen bind i UI; løype-undertitler; St. Hanshaugen; bydel uten Bull-ref; SW v24
- 25.11 - Bydelskart, tidsalder-filter, funn-register (Bull s.21-22), tidslinje til 1924
- 25.11 - Teknisk QA: fiks «Min posisjon» ved gjenopptatt følging; smoke-ui-ids; verify OK; SW v25
- 25.11 - T1/T7: Stortorvet, Homansbyen, Hammeren kraftverk, Vøyen/Hjula + 5 hendelser; jubileum-parafrase; løyper justert; SW v26
- 25.11 - Masthead: ny rubrikk, lead, dek og typografi (avis-tema); SW v27
- 25.11 - Hovedvalg Se kart / Gå rute; rutekort starter gåtur ved trykk; estimert tid; SW v29
- 25.11 - T4: tidslinje-scroll i Se kart-panel; `scripts/open-app.ps1` for lokal forhåndsvisning
- 25.11 - Teknisk QA: SW network-first v30, exitWalkMode, filter under gåtur, smoke-app-http; verify OK
- 25.11 - Dyp QA: dobbel «ca.» i rutetid; Gå rute låst under gåtur; én Esc-handler; smoke-app-http js-fix; SW v32
- 25.11 - T4: tydelig posisjons-hjelp (nettleser + Windows); mobil touch på faner/gåtur/rutekort; smoke-ui-buttons-static; SW v33
- 25.11 - T7: Skippergata, Filipstad, Paulus kirke, Sagene kirke + 4 hendelser; løyper justert; SW v34
- 25.11 - Mot 1924: Paulus/Filipstad kun på kart (ikke gåtur); løypetall synket i FREMGANG; verify OK
- 25.11 - Mot 1924: ny stopprekkefølge (~5,7 km); Brugata + hendelse (kart); SW v36
- 25.11 - Akerselva: elvefølge Nydalen-Pipervika (~5,8 km); suggest-route-order.py; SW v37
- 25.11 - App-TODO: T2 Grønland/Karl Johan; T7 Møllergata; T4 mobil markør/tidslinje; fremgang.html synk; SW v38
- 25.11 - Bull-full start: people + context + bilder; Ibsen-hjem; BULL-DEKNING.md; SW v39
- 25.11 - B4 bind I: +8 context, biskop Nikolas, bispegård bilde/tekst; utdrag-notater; SW v40
- 25.11 - B7-B8: bull-chapter-ingest bind I-V (97 bakgrunn, 147 kap. backlog, 80+ utdrag); B9-B10 åpent; SW v43
- 25.11 - B11/T11: Blå skilt filter + 85 skilt, import-blaaskilt; SW v44
- 25.11 - T4: masthead ren tekst (ingen ui-jump), filtre grid, kart-header skalering; SW v46
- 25.11 - T7/T5: +3 steder (Treschowgården, Olympen, LO), 2 hendelser; mot-1924 `place_order` med Møllergata m.m.; SW v47
- 25.11 - B3/UI: kartfarger per type (`map-markers.json`), funn-bilder, person-merker + portretter; SW v48
- 25.11 - B3/B9/T7: 14 stedsbilder, 6 context bind II parafrase, Ankerbrua + Olav; SW v49
- 25.11 - T4: gatesøk med «Hele X» + gatenummer-liste, færre duplikat-adresser; SW v50
- 25.11 - B9/T7: +2 steder (Gjestgiveri, Collettgården), bind III parafrase; SW v51
- 25.11 - B9/T7/B11: bind IV parafrase (8 kap.), Bybrann 1858 hendelse, Mangelsgården, blå skilt Skippergata; SW v52
- 25.11 - B9/B3: bind IV +13 og bind I +6 parafrase; 14 nye stedsbilder (havn/kvadratur/sentrum); SW v53
- 25.11 - B9/B3: bind V +15 og bind I +7 parafrase; 5 stedsbilder til; OCR-rot i 2 bakgrunnskort rettet; SW v54
- 25.11 - B9: `remaining-batch` +25 (rest bind V/I/II/IV + OCR-rot); SW v55
- 25.11 - T4: Mapbox-fallback til OSM ved ugyldig token; bydelslag bort ved gatezoom; kartlag merket; SW v56-v57
- 25.11 - B3/B11: +7 stedsbilder, Grønland Asyl koblet blå skilt; SW v57
- 25.11 - T1/T7: Gassverket + Nonneseter, gass 1854; Akerselva/havn-bilder; seed kobling; SW v58
- 25.11 - Funn: utvidete parafraser bind I s.21-24 (viking/jordbruk/Teisen), +3 (Blåsen, Østre Aker kirke, bispeborg 1917); SW v59
- 25.11 - Forside: hjemskjerm med Søk og Gå rute, tittel tilbake til forsiden; SW v60
- 25.11 - T7/B3: Hausmanns bru 1892, mot-1924 havn (Vaterland/Ankerbrua), alle stedsbilder; SW v61
- 25.11 - UX: forsideknapper fikset (init), gul/oransje CTA, header-pitch, lesbarere typografi; SW v62
- 25.11 - T7/T2/B11: kornkrise 1808, 1814-løype utvidet, 4 context-parafraser, +6 blåskilt-koblinger; SW v63
- 25.11 - Forside/header: korte salgsord, gul/oransje CTA; SW v64
- 25.11 - UX: Tilbake til forsiden etter Søk/Gå rute (+ Escape); SW v65
- 25.11 - T2/T7/B11: context batch3 (+6 parafraser), +12 seed place_id, Kontraskjerp på kvadraturen-løype; SW v67
- 25.11 - UX: Tilbake til forsiden uten avhengighet av nettleserens historikk; SW v69
- 25.11 - UX: /home, /kart, /tur i adressen; masthead uten klikk; SPA-server lokalt; T2 batch5 (alle korte context); SW v72
- 25.11 - T12: rubrikk uten «interaktivt», Gå rute-fane fikset, start/slutt + reisevei-lenke; SW v73
- 25.11 - B11/T7: +9 blåskilt-koblinger (forfattere/teater); forsøk-CTA brun+gull/oransje; theme-preview lint; SW v76
- 25.11 - T7/T12/T13: Akerselva-løype +havn ved Akershus; Entur-lenke ved gåtur; tekstkorrektur; SW v77
- 25.11 - T2/T7/B11: context batch4 (+8), +12 blåskilt-koblinger, Filipstad på mot-1924; SW v70
- 25.11 - T7/B11: +3 steder (Storebrand, Steen/Strøm, Schweigaards bro), 2 hendelser bind V; mot-1924; A16 footer; SW v79
- 25.11 - T4: filter Tidsperiode med steinalder/jernalder; funn filtreres; tidslinje fra -10000; SW v80
- 25.11 - T7/B11: +4 steder havn/kvadratur 1880 (Handelsstand, Wessels, Victoria, Piperviksbakken), 2 hendelser; SW v81
- 25.11 - QA: mot-1924 gåtur 14 stopp / map_place_order; T13 OSM fotrute; verify + smoke http OK; SW v82
- 25.11 - T7/T2/B11: Collett oljemølle Bjølsen, juni 1795; Akerselva map_place_order; Paulus-bilde; SW v83