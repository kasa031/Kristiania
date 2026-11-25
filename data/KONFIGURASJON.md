# Konfigurasjon og kart (beste tilgang)

## Uten fil lokalt

Appen bruker **OpenStreetMap** som gatekart. Ingen nøkkel.

**Søk:** Stedsnavn fra appen eller adresse/gate via OpenStreetMap (Nominatim). Treff vises med nål på kartet. Krever nett (ikke offline).

## Beste kartopplevelse (anbefalt: Mapbox)

Mapbox gir tydeligere gater og bygg ved inzooming, og fungerer godt på mobil.

**Muntlig fremgangsmåte:**

1. Gå til [account.mapbox.com](https://account.mapbox.com/) og lag gratis konto.
2. Under **Access tokens** kopier token som starter med `pk.` (Default public token).
3. I prosjektmappa: kopier `data/map-config.local.json.example` til `data/map-config.local.json`.
4. Lim inn tokenet i `mapbox_access_token`.
5. La `"default_layer": "mapbox-streets"` stå i filen (eksempelfilen har dette).
6. Lagre, start `.\scripts\serve.ps1` på nytt om nødvendig, og **Ctrl+F5** i nettleseren.

Appen velger automatisk Mapbox når token finnes. Du kan fortsatt bytte lag i kartvelgeren.

**Viktig:** `map-config.local.json` skal aldri committes til git (står i `.gitignore`).

## Alternativ: Carto Voyager

1. [carto.com/basemaps/apikey](https://carto.com/basemaps/apikey) - gratis nøkkel (også privat bruk).
2. Legg `carto_basemaps_api_key` i `map-config.local.json`.
3. Sett f.eks. `"default_layer": "carto-voyager"`.

Hvis både Mapbox og Carto finnes, vinner det som står i `default_layer`, ellers Mapbox først.

## Kartet viser bare fargefelt uten gater

Da laster ikke bakgrunnskartet. Vanligste årsak: **utløpt eller ugyldig Mapbox-token** (`401` fra Mapbox). Bydelsgrenser ligger som blå/grå felt over tom bakgrunn.

**Rask løsning:** I kartvelgeren øverst, velg **Gater** (OpenStreetMap). Hard oppdatering: **Ctrl+F5**.

**Mapbox på nytt:** Opprett nytt `pk.`-token på [account.mapbox.com](https://account.mapbox.com/), oppdater `map-config.local.json`, sett `"default_layer": "mapbox-streets"`, lagre og last siden på nytt.

## Tema: Dronningensgate 1714 (gamle rådhus-stil)

Aktivert i `site-config.json` som `theme_palette: dronningensgate1714` (teglgul/teglrød, Fraunces + Newsreader).

## Gåtur - estimert tid

Appen regner **luftlinje** mellom stopp (samme som desktop-test). Standard er **4,8 km/t** gang og **5 min lesing per stopp** (`walk_speed_km_h` og `walk_dwell_minutes_per_stop` i `site-config.json`). Tallene er veiledende, ikke eksakte rutetider.

## Kun Karina (ikke API)

- `verified: true` i JSON etter sjekk mot fysiske Bull-bind (F5).