# Bull I-V: hvordan alt skal inn i appen

**Sluttmål:** digitalisere Oslo som **interaktivt vandringskart** - alt vesentlig fra de fem bindene skal kunne oppdages ved å gå eller scrolle kartet: markør der det finnes adresse, ellers bakgrunn i tidslinjen med riktig tid og tema.

Mål per oppføring: lesbar norsk parafrase, `source_ref` (bind + sider), bilde/person der Bull eller supplement gir det, `verified` først når Karina har sjekket fysisk bind (F5).

## Fire innholdstyper

| Type | JSON | Kart | Eksempel |
|------|------|:----:|----------|
| **Sted** | `places.json` | ja | Ibsens hjem, Akershus |
| **Hendelse** | `events.json` | via sted | Brannen 1624 |
| **Person** | `people.json` | via `place_ids` | Henrik Ibsen |
| **Bakgrunn** | `context.json` | nei (tidslinje) | Geologi bind I, sosiale forhold |
| **Funn** | `finds.json` | ja | Gravfunn, steinalder |

Bind I har mye **bakgrunn** uten fast gateadresse (geologi, klima, sosiale forhold). Det havner i `context.json` med tema-tag og år, filtrert som hendelser.

## Tema (bind I og generell bakgrunn)

| Tag-id | Betydning |
|--------|-----------|
| `geologi` | Berggrunn, havnivå, istid |
| `natur` | Naturhistorie, dyreliv, landskap |
| `klima` | Klimaendring i historisk perspektiv |
| `sosial` | Sosiale forhold, klasse, bolig |

## Personer

- Én rad i `people.json` per person (id, navn, kort `summary`, `place_ids`, valgfri `image`).
- Sted der personen bodde eller står sentralt: vanlig `place` med koordinat + **markør på kartet**.
- I detaljpanelet: trykkbar lenke **Les om [person]** åpner persontekst (og bilder om satt).

`related_people` på steder bruker **person-id** (f.eks. `henrik-ibsen`), ikke bare fritekst.

## Bilder

- `image`: `{ "url", "credit" }` på `places`, `people`, og senere `events`/`context`.
- Kilde: Bull-illustrasjoner (når dere scanner/åpner rettigheter), Wikimedia, eller supplement med kreditt.
- Ingen bilder i repo før dere har lov - URL-er til eksterne arkiv i JSON.

## Arbeidsrekkefølge (bind for bind)

| Fase | Gjøres |
|------|--------|
| B1 | TOC per bind → liste kapitler som sted / hendelse / person / bakgrunn |
| B2 | Bind I: bakgrunn (`context`) + funn dere har, geologi/sosial |
| B3 | Bind II-III: flere steder + hendelser, personer med adresse |
| B4 | Bind IV-V: jubileum, byutvidelse, bilder fra teksten |
| B5 | Koble alle `source_ref` (bind + sider), `verified` kun Karina (F5) |
| B6 | Illustrasjonsfortegnelse bind I → `image` på matchende sted/person |

**Autonom regel:** ikke kopiere full OCR fra PDF. Parafrase (A14) + `sources/excerpts/` som notat.

## Status nå

- Personer: `henrik-ibsen`, `biskop-nikolas` (bispegården på kartet).
- Bakgrunn: **97** oppføringer i `context.json` (TOC kapittel bind I-V); 10 første manuelt parafrasert, resten titel/kilde-koblet til utdrag (B9: forbedre tekst).
- Bilder: bispeborg (Wikimedia) + Ibsen pilot.
- Dekning: liten brøkdel av bind I-V. `sources/innsamling/status.json` oppdateres ved `verify-deliverable`.

Se også **App-TODO** og **F16** i `FREMGANG.md`.