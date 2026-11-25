# Kilder: Kristianias historie

Lokale filer knyttet til Bulls *Kristianias historie* (bind I-V). Nettsiden bygger på **parafraser** og `source_ref` i `data/`, ikke fulltekst fra bøkene.

## Primær (dine filer)

| Plassering | Innhold | Git |
|------------|---------|-----|
| `literature/*.pdf` | Dine skannede/ digitale bind | **Ignorert** (`.gitignore`) |
| `sources/toc/` | Innholdsfortegnelser | Versjoneres |
| `sources/excerpts/` | Korte utdrag du jobber med | Kun ved behov |
| **`sources/innsamling/`** | **Innsamlingsstatus per bind** (manifest + `status.json`) | Versjoneres |

**Sporing:** `python scripts/literature-status.py` oppdaterer [innsamling/INNSAMLING.md](innsamling/INNSAMLING.md). Les [innsamling/README.md](innsamling/README.md) for arbeidsflyt (AI og deg).

**Utdrag:** `python scripts/extract-excerpt.py --bind 3 --pages 227-229 --out sources/excerpts/...` deretter `python scripts/enrich-from-excerpts.py` (tilpass) eller manuell parafrase i JSON.

**TOC fra PDF:** `python scripts/extract-toc.py` (krever PDF i `literature/`).

## Sekundær (nett)

| Bind | Periode | Oppføring |
|------|---------|-----------|
| I | til 1624 | [Lokalhistoriewiki - Kristianias historie](https://lokalhistoriewiki.no/wiki/Kristianias_historie) |
| II-V | 1624-1924 | Samme oversikt + faksimile-lenker i `data/bind-sources.json` |

Faksimiler: [Wikimedia Commons (Edvard Bull)](https://commons.wikimedia.org/wiki/Category:Edvard_Bull_d._e.).

## Arbeidsrekkefølge (profesjonell)

1. **TOC** i `sources/toc/` (uttrekk eller manuell kontroll mot bind).
2. **Kuratér** stopp og hendelser for én løype om gangen.
3. **Skriv** parafrase til `data/places.json` / `events.json` med `source_ref`.
4. **Valider** sidetall mot bind ved sluttfase (jf. prosjektplan).
5. **Utdrag** kun ved tvil: `sources/excerpts/` med bind + sider i filnavn.

Valgfritt: OCR-kopi til `sources/ocr/` (gitignorert) for raskere søk - ikke nødvendig hvis `literature/` har søkbar tekst.

## Opphavsrett

Offentlig nettside: **korte sammendrag** + kildehenvisning. Ikke publiser full boktekst uten rettighetsvurdering.