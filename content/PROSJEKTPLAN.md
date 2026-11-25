# Prosjektplan: Oslo-historie

**Dokumenttype:** Prosjektplan (visjon, sluttmål, faser)  
**Referansestil:** APA 7  
**Forfatter:** Karina Sætersdal Nilssen  
**Versjon:** 1.1, november 2025  

---

## Dedikasjon

Til Thomas, Alma og Celia - med takk for at dere deler byen med meg, og for at dere bærer hverdagen mens jeg går i Bulls spor.
**HTML:** [prosjektplan.html](prosjektplan.html)  
**PDF:** [prosjektplan.pdf](prosjektplan.pdf)  
**Oppgaveliste:** [fremgang.html](fremgang.html)  
**Prosjektrapport (metode/resultat):** [PROSJEKTRAPPORT.md](PROSJEKTRAPPORT.md)

---

## Sammendrag

Denne planen beskriver **hva Oslo-historie skal bli når det er ferdig**, hvordan vi kommer dit, og hva som regnes som «fertig». Produktet er en **statisk nettside** (HTML/CSS/JS, ingen app-butikk) knyttet til Edvard Bulls *Kristianias historie* (bind I-V), med kart, tidslinje og kuraterte løyper. Kan hostes som vanlig webside. Full kildekontroll og endelig verifisering skjer **når rapporten ferdigstilles** og eier går systematisk gjennom kilder - ikke som forutsetning for hvert utkast underveis.

**Nøkkelord:** prosjektplan, sluttleveranse, gåtur, kildekontroll, Bull

---

## 1. Visjon og sluttresultat

### 1.1 Elevator pitch

Oslo-historie kobler Bulls fembindsverk til et gatekart i mobilen: du ser hvor du er, trykker gater og bygg, og får korte kildehenviste sammendrag. Valgfrie gåtur-ruter finnes for de som vil følge en fast rekkefølge.

### 1.2 Hva prosjektet skal ende i

Når prosjektet er **ferdigstilt**, skal følgende eksistere:

| Leveranse | Beskrivelse |
|-----------|-------------|
| **Nettside** | Statisk side med kart (utforskning først), tidslinje, filtre og valgfri gåtur-modus |
| **Seks løyper** | Minst én full gåtur per hovedperiode bind I-V; hver med 4-7 stopp og `place_order` testet i felt |
| **Datagrunnlag** | JSON med steder og hendelser; alle tekster på nettsiden har `source_ref` (bind + sider) |
| **Dokumentasjon** | Prosjektplan (denne filen), prosjektrapport APA 7, og fremdriftsliste (FREMGANG) |
| **Kilderegister** | Innholdsfortegnelser i `sources/toc/`; PDF-er lokalt i `literature/` |
| **Kvalitet ved levering** | Eier har gjennomgått kilder for alt innhold som skal stå som «ferdig»; `verified` satt der det er avklart |

Prosjektet er **ikke** et mål om å digitalisere eller erstatte hele verket. Det er en **kuratert bro** mellom bøkene og byrommet.

### 1.3 Hva som ligger utenfor sluttmålet (med mindre du velger fase 8)

- Fulltekst av Bull på nett  
- Nedlastbar mobilapp / App Store  
- Database, brukerkonto eller innlogging  
- Obligatorisk offentlig deling (kan være valgfritt steg 7)

---

## 2. Målgruppe og bruksbilder

1. **Deg selv** som leser bindene og vil forankre kapittler i Oslo.  
2. **Lokalhistorisk interesserte** som vil ha Bulls tråd, ikke et leksikon med 7000 artikler.  
3. **Valgfritt senere:** studenter, guider eller venner på gåtur med mobilen.

Typisk bruk: 40-50 minutter ute; ett avsnitt per stopp; sidetall som pek til videre lesning hjemme.

---

## 3. Faser til ferdig prosjekt

Planen har **syv obligatoriske steg** (detaljer i FREMGANG) og **én valgfri sluttfase**.

**Status nov. 2025 (fase 1):** Levert med utforsk-modus, 31 steder og 44 hendelser, 6 valgfrie ruter; `source_ref` overalt; `verified: false` til du gjør sluttkontroll (F5). Publisering klar via GitHub Pages.

| Fase | Innhold | Utfall |
|:----:|---------|--------|
| 1 | TOC fra alle bind (PDF `literature/` → `sources/toc/`) | Du finner sider uten gjett |
| 2 | Løype 1624: innhold og sidetall | Første «gullstandard»-løype |
| 3 | Middelalder-Oslo + Kvadraturen | Bind I-II dekning |
| 4 | Feltgåtur alle aktive løyper | Rekkefølge og tekstlengde stemmer |
| 5 | Akerselva + 1814 | Bind III-IV på nettsiden |
| 6 | Løype «Mot 1924» + bind V | Hele verkets tidslinje kuratert |
| 7 | Hosting / deling (valgfritt) | GitHub Pages, Origin, eller kun arkiv lokalt |
| **Slutt** | **Prosjektrapport ferdig** + **kildegjennomgang** | APA-rapport; tekster på nettsiden bekreftet mot bøker |

Underveis er utkast og `verified: false` **normalt**. Det blokkerer ikke utvikling av rapport eller nettside.

---

## 4. Definition of done (suksesskriterier)

Prosjektet kalles **ferdig** når alle punktene under er oppfylt:

- [ ] Alle seks løyper har stopp, tekst og `place_order` gjennomført i felt  
- [x] TOC for bind I-V ligger strukturert i `sources/toc/`  
- [x] Hver hendelse/sted som vises i en løype har `source_ref` med bind og sidetall (utkast)  
- [ ] Eier har gjennomgått kilder for publisert innhold (ingen utkast-badge der innholdet skal stå som ferdig)  
- [ ] Prosjektrapport APA 7 er ferdigstilt og eksportert som PDF  
- [ ] Prosjektplan og fremgang er oppdatert og konsistente med det som er levert  

---

## 5. Arbeidsfordeling: deg, AI og nettsiden

| Rolle | Ansvar |
|-------|--------|
| **Deg** | Redaktør: historisk innhold, felt, endelig kildegjennomgang, ferdigstilt rapport |
| **AI (Cursor)** | Utkast, struktur, søk i PDF, oppdatering av JSON og dokumenter |
| **Nettsiden** | Viser utkast tydelig underveis; endelig tekst etter din kildegjennomgang |

---

## 6. Kilder og filstruktur (planlagt sluttarkiv)

```
Oslo_Historie/
  index.html, data/*.json     ← nettsiden du åpner i nettleseren (mobil eller PC)
  literature/*.pdf            ← bind I-V (lokalt, ikke i git)
  sources/toc/                ← innholdsfortegnelser
  content/
    prosjektplan.html|pdf     ← denne planen
    prosjektrapport.html|pdf  ← APA-rapport
    fremgang.html             ← avkryssing underveis
```

---

## 7. Risiko og forutsetninger

| Risiko | Tiltak |
|--------|--------|
| Feil sidetall i OCR/PDF | TOC + dine bøker ved sluttgjennomgang |
| AI-feil i parafraser | Ingen «ferdig» uten din lesing |
| Tidsbruk | Én liste (FREMGANG); utvid kun med stopp som skal i løyper |
| Opphavsrett | Kun korte sammendrag i repo; full boktekst lokalt |

**Forutsetning:** Du har tilgang til bind I-V (fysisk og/eller PDF i `literature/`).

---

## 8. Etter prosjektet (valgfritt)

- Statisk hosting og deling med studie / venner  
- Flere løyper eller dybdelag per kapittel  
- Overføring til museum/lokalhistorisk forening (kun hvis de ønsker kuratert innhold)

---

## Referanser

Bull, E. (1922-1936). *Kristianias historie* (bd. 1-5). J. W. Cappelens forlag.

Bull, E., & Brøgger, A. W. (1917). Kristianias historie. *St. Hallvard*. https://lokalhistoriewiki.no/wiki/Kristianias_historie

---

*Ende av prosjektplan v1.1 (APA 7)*