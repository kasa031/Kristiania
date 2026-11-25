/* global L */

const BIND_COLORS = {
  1: "#6b5d54",
  2: "#b24a3a",
  3: "#5c4d6a",
  4: "#8b5a3c",
  5: "#4a4e55",
};

const MARKER_KIND_FALLBACK = {
  sted: { label: "Historisk stopp", shape: "circle", color: "#b24a3a", color_active: "#9a3f32" },
  "blaa-skilt": { label: "Blå skilt", shape: "square", color: "#1e4f8a", color_active: "#163d6e" },
  funn: { label: "Arkeologisk funn", shape: "diamond", color: "#8b6914", color_active: "#6e5410" },
  person: { label: "Person", shape: "ring", color: "#5c4d6a", color_active: "#4a3e55" },
};

let MARKER_KINDS = { ...MARKER_KIND_FALLBACK };

function markerKindSpec(kindId) {
  return MARKER_KINDS[kindId] || MARKER_KIND_FALLBACK[kindId] || MARKER_KIND_FALLBACK.sted;
}

function markerColor(kindId, active = false) {
  const s = markerKindSpec(kindId);
  return active ? s.color_active || s.color : s.color;
}

function pinBoxSize() {
  return window.matchMedia("(max-width: 900px)").matches ? 36 : 26;
}

function pinHtml({ kindId, active = false, labelHtml = "", blaaRing = false }) {
  const spec = markerKindSpec(kindId);
  const mobile = window.matchMedia("(max-width: 900px)").matches;
  const base = mobile ? 18 : 16;
  const size = active ? base + (kindId === "funn" ? 4 : 6) : base;
  const color = markerColor(kindId, active);
  const ring = active
    ? `box-shadow:0 0 0 3px #fff,0 0 0 5px ${markerColor(kindId, true)};`
    : "box-shadow:0 2px 6px rgba(0,0,0,.35);";
  const blaa = blaaRing ? `outline:2px solid ${markerColor("blaa-skilt")};outline-offset:1px;` : "";
  const extra = `${ring}${blaa}`;
  if (spec.shape === "diamond") {
    return `<span class="map-pin map-pin--funn" style="background:${color};width:${size}px;height:${size}px;border:2px solid #fff;transform:rotate(45deg);${extra}"></span>`;
  }
  if (spec.shape === "square") {
    return `<span class="map-pin map-pin--blaa-skilt" style="background:${color};width:${size}px;height:${size}px;border:2px solid #fff;border-radius:4px;display:flex;align-items:center;justify-content:center;${extra}">${labelHtml}</span>`;
  }
  if (spec.shape === "ring") {
    return `<span class="map-pin map-pin--person" style="background:#fff8f0;width:${size}px;height:${size}px;border:3px solid ${color};border-radius:50%;display:flex;align-items:center;justify-content:center;${extra}"><span style="display:block;width:38%;height:38%;background:${color};border-radius:50%;"></span></span>`;
  }
  return `<span class="map-pin map-pin--sted" style="background:${color};width:${size}px;height:${size}px;border:2px solid #fff;border-radius:50%;display:flex;align-items:center;justify-content:center;${extra}">${labelHtml}</span>`;
}

function placeMarkerKind(place) {
  const { destination } = getFilters();
  if (destination === "blaa-skilt" && placeHasBlaaSkilt(place)) return "blaa-skilt";
  return "sted";
}

function shouldShowPeopleMarkers() {
  const d = getFilters().destination;
  if (d === "community" || d === "blaa-skilt") return false;
  return d === "all" || d === "historie";
}

const state = {
  places: [],
  events: [],
  episodes: [],
  tags: [],
  tagGroups: [],
  eras: [],
  centuries: [],
  milestones: [],
  bindSources: [],
  map: null,
  mapConfig: null,
  mapToken: "",
  baseLayers: {},
  activeTileLayer: null,
  activeMapLayerId: "detailed",
  placeMiniMap: null,
  routeLayer: null,
  userRouteLayer: null,
  userRouteFetchAbort: null,
  userRouteDistanceM: null,
  userRouteTargetId: null,
  userRouteRefreshTimer: null,
  userMarker: null,
  userAccuracy: null,
  markers: {},
  findMarkers: {},
  personMarkers: {},
  activeFindId: null,
  districts: [],
  chronologyEras: [],
  chronologyYearMin: -5000,
  chronologyYearMax: 1924,
  finds: [],
  people: [],
  contextEntries: [],
  blueSigns: [],
  activePersonId: null,
  activeContextId: null,
  activeBlueSignId: null,
  activeCommunityPinId: null,
  bydelerGeo: null,
  districtMapUi: null,
  activeEventId: null,
  activePlaceId: null,
  walkMode: false,
  walkIndex: 0,
  sidePanelMode: "explore",
  currentEpisodeId: "1624-ny-by",
  userPosition: null,
  followUser: true,
  geoWatchId: null,
  geoActive: false,
  exploreMarker: null,
  searchMarker: null,
  searchSuggestTimer: null,
  lastMapFitKey: "",
  communityMapPick: false,
  communityPickMarker: null,
  communityMarkers: {},
  siteConfig: {
    phase: 1,
    primary_mode: "explore",
    walk_prominent: false,
    show_source_in_ui: false,
    show_source_badge: false,
    show_bind_filter: false,
    show_bind_chips: false,
    enable_geolocation: true,
    geolocation_follow_default: true,
    explore_snap_radius_m: 140,
    explore_nearby_radius_m: 600,
    explore_nearby_list_size: 5,
    reverse_geocode_on_map_click: true,
    collapsible_filters_on_mobile: true,
  },
};

async function fetchJson(url, optional = false) {
  const res = await fetch(url);
  if (!res.ok) {
    if (optional) return null;
    throw new Error(`Kunne ikke laste ${url} (HTTP ${res.status})`);
  }
  return res.json();
}

async function loadData() {
  const [
    places,
    events,
    episodes,
    tags,
    erasDoc,
    milestones,
    siteConfig,
    mapConfig,
    mapLocal,
    chronologyDoc,
    districtsDoc,
    findsDoc,
    peopleDoc,
    contextDoc,
    blueSignsDoc,
    mapMarkersDoc,
    bydelerGeo,
  ] = await Promise.all([
      fetchJson("data/places.json"),
      fetchJson("data/events.json"),
      fetchJson("data/episodes.json"),
      fetchJson("data/tags.json"),
      fetchJson("data/eras.json"),
      fetchJson("data/milestones.json"),
      fetchJson("data/site-config.json", true),
      fetchJson("data/map-config.json"),
      fetchJson("data/map-config.local.json", true),
      fetchJson("data/chronology.json"),
      fetchJson("data/districts.json"),
      fetchJson("data/finds.json"),
      fetchJson("data/people.json"),
      fetchJson("data/context.json"),
      fetchJson("data/blue-signs.json"),
      fetchJson("data/map-markers.json"),
      fetchJson("data/bydeler.geojson"),
    ]);
  state.places = places.places;
  state.events = events.events;
  state.episodes = episodes.episodes;
  state.tags = tags.tags;
  state.tagGroups = tags.groups || [];
  state.eras = (erasDoc.eras || []).slice().sort((a, b) => (a.sort || 0) - (b.sort || 0));
  state.centuries = erasDoc.centuries || [];
  state.milestones = milestones.milestones || [];
  state.chronologyEras = (chronologyDoc.eras || []).slice().sort((a, b) => (a.sort || 0) - (b.sort || 0));
  state.chronologyYearMin = chronologyDoc.year_min ?? siteConfig.timeline_year_min ?? -5000;
  state.chronologyYearMax = Math.min(
    chronologyDoc.year_max ?? 1924,
    siteConfig.timeline_year_max ?? 1924,
  );
  state.districts = districtsDoc.districts || [];
  state.finds = findsDoc.finds || [];
  state.people = peopleDoc.people || [];
  state.contextEntries = contextDoc.entries || [];
  state.blueSigns = blueSignsDoc.signs || [];
  if (mapMarkersDoc?.kinds?.length) {
    MARKER_KINDS = Object.fromEntries(mapMarkersDoc.kinds.map((k) => [k.id, k]));
  }
  state.bydelerGeo = bydelerGeo;
  window.OsloHistorieBydel?.assignDistrictsToPlaces(state.places, state.districts);
  state.siteConfig = { ...state.siteConfig, ...(siteConfig || {}) };
  window.__KRISTIANIA_SITE__ = state.siteConfig;
  state.mapConfig = { ...mapConfig, ...(mapLocal || {}) };
  state.mapToken =
    mapLocal.mapbox_access_token || mapConfig.mapbox_access_token || "";
  if (state.siteConfig.show_source_in_ui) {
    const bindSources = await fetch("data/bind-sources.json").then((r) => r.json());
    state.bindSources = bindSources.binds || [];
  } else {
    state.bindSources = [];
  }
}

function sourceBlockHtml(item) {
  if (!state.siteConfig.show_source_in_ui) return "";
  const src = formatSource(item.source_ref);
  if (!src) return "";
  return `<p class="source">${src}</p>`;
}

function tagLabel(id) {
  return state.tags.find((t) => t.id === id)?.label || id;
}

function eraLabel(eraId) {
  return state.eras.find((e) => e.id === eraId)?.label || "";
}

function tagChipsHtml(tagIds) {
  return (tagIds || [])
    .map((t) => `<span class="chip">${tagLabel(t)}</span>`)
    .join("");
}

function centuryBucket(year) {
  if (year < -1800) return "stone";
  if (year < -500) return "bronze";
  if (year < 1000) return "iron";
  if (year < 1100) return "11";
  if (year < 1400) return "13";
  if (year < 1700) return "16";
  if (year < 1800) return "17";
  if (year < 1900) return "18";
  return "19";
}

function centuryHeading(year) {
  if (year < -1800) return "Steinalder (funn)";
  if (year < -500) return "Bronsealder";
  if (year < 1000) return "Jernalder og vikingtid";
  if (year < 1100) return "1000-tallet";
  if (year < 1400) return "1200-1300-tall";
  if (year < 1700) return "1500-1600-tall";
  if (year < 1800) return "1700-tallet";
  if (year < 1900) return "1800-tallet";
  return "1900-tallet";
}

function itemMatchesCentury(item, centuryId) {
  if (centuryId === "all") return true;
  const def = state.centuries.find((c) => c.id === centuryId);
  if (def?.from == null) {
    const y = item.year ?? item.year_from ?? item.year_to ?? 0;
    return centuryBucket(y) === centuryId;
  }
  if (item.year != null) {
    return item.year >= def.from && item.year <= def.to;
  }
  const yFrom = item.year_from ?? item.year_to;
  const yTo = item.year_to ?? item.year_from;
  if (yFrom == null && yTo == null) return false;
  const from = yFrom ?? yTo;
  const to = yTo ?? yFrom;
  return !(to < def.from || from > def.to);
}

function formatSource(ref) {
  if (!ref) return "";
  let s = `Kristianias historie, bind ${ref.bind}, s. ${ref.pages}`;
  if (ref.note) s += ` (${ref.note})`;
  return s;
}

function sourceBadgeHtml(item) {
  if (!state.siteConfig.show_source_badge) return "";
  if (item?.verified === true) return "";
  return '<span class="badge-draft">Sidetall: utkast</span>';
}

function bindSourceLinksHtml(_bind) {
  return "";
}

function mapFocusZoom() {
  return state.mapConfig?.focus_zoom || 18;
}

function resolvePreferredMapLayerId() {
  const layers = state.mapConfig?.layers || [];
  const find = (id) => layers.find((l) => l.id === id);
  const canUse = (id) => {
    const def = find(id);
    return def && buildTileLayer(def);
  };
  const requested = state.mapConfig?.default_layer;
  if (requested && canUse(requested)) return requested;
  if (state.mapToken && canUse("mapbox-streets")) return "mapbox-streets";
  if (state.mapConfig?.carto_basemaps_api_key && canUse("carto-voyager")) return "carto-voyager";
  if (canUse("detailed")) return "detailed";
  return layers.find((l) => !l.requires_token && !l.requires_carto_key)?.id || "detailed";
}

function resolveRasterTileUrl(layerDef) {
  let url = layerDef.url;
  if (!url) return null;
  const needsCartoKey =
    layerDef.requires_carto_key || url.includes("basemaps.cartocdn.com") || url.includes("cartocdn.com");
  if (needsCartoKey) {
    const cartoKey = state.mapConfig?.carto_basemaps_api_key || "";
    if (!cartoKey) return null;
    const join = url.includes("?") ? "&" : "?";
    url = `${url}${join}key=${encodeURIComponent(cartoKey)}`;
  }
  return url;
}

let mapboxBasemapFailed = false;

function attachTileLoadFallback(tileLayer, layerId) {
  if (layerId !== "mapbox-streets" && layerId !== "mapbox-satellite") return;
  if (mapboxBasemapFailed) return;
  let errors = 0;
  tileLayer.on("tileerror", () => {
    errors += 1;
    if (errors < 3 || mapboxBasemapFailed) return;
    mapboxBasemapFailed = true;
    const sel = document.getElementById("map-layer");
    const fallbackId = (state.mapConfig?.layers || []).some((l) => l.id === "detailed")
      ? "detailed"
      : "osm";
    if (!sel || ![...sel.options].some((o) => o.value === fallbackId)) return;
    sel.value = fallbackId;
    setMapLayer(fallbackId);
  });
}

function buildTileLayer(layerDef) {
  const token = state.mapToken;
  if (layerDef.provider === "mapbox") {
    if (!token) return null;
    const style = layerDef.style || "mapbox/streets-v12";
    const url = `https://api.mapbox.com/styles/v1/${style}/tiles/256/{z}/{x}/{y}@2x?access_token=${encodeURIComponent(token)}`;
    return L.tileLayer(url, {
      attribution:
        '&copy; <a href="https://www.mapbox.com/">Mapbox</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: layerDef.max_zoom || 22,
    });
  }
  const rasterUrl = resolveRasterTileUrl(layerDef);
  if (!rasterUrl) return null;
  const opts = {
    attribution: layerDef.attribution || "",
    maxZoom: layerDef.max_zoom || 20,
  };
  if (layerDef.subdomains) opts.subdomains = layerDef.subdomains;
  return L.tileLayer(rasterUrl, opts);
}

function setMapLayer(layerId) {
  const layerDef = (state.mapConfig?.layers || []).find((l) => l.id === layerId);
  if (!layerDef || !state.map) return;
  const next = buildTileLayer(layerDef);
  if (!next) return;
  if (state.activeTileLayer) state.map.removeLayer(state.activeTileLayer);
  next.addTo(state.map);
  attachTileLoadFallback(next, layerId);
  state.activeTileLayer = next;
  state.activeMapLayerId = layerId;
  state.map.setMaxZoom(layerDef.max_zoom || state.mapConfig.max_zoom || 20);
  const place = state.places.find((p) => p.id === state.activePlaceId);
  if (place) initPlaceMiniMap(place);
}

function populateMapLayers() {
  const sel = document.getElementById("map-layer");
  if (!sel || !state.mapConfig?.layers) return;
  sel.innerHTML = "";
  const token = state.mapToken;
  let defaultId = resolvePreferredMapLayerId();
  const hasDetailed = state.mapConfig.layers.some((l) => l.id === "detailed");
  (state.mapConfig.layers || []).forEach((layer) => {
    if (layer.id === "osm" && hasDetailed) return;
    if (layer.requires_token && !token) return;
    if (layer.requires_carto_key && !state.mapConfig.carto_basemaps_api_key) return;
    const opt = document.createElement("option");
    opt.value = layer.id;
    opt.textContent = layer.label;
    sel.appendChild(opt);
  });
  if (![...sel.options].some((o) => o.value === defaultId)) {
    defaultId = sel.options[0]?.value || defaultId;
  }
  sel.value = defaultId;
  setMapLayer(defaultId);
  if (!sel.dataset.bound) {
    sel.dataset.bound = "1";
    sel.addEventListener("change", () => setMapLayer(sel.value));
  }
}

function normalizeSearchQuery(query) {
  return String(query || "")
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{M}/gu, "");
}

function searchPlacesLocal(query) {
  const q = normalizeSearchQuery(query);
  if (q.length < 2) return [];
  return filterPlaces()
    .filter((p) => {
      const hay = normalizeSearchQuery(`${p.name} ${p.standpoint || ""} ${p.id.replace(/-/g, " ")}`);
      return hay.includes(q);
    })
    .slice(0, 8);
}

function hideSearchSuggest() {
  const list = document.getElementById("map-search-suggest");
  if (list) {
    list.hidden = true;
    list.innerHTML = "";
  }
}

function setSearchStatus(message) {
  const el = document.getElementById("map-search-status");
  if (!el) return;
  if (!message) {
    el.hidden = true;
    el.textContent = "";
    return;
  }
  el.hidden = false;
  el.textContent = message;
}

function clearSearchMarker() {
  if (state.searchMarker) {
    state.searchMarker.remove();
    state.searchMarker = null;
  }
}

function setSearchPin(lat, lng, label) {
  clearSearchMarker();
  if (!state.map) return;
  const icon = L.divIcon({
    className: "search-pin",
    html: '<span class="search-pin-dot" aria-hidden="true"></span>',
    iconSize: [28, 28],
    iconAnchor: [14, 26],
  });
  state.searchMarker = L.marker([lat, lng], { icon, zIndexOffset: 250 }).addTo(state.map);
  state.searchMarker.bindPopup(label || "Søketreff");
}

function renderDetailForSearchPoint(lat, lng, label) {
  const el = document.getElementById("detail-panel");
  if (!el) return;
  const snap = exploreSnapRadiusM();
  const nearest = placesByDistance(lat, lng, snap * 4, 3);
  let body = `<p>Adressen eller stedet er markert på kartet med en blå nål.</p>`;
  if (nearest.length) {
    body += `<p>Nærmeste kuraterte stopp:</p><ul class="explore-near-list">`;
    nearest.forEach(({ place, meters }) => {
      body += `<li><button type="button" class="linkish nearby-pick" data-place-id="${place.id}">${place.name} (${formatDistanceM(meters)})</button></li>`;
    });
    body += `</ul>`;
  }
  el.innerHTML = `<h3>${label}</h3>${body}<p class="detail-actions"><button type="button" class="detail-back linkish" data-action="clear-selection">Lukk</button></p>`;
  el.querySelectorAll(".nearby-pick").forEach((btn) => {
    btn.addEventListener("click", () => selectPlace(btn.dataset.placeId));
  });
  focusDetailPanel();
}

const NOMINATIM_HEADERS = {
  "Accept-Language": "nb",
  Accept: "application/json",
  "User-Agent": "KristianiaHistorieKart/1.0 (educational project)",
};

const OSLO_VIEWBOX = "10.55,60.05,10.95,59.85";

function parseStreetQuery(query) {
  const raw = String(query || "").trim();
  const m = raw.match(/^(.+?)\s+(\d+\s*[a-zA-ZæøåÆØÅ]?)$/);
  if (m) return { street: m[1].trim(), houseNumber: m[2].trim() };
  return { street: raw, houseNumber: null };
}

function looksLikeStreetOnly(query) {
  const { street, houseNumber } = parseStreetQuery(query);
  if (houseNumber) return false;
  if (street.length < 4) return false;
  if (/\d/.test(street)) return false;
  return /(gate|gata|gaten|vei|veien|veg|allé|alle|stredet|plass|torg|svingen|bakken)\b/i.test(street);
}

function roadMatchesQuery(road, streetQuery) {
  if (!road) return false;
  const a = normalizeSearchQuery(road);
  const b = normalizeSearchQuery(parseStreetQuery(streetQuery).street);
  return a === b || a.includes(b) || b.includes(a);
}

function compareHouseNumbers(a, b) {
  const na = parseInt(String(a).replace(/\D/g, ""), 10) || 0;
  const nb = parseInt(String(b).replace(/\D/g, ""), 10) || 0;
  if (na !== nb) return na - nb;
  return String(a).localeCompare(String(b), "nb");
}

function labelFromNominatimRow(row) {
  const addr = row.address || {};
  const road = addr.road || addr.pedestrian || addr.footway;
  const hn = addr.house_number;
  if (road && hn) return `${road} ${hn}`;
  if (road) return road;
  const parts = (row.display_name || "").split(",").map((s) => s.trim());
  return parts.slice(0, 2).join(", ") || String(row.display_name || "");
}

function boundsFromRows(rows) {
  const lats = [];
  const lngs = [];
  rows.forEach((r) => {
    const lat = parseFloat(r.lat);
    const lon = parseFloat(r.lon);
    if (Number.isFinite(lat) && Number.isFinite(lon)) {
      lats.push(lat);
      lngs.push(lon);
    }
    if (r.boundingbox?.length === 4) {
      lats.push(parseFloat(r.boundingbox[0]), parseFloat(r.boundingbox[1]));
      lngs.push(parseFloat(r.boundingbox[2]), parseFloat(r.boundingbox[3]));
    }
  });
  if (!lats.length) return null;
  return [
    [Math.min(...lats), Math.min(...lngs)],
    [Math.max(...lats), Math.max(...lngs)],
  ];
}

function centerFromBounds(bounds) {
  if (!bounds) return { lat: 59.91, lng: 10.75 };
  return {
    lat: (bounds[0][0] + bounds[1][0]) / 2,
    lng: (bounds[0][1] + bounds[1][1]) / 2,
  };
}

async function nominatimSearchParams(params) {
  params.set("format", "json");
  params.set("addressdetails", "1");
  params.set("viewbox", OSLO_VIEWBOX);
  params.set("bounded", "1");
  const url = `https://nominatim.openstreetmap.org/search?${params}`;
  try {
    const res = await fetch(url, { headers: NOMINATIM_HEADERS });
    if (!res.ok) return [];
    return (await res.json()) || [];
  } catch {
    return [];
  }
}

function buildStreetSuggestItems(rows, streetQuery) {
  const { street } = parseStreetQuery(streetQuery);
  const houses = new Map();
  const matchedRows = [];

  rows.forEach((row) => {
    const addr = row.address || {};
    const road = addr.road || addr.pedestrian || addr.footway || "";
    if (!roadMatchesQuery(road, street)) {
      const hay = normalizeSearchQuery(row.display_name || "");
      const needle = normalizeSearchQuery(street);
      if (!hay.includes(needle)) return;
    }
    matchedRows.push(row);
    const hn = addr.house_number;
    if (road && hn) {
      const key = String(hn).toLowerCase();
      if (!houses.has(key)) {
        houses.set(key, {
          lat: parseFloat(row.lat),
          lng: parseFloat(row.lon),
          label: `${road} ${hn}`,
          hint: [addr.suburb, addr.city_district, addr.postcode].filter(Boolean).join(" · "),
        });
      }
    }
  });

  const displayRoad =
    houses.size > 0
      ? [...houses.values()][0].label.replace(/\s+\d+.*$/, "").trim()
      : street;
  const items = [];
  const bounds = boundsFromRows(matchedRows);
  const center = centerFromBounds(bounds);

  if (bounds || houses.size > 0) {
    items.push({
      kind: "street",
      label: `Hele ${displayRoad}`,
      lat: center.lat,
      lng: center.lng,
      bounds,
    });
  }

  [...houses.entries()]
    .sort((a, b) => compareHouseNumbers(a[0], b[0]))
    .slice(0, 24)
    .forEach(([, h]) => {
      items.push({
        kind: "address",
        label: h.label,
        hint: h.hint,
        lat: h.lat,
        lng: h.lng,
      });
    });

  if (items.length <= 1 && matchedRows.length) {
    const dedup = new Map();
    matchedRows.forEach((row) => {
      const label = labelFromNominatimRow(row);
      const key = normalizeSearchQuery(label);
      if (!dedup.has(key)) {
        dedup.set(key, {
          kind: "address",
          label,
          lat: parseFloat(row.lat),
          lng: parseFloat(row.lon),
        });
      }
    });
    return items.length ? items : [...dedup.values()].slice(0, 8);
  }

  return items;
}

async function nominatimStreetSearch(streetQuery) {
  const { street, houseNumber } = parseStreetQuery(streetQuery);
  const structured = new URLSearchParams({
    street: houseNumber ? `${houseNumber} ${street}` : street,
    city: "Oslo",
    country: "Norway",
    limit: "40",
  });
  let rows = await nominatimSearchParams(structured);
  if (rows.length < 4) {
    const free = new URLSearchParams({
      q: houseNumber ? `${street} ${houseNumber}, Oslo, Norway` : `${street}, Oslo, Norway`,
      countrycodes: "no",
      limit: "40",
    });
    const extra = await nominatimSearchParams(free);
    const seen = new Set(rows.map((r) => r.place_id));
    extra.forEach((r) => {
      if (!seen.has(r.place_id)) rows.push(r);
    });
  }
  return buildStreetSuggestItems(rows, street);
}

async function nominatimForwardSearch(query) {
  const { street, houseNumber } = parseStreetQuery(query);
  if (houseNumber || looksLikeStreetOnly(query)) {
    return nominatimStreetSearch(query);
  }
  const params = new URLSearchParams({
    q: query,
    limit: "12",
    countrycodes: "no",
  });
  const data = await nominatimSearchParams(params);
  const seen = new Set();
  const out = [];
  for (const row of data) {
    const label = labelFromNominatimRow(row);
    const key = `${normalizeSearchQuery(label)}|${row.lat}|${row.lon}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({
      kind: "address",
      lat: parseFloat(row.lat),
      lng: parseFloat(row.lon),
      label,
      hint: (row.address?.suburb || row.address?.city_district) ?? "",
    });
    if (out.length >= 8) break;
  }
  return out;
}

function searchSuggestOptionHtml(item, index) {
  const streetCls = item.kind === "street" ? " map-search-option--street" : "";
  let prefix = "Adresse";
  if (item.kind === "place") prefix = "Sted";
  else if (item.kind === "street") prefix = "";
  else if (item.kind === "address" && item.label.match(/\d/)) prefix = "Gatenr.";
  const title = item.kind === "street" ? item.label : `${prefix ? `${prefix}: ` : ""}${item.label}`;
  const hint = item.hint ? `<span class="map-search-option-hint">${item.hint}</span>` : "";
  return `<li><button type="button" role="option" class="map-search-option${streetCls}" data-suggest-index="${index}">${title}${hint}</button></li>`;
}

function showSearchSuggest(items) {
  const list = document.getElementById("map-search-suggest");
  if (!list) return;
  if (!items.length) {
    hideSearchSuggest();
    return;
  }
  list.hidden = false;
  list.innerHTML = items.map((item, i) => searchSuggestOptionHtml(item, i)).join("");
  list._suggestItems = items;
  list.querySelectorAll(".map-search-option").forEach((btn) => {
    btn.addEventListener("click", () => {
      const idx = parseInt(btn.dataset.suggestIndex, 10);
      const pick = list._suggestItems?.[idx];
      if (pick) applySearchResult(pick);
    });
  });
}

async function applySearchResult(result) {
  hideSearchSuggest();
  setSearchStatus("");
  const input = document.getElementById("map-search");
  if (input) input.value = result.label;

  if (result.kind === "place") {
    clearSearchMarker();
    selectPlace(result.placeId, { pan: true });
    return;
  }

  const { lat, lng, label, bounds } = result;
  if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
    setSearchStatus("Fant ikke koordinater for søket.");
    return;
  }

  setSearchPin(lat, lng, label);
  if (state.exploreMarker) {
    state.exploreMarker.remove();
    state.exploreMarker = null;
  }
  if (result.kind === "street" && bounds?.length === 2) {
    state.map.fitBounds(bounds, { padding: [36, 36], maxZoom: 17, animate: true });
  } else {
    state.map.setView([lat, lng], mapFocusZoom(), { animate: true });
  }

  const snap = exploreSnapRadiusM();
  const hit = placesByDistance(lat, lng, snap, 1)[0];
  if (hit) {
    selectPlace(hit.place.id, { pan: false });
    return;
  }

  state.activePlaceId = null;
  state.activeEventId = null;
  renderTimeline();
  renderDetailForSearchPoint(lat, lng, label);
  refreshMarkers();
}

async function runMapSearch(query) {
  const q = String(query || "").trim();
  if (q.length < 2) {
    setSearchStatus("Skriv minst to tegn for å søke.");
    return;
  }

  const local = searchPlacesLocal(q).map((p) => ({
    kind: "place",
    label: p.name,
    placeId: p.id,
    lat: p.lat,
    lng: p.lng,
  }));

  const exact = local.filter((p) => normalizeSearchQuery(p.label) === normalizeSearchQuery(q));
  if (exact.length === 1) {
    await applySearchResult(exact[0]);
    return;
  }
  if (local.length === 1) {
    await applySearchResult(local[0]);
    return;
  }
  if (local.length > 1) {
    showSearchSuggest(local);
    setSearchStatus("Velg et forslag i listen.");
    return;
  }

  setSearchStatus("Søker adresse...");
  const remote = await nominatimForwardSearch(q);
  if (!remote.length) {
    setSearchStatus("Ingen treff. Prøv gate, torg eller stedsnavn.");
    hideSearchSuggest();
    return;
  }

  if (remote.length === 1 && remote[0].kind !== "street") {
    await applySearchResult(remote[0]);
    return;
  }
  showSearchSuggest(remote);
  setSearchStatus(
    looksLikeStreetOnly(q)
      ? "Velg hele gaten eller et gatenummer."
      : "Velg forslag i listen.",
  );
}

function onSearchInput() {
  const input = document.getElementById("map-search");
  if (!input || state.siteConfig.search_places_and_addresses === false) return;
  clearTimeout(state.searchSuggestTimer);
  state.searchSuggestTimer = setTimeout(async () => {
    const q = String(input.value || "").trim();
    const local = searchPlacesLocal(q).map((p) => ({
      kind: "place",
      label: p.name,
      placeId: p.id,
      lat: p.lat,
      lng: p.lng,
    }));
    if (local.length) {
      showSearchSuggest(local);
      setSearchStatus("");
      return;
    }
    if (q.length >= 3 && (looksLikeStreetOnly(q) || parseStreetQuery(q).houseNumber)) {
      setSearchStatus("Søker gate...");
      const remote = await nominatimForwardSearch(q);
      if (remote.length) {
        showSearchSuggest(remote);
        setSearchStatus(
          looksLikeStreetOnly(q) ? "Velg hele gaten eller et gatenummer." : "Velg forslag i listen.",
        );
      } else {
        hideSearchSuggest();
        setSearchStatus("");
      }
      return;
    }
    hideSearchSuggest();
    setSearchStatus("");
  }, 420);
}

function destroyPlaceMiniMap() {
  if (state.placeMiniMap) {
    state.placeMiniMap.remove();
    state.placeMiniMap = null;
  }
}

function initPlaceMiniMap(place) {
  destroyPlaceMiniMap();
  const el = document.getElementById("place-mini-map");
  if (!el || place?.lat == null || place?.lng == null) return;
  const layerId = state.activeMapLayerId || state.mapConfig?.default_layer || "detailed";
  const layerDef = (state.mapConfig?.layers || []).find((l) => l.id === layerId);
  if (!layerDef) return;
  const tile = buildTileLayer(layerDef);
  if (!tile) return;
  const zoom = Math.min(mapFocusZoom(), layerDef.max_zoom || 20);
  state.placeMiniMap = L.map(el, {
    zoomControl: false,
    attributionControl: true,
    dragging: true,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    keyboard: false,
  }).setView([place.lat, place.lng], zoom);
  tile.addTo(state.placeMiniMap);
  L.circleMarker([place.lat, place.lng], {
    radius: 7,
    color: markerColor("sted"),
    weight: 2,
    fillColor: markerColor("sted"),
    fillOpacity: 0.9,
  }).addTo(state.placeMiniMap);
  requestAnimationFrame(() => {
    state.placeMiniMap?.invalidateSize();
  });
}

function mediaFigureHtml(item) {
  if (!item?.image?.url) return "";
  const credit = item.image.credit
    ? `<figcaption class="detail-figure-credit">${item.image.credit}</figcaption>`
    : "";
  return `<figure class="detail-figure"><img src="${item.image.url}" alt="" loading="lazy" width="640" height="auto" />${credit}</figure>`;
}

function personByRef(ref) {
  if (!ref) return null;
  return (
    state.people.find((p) => p.id === ref) ||
    state.people.find((p) => p.name === ref) ||
    null
  );
}

function peopleLinksHtml(place) {
  const refs = place?.related_people || [];
  if (!refs.length || !state.people.length) return "";
  const links = refs
    .map((ref) => {
      const person = personByRef(ref);
      if (!person) return "";
      return `<button type="button" class="linkish person-link" data-person-id="${person.id}">${person.name}</button>`;
    })
    .filter(Boolean);
  if (!links.length) return "";
  return `<p class="detail-people"><span class="links-label">Personer:</span> ${links.join(" · ")}</p>`;
}

function filterContextEntries() {
  const { destination, bind, century, tag, episode, chronology, yearMin, yearMax } = getFilters();
  if (destination === "community") return [];
  return state.contextEntries.filter((ctx) => {
    if (!itemMatchesYearRange(ctx, yearMin, yearMax)) return false;
    if (!itemMatchesChronology(ctx, chronology)) return false;
    if (bind !== "all" && String(ctx.bind) !== bind) return false;
    if (!itemMatchesCentury(ctx, century)) return false;
    if (tag !== "all" && !(ctx.tags || []).includes(tag)) return false;
    if (episode !== "all" && (ctx.place_ids || []).length) {
      const linked = ctx.place_ids.some((pid) => {
        const p = state.places.find((x) => x.id === pid);
        return p && placeMatchesEpisode(p, episode);
      });
      if (!linked) return false;
    }
    return true;
  });
}

function placeVisualHtml(item) {
  const parts = [];
  parts.push(mediaFigureHtml(item));
  if (item?.lat != null && item?.lng != null) {
    parts.push(
      '<div id="place-mini-map" class="place-mini-map" aria-label="Kartutsnitt rundt stoppet"></div>',
    );
  }
  if (item?.standpoint) {
    const lead = state.walkMode ? "Stå her" : "Se herfra";
    parts.push(`<p class="standpoint"><strong>${lead}:</strong> ${item.standpoint}</p>`);
  }
  return parts.join("");
}

function bindChipHtml(bind) {
  if (!state.siteConfig.show_bind_chips) return "";
  return `<span class="chip bind">Bind ${bind}</span>`;
}

function runUiAction(action) {
  if (!action) return;
  if (action === "explore") {
    setSidePanelMode("explore");
    document.getElementById("mode-tab-explore")?.focus({ preventScroll: true });
    return;
  }
  if (action === "routes") {
    setSidePanelMode("routes");
    document.getElementById("mode-tab-routes")?.focus({ preventScroll: true });
    return;
  }
  if (action === "locate") {
    document.querySelector(".panel-map")?.scrollIntoView({ behavior: "smooth", block: "start" });
    document.getElementById("btn-map-locate")?.click();
    return;
  }
  if (action === "search" || action === "home-search") {
    if (isHomeActive()) dismissHome("explore");
    else {
      document.querySelector(".panel-map")?.scrollIntoView({ behavior: "smooth", block: "start" });
      const input = document.getElementById("map-search");
      input?.focus({ preventScroll: false });
    }
    return;
  }
  if (action === "home-routes") {
    dismissHome("routes");
    return;
  }
  if (action === "home-back") {
    showHomeScreen();
    return;
  }
  if (action === "home-share" || action === "community-tag") {
    if (isHomeActive()) dismissHome("explore", { openCommunityTag: true });
    else openCommunityTagDialog();
    return;
  }
  if (action === "reset-filters") {
    resetFilters();
    document.getElementById("btn-reset-filters")?.focus({ preventScroll: true });
    return;
  }
  if (action === "map-focus") {
    document.querySelector(".panel-map")?.scrollIntoView({ behavior: "smooth", block: "start" });
    const mapEl = document.getElementById("map");
    if (mapEl && typeof mapEl.focus === "function") mapEl.focus({ preventScroll: true });
  }
}

let uiJumpLinksBound = false;

function bindUiJumpLinks() {
  if (uiJumpLinksBound) return;
  uiJumpLinksBound = true;
  document.body.addEventListener("click", (e) => {
    const jump = e.target.closest("[data-ui-action]");
    if (!jump || jump.closest("a[href]")) return;
    e.preventDefault();
    runUiAction(jump.dataset.uiAction);
  });
}

function setNearbyIdleHint() {
  const statusEl = document.getElementById("nearby-status");
  if (!statusEl) return;
  statusEl.dataset.nearbyIdle = "true";
  statusEl.textContent = "Trykk Min posisjon over kartet for å se steder rundt deg.";
}

function isHomeActive() {
  return document.body.classList.contains("home-active");
}

function homeHistoryState(view, mode = "explore") {
  return { kristianiaView: view, mode };
}

function getAppBase() {
  const script = document.querySelector('script[src*="app.js"]');
  if (!script?.src) return "";
  try {
    const u = new URL(script.src, window.location.href);
    return u.pathname.replace(/\/js\/app\.js.*$/i, "") || "";
  } catch {
    return "";
  }
}

function normalizeRoutePath(pathname = window.location.pathname) {
  const base = getAppBase();
  let p = pathname || "/";
  if (base && p.startsWith(base)) p = p.slice(base.length) || "/";
  p = p.replace(/\/index\.html$/i, "");
  if (!p.startsWith("/")) p = `/${p}`;
  if (p.length > 1 && p.endsWith("/")) p = p.slice(0, -1);
  return p || "/";
}

function parseAppRoute() {
  const p = normalizeRoutePath();
  if (p === "/" || p === "/home") return { view: "home", mode: "explore" };
  if (p === "/kart") return { view: "app", mode: "explore" };
  if (p === "/tur") return { view: "app", mode: "routes" };
  return null;
}

function routeUrl(view, mode = "explore") {
  const base = getAppBase();
  let segment = "/home";
  if (view !== "home") segment = mode === "routes" ? "/tur" : "/kart";
  return `${base}${segment}`;
}

function currentSearchSuffix() {
  const q = window.location.search;
  return q && q !== "?" ? q : "";
}

function writeAppRoute(mode, options = {}) {
  const url = routeUrl("app", mode) + currentSearchSuffix();
  const st = homeHistoryState("app", mode);
  if (options.replace) history.replaceState(st, "", url);
  else history.pushState(st, "", url);
}

function writeHomeRoute(options = {}) {
  const url = routeUrl("home", "explore") + currentSearchSuffix();
  const st = homeHistoryState("home", "explore");
  if (options.replace) history.replaceState(st, "", url);
  else history.pushState(st, "", url);
}

function applyRouteFromUrl(options = {}) {
  const parsed = parseAppRoute();
  const canonical = parsed || { view: "home", mode: "explore" };
  const needCanonicalUrl =
    !parsed || normalizeRoutePath() === "/" || /\/index\.html$/i.test(window.location.pathname);
  if (needCanonicalUrl || options.forceUrl) {
    const url =
      (canonical.view === "home"
        ? routeUrl("home", "explore")
        : routeUrl("app", canonical.mode)) + currentSearchSuffix();
    const st = homeHistoryState(canonical.view === "home" ? "home" : "app", canonical.mode);
    history.replaceState(st, "", url);
  }
  if (canonical.view === "home") {
    applyHomeScreenDom();
    return;
  }
  if (isHomeActive()) {
    leaveHomeScreenDom(canonical.mode);
  } else {
    setSidePanelMode(canonical.mode, { skipHomeDismiss: true, skipRouteSync: true });
  }
}

function wakeMapAfterHomeDismiss(nextMode) {
  const wakeMap = () => {
    state.map?.invalidateSize();
    state.districtMapUi?.restyle?.();
  };
  requestAnimationFrame(() => {
    wakeMap();
    window.setTimeout(wakeMap, 150);
    if (nextMode === "routes") {
      document.querySelector(".panel-side")?.scrollIntoView({ behavior: "smooth", block: "start" });
      document.getElementById("mode-tab-routes")?.focus({ preventScroll: true });
    } else {
      const mapPanel = document.querySelector(".panel-map");
      if (mapPanel && window.matchMedia("(max-width: 900px)").matches) {
        mapPanel.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      const input = document.getElementById("map-search");
      if (input) {
        window.setTimeout(() => input.focus({ preventScroll: true }), 80);
      }
    }
  });
}

function applyHomeScreenDom() {
  const home = document.getElementById("home-screen");
  if (home) home.hidden = false;
  document.body.classList.add("home-active");
  document.body.classList.remove("home-dismissed");
  window.scrollTo({ top: 0, behavior: "smooth" });
  requestAnimationFrame(() => state.map?.invalidateSize());
}

function leaveHomeScreenDom(nextMode = "explore") {
  document.body.classList.add("home-ever");
  const home = document.getElementById("home-screen");
  if (home) home.hidden = true;
  document.body.classList.remove("home-active");
  document.body.classList.add("home-dismissed");
  if (nextMode === "routes") {
    setSidePanelMode("routes", { skipHomeDismiss: true });
    renderEpisodeCards();
  } else {
    setSidePanelMode("explore", { skipHomeDismiss: true });
  }
  wakeMapAfterHomeDismiss(nextMode);
}

function dismissHome(nextMode = "explore", options = {}) {
  if (!isHomeActive()) return;
  leaveHomeScreenDom(nextMode);
  if (!options.skipHistory) writeAppRoute(nextMode);
  if (options.openCommunityTag) {
    window.setTimeout(() => openCommunityTagDialog(), 250);
  }
}

function showHomeScreen(options = {}) {
  if (state.walkMode) {
    exitWalkMode({ returnMode: "explore" });
  }
  clearSelection();
  if (!options.fromHistory && !isHomeActive()) writeHomeRoute();
  applyHomeScreenDom();
}

function setSidePanelMode(mode, options = {}) {
  if (!options.skipHomeDismiss && isHomeActive()) {
    dismissHome(mode === "routes" ? "routes" : "explore");
    return;
  }
  const isExplore = mode === "explore";
  state.sidePanelMode = mode;
  const explore = document.getElementById("panel-explore");
  const routes = document.getElementById("panel-routes");
  const tabExplore = document.getElementById("mode-tab-explore");
  const tabRoutes = document.getElementById("mode-tab-routes");
  if (explore) explore.hidden = !isExplore;
  if (routes) routes.hidden = isExplore;
  if (tabExplore) {
    tabExplore.classList.toggle("active", isExplore);
    tabExplore.setAttribute("aria-selected", isExplore ? "true" : "false");
  }
  if (tabRoutes) {
    tabRoutes.classList.toggle("active", !isExplore);
    tabRoutes.setAttribute("aria-selected", isExplore ? "false" : "true");
  }
  document.body.classList.toggle("side-mode-explore", isExplore);
  document.body.classList.toggle("side-mode-routes", !isExplore);
  if (!options.skipRouteSync && !isHomeActive()) {
    writeAppRoute(mode, { replace: true });
  }
  requestAnimationFrame(() => state.map?.invalidateSize());
  if (!isExplore) renderEpisodeCards();
  if (isExplore && !state.walkMode && !state.activePlaceId && !state.activeEventId) {
    renderExploreWelcome();
  }
}

function exitWalkMode(options = {}) {
  const returnMode = options.returnMode || "routes";
  state.walkMode = false;
  state.walkIndex = 0;
  document.body.classList.remove("side-mode-walking");
  const epSel = document.getElementById("filter-episode");
  if (epSel) epSel.value = "all";
  state.lastMapFitKey = "";
  clearSelection();
  updateWalkBar();
  refreshWalkRoute();
  refreshMarkers();
  renderEpisodeCards();
  onFilterChange();
  if (returnMode === "explore") {
    setSidePanelMode("explore");
  } else {
    setSidePanelMode("routes");
  }
}

function applyBranding() {
  const cfg = state.siteConfig;
  const name = cfg.app_name || "Kristiania";
  const title = cfg.app_title || `${name} | Kart og historie`;
  document.title = title;
  const homeTitle = document.getElementById("masthead-title");
  if (homeTitle) homeTitle.textContent = name;
  const tagline = document.getElementById("masthead-tagline");
  const dekText = cfg.masthead_dek || cfg.app_tagline;
  if (tagline && dekText) {
    tagline.textContent = dekText;
  } else if (tagline && cfg.masthead_edition) {
    tagline.textContent = cfg.masthead_edition;
  }
  const foot = document.getElementById("site-footer-text");
  if (foot && cfg.app_footer) foot.textContent = cfg.app_footer;
  const rubric = document.getElementById("masthead-rubric");
  if (rubric && cfg.masthead_rubric) rubric.textContent = cfg.masthead_rubric;
  const homeKicker = document.getElementById("home-kicker");
  if (homeKicker) {
    if (cfg.home_kicker) {
      homeKicker.textContent = cfg.home_kicker;
      homeKicker.hidden = false;
    } else {
      homeKicker.hidden = true;
    }
  }
  const homeLead = document.getElementById("home-lead");
  if (homeLead) {
    if (cfg.home_lead) {
      homeLead.textContent = cfg.home_lead;
      homeLead.hidden = false;
    } else {
      homeLead.hidden = true;
    }
  }
  const homeHeadline = document.getElementById("home-headline");
  if (homeHeadline && cfg.home_headline) homeHeadline.textContent = cfg.home_headline;
  const homeSearchHint = document.getElementById("home-search-hint");
  if (homeSearchHint && cfg.home_search_hint) homeSearchHint.textContent = cfg.home_search_hint;
  const homeRoutesHint = document.getElementById("home-routes-hint");
  if (homeRoutesHint && cfg.home_routes_hint) homeRoutesHint.textContent = cfg.home_routes_hint;
  const homeShareHint = document.getElementById("home-share-hint");
  if (homeShareHint && cfg.home_share_hint) homeShareHint.textContent = cfg.home_share_hint;
  const shareBtn = document.getElementById("home-btn-share");
  if (shareBtn) shareBtn.hidden = cfg.community_tags_enabled === false;
  const mapShareBtn = document.getElementById("btn-map-share");
  if (mapShareBtn) mapShareBtn.hidden = cfg.community_tags_enabled === false;
  const communityDestOpt = document.getElementById("filter-destination-community");
  if (communityDestOpt) communityDestOpt.hidden = cfg.community_tags_enabled === false;
  const homeJubilee = document.getElementById("home-jubilee-note");
  if (homeJubilee) {
    if (cfg.home_jubilee_note) {
      homeJubilee.textContent = cfg.home_jubilee_note;
      homeJubilee.hidden = false;
    } else {
      homeJubilee.hidden = true;
    }
  }
  const routesLead = document.getElementById("routes-panel-lead");
  if (routesLead && cfg.routes_panel_lead) routesLead.textContent = cfg.routes_panel_lead;
  const backHome = document.getElementById("btn-back-home");
  if (backHome && cfg.home_back_label) backHome.textContent = cfg.home_back_label;
  const pitch = document.getElementById("masthead-pitch");
  if (pitch) {
    if (cfg.masthead_pitch) {
      pitch.textContent = cfg.masthead_pitch;
      pitch.hidden = false;
    } else {
      pitch.hidden = true;
    }
  }
  if (cfg.show_home_on_load === false) {
    document.body.classList.remove("home-active");
    document.body.classList.add("home-dismissed", "home-ever");
    const home = document.getElementById("home-screen");
    if (home) home.hidden = true;
  }
  document.body.classList.toggle("theme-avis-1880", cfg.theme_layout === "avis1880");
  document.body.classList.toggle("theme-slotts1848", cfg.theme_palette === "slotts1848");
  document.body.classList.toggle("theme-dronningensgate1714", cfg.theme_palette === "dronningensgate1714");
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  if (themeMeta) {
    themeMeta.setAttribute(
      "content",
      cfg.theme_palette === "dronningensgate1714" ? "#2a221c" : "#2c3230",
    );
  }
  renderMapLegend();
}

function applySiteUi() {
  const locateBtn = document.getElementById("btn-map-locate");
  if (locateBtn) {
    locateBtn.hidden = !state.siteConfig.enable_geolocation;
  }
  state.followUser = state.siteConfig.geolocation_follow_default !== false;
  const filtersWrap = document.getElementById("filters-wrap");
  if (filtersWrap && state.siteConfig.collapsible_filters_on_mobile) {
    filtersWrap.classList.add("filters-collapsible");
    if (window.matchMedia("(max-width: 900px)").matches) {
      filtersWrap.open = false;
    }
  }
  const nearbyWrap = document.getElementById("nearby-wrap");
  if (nearbyWrap && window.matchMedia("(max-width: 900px)").matches) {
    nearbyWrap.open = false;
  }
  const filtersAdvanced = document.getElementById("filters-advanced");
  if (filtersAdvanced && window.matchMedia("(max-width: 900px)").matches) {
    filtersAdvanced.open = false;
  }
}

function scrollTimelineToActive() {
  requestAnimationFrame(() => {
    const list = document.getElementById("timeline-list");
    const active = list?.querySelector(".event-card.active");
    active?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  });
}

function haversineMeters(a, b) {
  const R = 6371000;
  const toRad = (d) => (d * Math.PI) / 180;
  const dLat = toRad(b.lat - a.lat);
  const dLng = toRad(b.lng - a.lng);
  const lat1 = toRad(a.lat);
  const lat2 = toRad(b.lat);
  const x =
    Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLng / 2) ** 2;
  return Math.round(2 * R * Math.asin(Math.sqrt(x)));
}

function walkSpeedMetersPerMinute() {
  const kmh = Number(state.siteConfig?.walk_speed_km_h) || 4.8;
  return (kmh * 1000) / 60;
}

function walkDwellMinutesPerStop() {
  const n = Number(state.siteConfig?.walk_dwell_minutes_per_stop);
  return Number.isFinite(n) && n >= 0 ? n : 5;
}

function walkMinutesForMeters(meters) {
  if (!meters || meters <= 0) return 0;
  return meters / walkSpeedMetersPerMinute();
}

function formatWalkMinutes(totalMin) {
  if (totalMin < 1) return "under 1 min";
  const rounded = Math.max(1, Math.round(totalMin));
  if (rounded < 60) return `ca. ${rounded} min`;
  const h = Math.floor(rounded / 60);
  const rest = rounded % 60;
  if (rest === 0) return `ca. ${h} t`;
  return `ca. ${h} t ${rest} min`;
}

function formatDistanceMeters(meters) {
  if (meters < 1000) return `ca. ${meters} m`;
  return `ca. ${(meters / 1000).toFixed(1)} km`;
}

function formatWalkLeg(meters) {
  return `${formatDistanceMeters(meters)} · ${formatWalkMinutes(walkMinutesForMeters(meters))}`;
}

function routeLengthMeters(places) {
  if (!places || places.length < 2) return 0;
  let sum = 0;
  for (let i = 1; i < places.length; i += 1) {
    sum += haversineMeters(
      { lat: places[i - 1].lat, lng: places[i - 1].lng },
      { lat: places[i].lat, lng: places[i].lng },
    );
  }
  return sum;
}

function legLengthMeters(places, stopIndex) {
  if (!places || stopIndex <= 0 || stopIndex >= places.length) return 0;
  const a = places[stopIndex - 1];
  const b = places[stopIndex];
  return haversineMeters({ lat: a.lat, lng: a.lng }, { lat: b.lat, lng: b.lng });
}

function walkRouteBannerHtml() {
  if (!state.walkMode) return "";
  const ep = state.episodes.find((e) => e.id === state.currentEpisodeId);
  const places = getWalkPlaces();
  if (!ep || !places.length) return "";
  const stats = walkRouteStats(places);
  return `<p class="walk-route-estimate"><strong>${ep.title}</strong> · ${stats.summary} (${stats.detail})</p>`;
}

function walkRouteStats(places) {
  const meters = routeLengthMeters(places);
  const walkMin = walkMinutesForMeters(meters);
  const dwellMin = places.length * walkDwellMinutesPerStop();
  const totalMin = walkMin + dwellMin;
  const km = (meters / 1000).toFixed(1);
  return {
    meters,
    walkMin,
    dwellMin,
    totalMin,
    summary: `${km} km · ${formatWalkMinutes(totalMin)}`,
    detail: `Gang ${formatWalkMinutes(walkMin)}, med ca. ${Math.round(dwellMin)} min på stoppene`,
  };
}

function distanceToNextStopText() {
  if (!state.walkMode || !state.userMarker || !state.map) return "";
  const places = getWalkPlaces();
  const target = places[state.walkIndex];
  if (!target) return "";
  const user = state.userMarker.getLatLng();
  let m = haversineMeters({ lat: user.lat, lng: user.lng }, { lat: target.lat, lng: target.lng });
  if (
    state.userRouteTargetId === target.id &&
    state.userRouteDistanceM != null
  ) {
    m = state.userRouteDistanceM;
  }
  return `${formatWalkLeg(m)} til dette stoppet`;
}

function getTravelRouteTarget() {
  if (state.walkMode) {
    const places = getWalkPlaces();
    return places[state.walkIndex] || null;
  }
  const place =
    state.activePlaceId &&
    state.places.find((p) => p.id === state.activePlaceId);
  if (place) return place;
  const ev =
    state.activeEventId &&
    state.events.find((e) => e.id === state.activeEventId);
  const pid = ev?.place_ids?.[0];
  if (pid) return state.places.find((p) => p.id === pid);
  if (state.activePersonId) {
    const person = state.people.find((p) => p.id === state.activePersonId);
    const ppid = person?.place_ids?.[0];
    return ppid ? state.places.find((p) => p.id === ppid) : null;
  }
  if (state.activeContextId) {
    const ctx = state.contextEntries.find((c) => c.id === state.activeContextId);
    const cpid = ctx?.place_ids?.[0];
    return cpid ? state.places.find((p) => p.id === cpid) : null;
  }
  return null;
}

function renderWalkProgress(userLegText) {
  const prog = document.getElementById("walk-progress");
  if (!prog) return;
  const places = getWalkPlaces();
  if (!places.length) {
    prog.innerHTML = "";
    return;
  }
  const p = places[state.walkIndex];
  const stats = walkRouteStats(places);
  const title = `Stopp ${state.walkIndex + 1} av ${places.length}: ${p?.name || ""}`;
  const metaParts = [`Hele ruten ${stats.summary} (${stats.detail})`];
  const legM = legLengthMeters(places, state.walkIndex);
  if (state.walkIndex > 0 && legM > 0) {
    metaParts.push(`Fra forrige stopp: ${formatWalkLeg(legM)}`);
  }
  if (userLegText) {
    metaParts.push(`Fra deg nå: ${userLegText}`);
  } else if (state.walkIndex === 0 && !state.userMarker) {
    metaParts.push("Første stopp - følg kartet til merket 1");
  }
  let travelBlock = "";
  const currentStop = places[state.walkIndex];
  if (currentStop) {
    const hint = travelHintHtml(currentStop);
    if (hint) travelBlock = `<span class="walk-travel-hint">${hint}</span>`;
  }
  prog.innerHTML = `<span class="walk-progress-title">${title}</span><span class="walk-progress-meta">${metaParts.join(" · ")}</span>${travelBlock}`;
  prog.querySelectorAll(".ep-travel-link").forEach((link) => {
    link.addEventListener("click", (ev) => ev.stopPropagation());
  });
}

function placesByDistance(lat, lng, radiusM, limit) {
  const ranked = state.places
    .map((p) => ({
      place: p,
      meters: haversineMeters({ lat, lng }, { lat: p.lat, lng: p.lng }),
    }))
    .filter((x) => x.meters <= radiusM)
    .sort((a, b) => a.meters - b.meters);
  return limit ? ranked.slice(0, limit) : ranked;
}

function formatDistanceM(m) {
  if (m < 1000) return `${Math.round(m)} m`;
  return `${(m / 1000).toFixed(1)} km`;
}

function userLatLng() {
  if (state.userMarker) return state.userMarker.getLatLng();
  if (state.userPosition) return { lat: state.userPosition.lat, lng: state.userPosition.lng };
  return null;
}

function routeTravelThresholdM() {
  const n = state.siteConfig?.route_travel_threshold_m;
  return typeof n === "number" && n > 0 ? n : 600;
}

function travelDirectionsUrl(place) {
  if (!place) return "";
  const dest = `${place.lat},${place.lng}`;
  const user = userLatLng();
  if (user) {
    return `https://www.google.com/maps/dir/?api=1&origin=${user.lat},${user.lng}&destination=${dest}&travelmode=walking`;
  }
  return `https://www.google.com/maps/dir/?api=1&destination=${dest}&travelmode=walking`;
}

function enturJourneyUrl(place) {
  if (!place) return "";
  const user = userLatLng();
  if (!user) return "";
  const from = `${user.lat},${user.lng}`;
  const to = `${place.lat},${place.lng}`;
  return `https://entur.no/ruteplanlegger?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`;
}

function osmWalkDirectionsUrl(place) {
  if (!place) return "";
  const user = userLatLng();
  if (!user) return "";
  const from = `${user.lat},${user.lng}`;
  const to = `${place.lat},${place.lng}`;
  return `https://www.openstreetmap.org/directions?engine=fossgis_osrm_foot&route=${encodeURIComponent(`${from};${to}`)}`;
}

function travelHintHtml(place) {
  const user = userLatLng();
  if (!user || !place) return "";
  let meters = haversineMeters(user, { lat: place.lat, lng: place.lng });
  if (
    state.userRouteTargetId === place.id &&
    state.userRouteDistanceM != null
  ) {
    meters = state.userRouteDistanceM;
  }
  if (meters < routeTravelThresholdM()) return "";
  const walkUrl = travelDirectionsUrl(place);
  const walkMin = formatWalkMinutes(walkMinutesForMeters(meters));
  const links = [
    `<a class="ep-travel-link" href="${walkUrl}" target="_blank" rel="noopener noreferrer">Gåvei · ${walkMin} (${formatDistanceM(meters)})</a>`,
  ];
  const osmUrl = osmWalkDirectionsUrl(place);
  if (osmUrl) {
    links.push(
      `<a class="ep-travel-link ep-travel-osm" href="${osmUrl}" target="_blank" rel="noopener noreferrer">Fotrute (kart)</a>`,
    );
  }
  if (state.siteConfig.travel_show_entur !== false) {
    const enturUrl = enturJourneyUrl(place);
    if (enturUrl) {
      links.push(
        `<a class="ep-travel-link ep-travel-entur" href="${enturUrl}" target="_blank" rel="noopener noreferrer">Kollektiv (Entur)</a>`,
      );
    }
  }
  return `<span class="ep-travel-links">${links.join("")}</span>`;
}

function clearUserTravelRoute() {
  if (state.userRouteFetchAbort) {
    state.userRouteFetchAbort.abort();
    state.userRouteFetchAbort = null;
  }
  state.userRouteDistanceM = null;
  state.userRouteTargetId = null;
  state.userRouteLayer?.clearLayers();
}

function scheduleUserTravelRouteRefresh() {
  clearTimeout(state.userRouteRefreshTimer);
  state.userRouteRefreshTimer = setTimeout(() => refreshUserTravelRoute(), 450);
}

async function refreshUserTravelRoute() {
  clearUserTravelRoute();
  if (state.siteConfig?.travel_draw_osrm_in_map === false) return;
  if (!state.map) return;
  const target = getTravelRouteTarget();
  const user = userLatLng();
  if (!target || !user) return;
  const meters = haversineMeters(user, { lat: target.lat, lng: target.lng });
  const minM = state.walkMode ? 40 : routeTravelThresholdM();
  if (meters < minM) return;
  const url = `https://router.project-osrm.org/route/v1/foot/${user.lng},${user.lat};${target.lng},${target.lat}?overview=full&geometries=geojson`;
  state.userRouteFetchAbort = new AbortController();
  try {
    const res = await fetch(url, { signal: state.userRouteFetchAbort.signal });
    if (!res.ok) return;
    const data = await res.json();
    const route = data.routes?.[0];
    const coords = route?.geometry?.coordinates;
    if (!coords?.length || !state.userRouteLayer) return;
    const latlngs = coords.map(([lng, lat]) => [lat, lng]);
    state.userRouteDistanceM = route.distance;
    state.userRouteTargetId = target.id;
    L.polyline(latlngs, {
      color: state.walkMode ? markerColor("sted") : "#2a6f97",
      weight: state.walkMode ? 5 : 5,
      opacity: 0.82,
    }).addTo(state.userRouteLayer);
    if (state.walkMode) {
      renderWalkProgress(distanceToNextStopText());
    }
    if (!document.querySelector(".ep-travel-route-note")) {
      const wrap = document.querySelector(".ep-travel-links");
      if (wrap) {
        wrap.insertAdjacentHTML(
          "beforeend",
          '<span class="detail-muted ep-travel-route-note">Fotrute tegnet på kartet.</span>',
        );
      }
    }
    const walkLink = document.querySelector(".detail-travel .ep-travel-link");
    if (walkLink && route.distance >= routeTravelThresholdM()) {
      const walkMin = formatWalkMinutes(walkMinutesForMeters(route.distance));
      walkLink.textContent = `Gåvei · ${walkMin} (${formatDistanceM(route.distance)})`;
    }
  } catch (err) {
    if (err?.name === "AbortError") return;
  } finally {
    state.userRouteFetchAbort = null;
  }
}

async function copyCommunityPinJson(pinId) {
  const pin = findCommunityPin(pinId);
  if (!pin) return;
  const text = JSON.stringify(pin, null, 2);
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      window.prompt("Kopier bidraget:", text);
      return;
    }
    const hint = document.querySelector(".community-copy-hint");
    if (hint) {
      hint.textContent = "JSON kopiert til utklippstavlen.";
      hint.hidden = false;
    }
  } catch {
    window.prompt("Kopier bidraget:", text);
  }
}

function deleteCommunityPin(pinId) {
  const list = loadCommunityPins().filter((p) => p.id !== pinId);
  saveCommunityPins(list);
  state.activeCommunityPinId = null;
  refreshCommunityMarkers();
  updateFilterChrome();
  renderDetail();
  refreshMarkers();
}

function exploreSnapRadiusM() {
  const base = state.siteConfig.explore_snap_radius_m || 140;
  return window.matchMedia("(max-width: 900px)").matches ? Math.max(base, 165) : base;
}

function exploreNearbyRadiusM() {
  const base = state.siteConfig.explore_nearby_radius_m || 600;
  return window.matchMedia("(max-width: 900px)").matches ? Math.max(base, 750) : base;
}

function focusDetailPanel() {
  const panel = document.getElementById("detail-panel");
  if (!panel || !window.matchMedia("(max-width: 900px)").matches) return;
  panel.scrollTop = 0;
  panel.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function geolocationUserHint() {
  return "Tillat plassering for denne siden i nettleseren (lås-ikonet ved adressefeltet). I Windows: Personvern og sikkerhet - Plassering.";
}

function refreshGeolocationPermissionState() {
  if (!state.siteConfig.enable_geolocation || !navigator.permissions?.query) return;
  navigator.permissions
    .query({ name: "geolocation" })
    .then((result) => {
      const statusEl = document.getElementById("nearby-status");
      if (result.state === "denied" && statusEl && !state.userPosition) {
        statusEl.textContent = `Posisjon er blokkert. ${geolocationUserHint()}`;
      }
      result.onchange = () => refreshGeolocationPermissionState();
    })
    .catch(() => undefined);
}

function setLocateButtonState() {
  const btn = document.getElementById("btn-map-locate");
  if (!btn) return;
  const on = state.geoActive && state.followUser;
  btn.classList.toggle("active", on);
  btn.setAttribute("aria-pressed", on ? "true" : "false");
  btn.textContent = on ? "Følger deg" : "Min posisjon";
  btn.title = on ? "Slutt å følge posisjonen på kartet" : "Vis posisjonen din og steder i nærheten";
}

function updateNearbyPanel() {
  const statusEl = document.getElementById("nearby-status");
  const listEl = document.getElementById("nearby-list");
  if (!statusEl || !listEl) return;
  if (!state.userPosition) {
    setNearbyIdleHint();
    listEl.innerHTML = "";
    return;
  }
  delete statusEl.dataset.nearbyIdle;
  const radius = exploreNearbyRadiusM();
  const limit = state.siteConfig.explore_nearby_list_size || 5;
  const ranked = placesByDistance(
    state.userPosition.lat,
    state.userPosition.lng,
    radius,
    limit,
  );
  if (!ranked.length) {
    statusEl.textContent = `Ingen kuraterte stopp innen ${formatDistanceM(radius)} - zoom eller flytt kartet.`;
    listEl.innerHTML = "";
    return;
  }
  statusEl.textContent = `Innen ${formatDistanceM(radius)}:`;
  listEl.innerHTML = ranked
    .map(
      ({ place, meters }) =>
        `<li><button type="button" class="nearby-btn" data-place-id="${place.id}">${place.name} · ${formatDistanceM(meters)}</button></li>`,
    )
    .join("");
  listEl.querySelectorAll(".nearby-btn").forEach((btn) => {
    btn.addEventListener("click", () => selectPlace(btn.dataset.placeId));
  });
}

function onUserPosition(lat, lng, accuracy) {
  state.userPosition = { lat, lng, accuracy };
  if (!state.userMarker) {
    state.userMarker = L.circleMarker([lat, lng], {
      radius: 10,
      color: "#fff",
      weight: 3,
      fillColor: "#2a6f97",
      fillOpacity: 1,
    }).addTo(state.map);
    state.userAccuracy = L.circle([lat, lng], {
      radius: Math.min(accuracy || 40, 120),
      color: "#2a6f97",
      weight: 1,
      fillColor: "#dceef7",
      fillOpacity: 0.35,
    }).addTo(state.map);
  } else {
    state.userMarker.setLatLng([lat, lng]);
    if (state.userAccuracy) {
      state.userAccuracy.setLatLng([lat, lng]);
      state.userAccuracy.setRadius(Math.min(accuracy || 40, 120));
    }
  }
  updateNearbyPanel();
  if (state.walkMode) {
    renderWalkProgress(distanceToNextStopText());
    scheduleUserTravelRouteRefresh();
  } else if (state.activePlaceId || state.activeEventId) {
    renderDetail();
    scheduleUserTravelRouteRefresh();
  } else if (state.followUser) {
    state.map.setView([lat, lng], Math.max(state.map.getZoom(), 17), { animate: true });
  }
  if (state.sidePanelMode === "routes") renderEpisodeCards();
}

function stopGeolocationWatch() {
  if (state.geoWatchId != null && navigator.geolocation) {
    navigator.geolocation.clearWatch(state.geoWatchId);
    state.geoWatchId = null;
  }
  state.geoActive = false;
  setLocateButtonState();
}

function startGeolocationWatch() {
  if (!state.siteConfig.enable_geolocation || !navigator.geolocation) return;
  if (state.geoWatchId != null) {
    state.geoActive = true;
    state.followUser = true;
    setLocateButtonState();
    const nearbyWrap = document.getElementById("nearby-wrap");
    if (nearbyWrap) nearbyWrap.open = true;
    updateNearbyPanel();
    if (state.userPosition && state.map) {
      const { lat, lng } = state.userPosition;
      state.map.setView([lat, lng], Math.max(state.map.getZoom(), 17), { animate: true });
    }
    return;
  }
  state.geoActive = true;
  state.followUser = true;
  setLocateButtonState();
  const nearbyWrap = document.getElementById("nearby-wrap");
  if (nearbyWrap) nearbyWrap.open = true;
  state.geoWatchId = navigator.geolocation.watchPosition(
    (pos) => {
      const { latitude: lat, longitude: lng, accuracy } = pos.coords;
      onUserPosition(lat, lng, accuracy);
    },
    () => {
      stopGeolocationWatch();
      const statusEl = document.getElementById("nearby-status");
      if (statusEl) statusEl.textContent = `Kunne ikke lese posisjon. ${geolocationUserHint()}`;
    },
    { enableHighAccuracy: true, timeout: 15000, maximumAge: 5000 },
  );
}

function startGeolocation() {
  startGeolocationWatch();
}

function setExploreMarker(lat, lng) {
  if (state.exploreMarker) state.exploreMarker.remove();
  state.exploreMarker = L.circleMarker([lat, lng], {
    radius: 8,
    color: "#1e2433",
    weight: 2,
    fillColor: "#bc6c25",
    fillOpacity: 0.95,
  }).addTo(state.map);
}

async function reverseGeocodeLabel(lat, lng) {
  if (!state.siteConfig.reverse_geocode_on_map_click) return "";
  const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&zoom=18&addressdetails=1`;
  try {
    const res = await fetch(url, { headers: NOMINATIM_HEADERS });
    if (!res.ok) return "";
    const data = await res.json();
    const a = data.address || {};
    return (
      a.road ||
      a.pedestrian ||
      a.building ||
      a.amenity ||
      data.name ||
      data.display_name?.split(",")[0] ||
      ""
    );
  } catch {
    return "";
  }
}

function renderExploreFallback(lat, lng, streetLabel, snapRadius) {
  const el = document.getElementById("detail-panel");
  if (!el) return;
  const nearest = placesByDistance(lat, lng, snapRadius * 4, 3);
  const title = streetLabel ? streetLabel : "Punkt på kartet";
  let body = `<p>Her er det ingen ferdig historietekst knyttet rett til dette punktet ennå.</p>`;
  if (nearest.length) {
    body += `<p>Nærmeste kuraterte stopp:</p><ul class="explore-near-list">`;
    nearest.forEach(({ place, meters }) => {
      body += `<li><button type="button" class="linkish nearby-pick" data-place-id="${place.id}">${place.name} (${formatDistanceM(meters)})</button></li>`;
    });
    body += `</ul>`;
  } else {
    body += `<p>Prøv et annet hjørne i Oslo sentrum, Gamlebyen eller langs Akerselva.</p>`;
  }
  el.innerHTML = `<h3>${title}</h3>${body}`;
  el.querySelectorAll(".nearby-pick").forEach((btn) => {
    btn.addEventListener("click", () => selectPlace(btn.dataset.placeId));
  });
}

function setCommunityMapPickBanner(show) {
  const el = document.getElementById("map-pick-banner");
  if (el) el.hidden = !show;
}

function clearCommunityPickMarker() {
  if (state.communityPickMarker) {
    state.communityPickMarker.remove();
    state.communityPickMarker = null;
  }
}

function exitCommunityMapPick() {
  state.communityMapPick = false;
  setCommunityMapPickBanner(false);
  clearCommunityPickMarker();
}

async function applyCommunityPickAt(lat, lng) {
  document.getElementById("community-tag-lat").value = String(lat);
  document.getElementById("community-tag-lng").value = String(lng);
  const label = await reverseGeocodeLabel(lat, lng);
  const geo = document.getElementById("community-tag-geo");
  if (geo) geo.textContent = label ? `Koordinat satt: ${label}` : "Koordinat satt fra kartet.";
  if (label && !document.getElementById("community-tag-address").value) {
    document.getElementById("community-tag-address").value = label;
  }
  clearCommunityPickMarker();
  if (state.map) {
    const icon = L.divIcon({
      className: "custom-pin custom-pin-community-pick",
      html: communityPinHtml(),
      iconSize: [28, 28],
      iconAnchor: [14, 14],
    });
    state.communityPickMarker = L.marker([lat, lng], { icon, zIndexOffset: 80 }).addTo(state.map);
  }
}

async function onMapExplore(latlng) {
  if (!state.map) return;
  const lat = latlng.lat;
  const lng = latlng.lng;
  if (state.communityMapPick) {
    exitCommunityMapPick();
    await applyCommunityPickAt(lat, lng);
    const dlg = document.getElementById("community-tag-dialog");
    if (dlg && typeof dlg.showModal === "function") dlg.showModal();
    return;
  }
  setExploreMarker(lat, lng);
  const snap = exploreSnapRadiusM();
  const hit = placesByDistance(lat, lng, snap, 1)[0];
  if (hit) {
    selectPlace(hit.place.id, { pan: false });
    return;
  }
  state.activePlaceId = null;
  state.activeEventId = null;
  renderTimeline();
  const label = await reverseGeocodeLabel(lat, lng);
  renderExploreFallback(lat, lng, label, snap);
}

function renderEpisodeCards() {
  const nav = document.getElementById("episode-cards");
  if (!nav) return;
  nav.innerHTML = "";

  const byEra = new Map();
  state.episodes.forEach((ep) => {
    const key = ep.era_id || "_other";
    if (!byEra.has(key)) byEra.set(key, []);
    byEra.get(key).push(ep);
  });

  state.eras.forEach((era) => {
    const eps = byEra.get(era.id);
    if (!eps?.length) return;

    const section = document.createElement("section");
    section.className = "episode-era";
    section.setAttribute("aria-label", era.label);
    section.innerHTML = `<h2 class="episode-era-title"><span>${era.label}</span><span class="era-short">${era.short || ""}</span></h2>`;

    const row = document.createElement("div");
    row.className = "episode-era-row";

    eps.forEach((ep) => {
      const stops = ep.place_order?.length || 0;
      if (stops < 1) return;
      const btn = document.createElement("button");
      btn.type = "button";
      const ready = true;
      const activeRoute = state.walkMode && state.currentEpisodeId === ep.id;
      btn.className = "episode-card-btn" + (activeRoute ? " active" : "");
      btn.setAttribute("aria-label", ready ? `${ep.title}. Trykk for å starte gåtur.` : ep.title);
      const ordered = (ep.place_order || [])
        .map((id) => state.places.find((pl) => pl.id === id))
        .filter(Boolean);
      const routeStats = ready ? walkRouteStats(ordered) : null;
      const badge = ready
        ? `${stops} stopp · ${routeStats.summary}`
        : "Planlagt";
      const first = ordered[0];
      const last = ordered[ordered.length - 1];
      const endpoints =
        first && last
          ? `<span class="ep-route-endpoints">Start: ${first.name} · Slutt: ${last.name}</span>`
          : "";
      const timeDetail = ready ? `<span class="ep-route-detail">${routeStats.detail}</span>` : "";
      const travel = ready ? travelHintHtml(first) : "";
      const cta = ready
        ? `<span class="ep-route-cta">${state.walkMode && activeRoute ? "Pågår - trykk for å fortsette" : "Trykk her for å starte gåtur"}</span>`
        : "";
      btn.innerHTML = `
        <span class="ep-title">${ep.title}</span>
        <span class="ep-meta">${ep.subtitle || ""}</span>
        ${endpoints}
        <span class="ep-badge ${ready ? "ready" : ""}">${badge}</span>
        ${timeDetail}
        ${travel}
        ${cta}
      `;
      btn.querySelectorAll(".ep-travel-link").forEach((link) => {
        link.addEventListener("click", (ev) => ev.stopPropagation());
      });
      btn.addEventListener("click", () => {
        if (!ready) return;
        startWalk(ep.id);
      });
      if (!ready) btn.disabled = true;
      row.appendChild(btn);
    });

    section.appendChild(row);
    nav.appendChild(section);
  });
}

function getEpisodePlaceSet(episodeId) {
  const ep = state.episodes.find((e) => e.id === episodeId);
  if (!ep) return null;
  const walk = ep.place_order || [];
  const extra = ep.map_place_order || [];
  const ids = [...walk, ...extra];
  if (!ids.length) return null;
  return new Set(ids);
}

function placeMatchesEpisode(place, episodeId) {
  if (place.episode_id === episodeId) return true;
  const order = getEpisodePlaceSet(episodeId);
  return order ? order.has(place.id) : false;
}

function eventMatchesEpisode(event, episodeId) {
  if (event.episode_id === episodeId) return true;
  const order = getEpisodePlaceSet(episodeId);
  if (!order) return false;
  return (event.place_ids || []).some((id) => order.has(id));
}

function getFilters() {
  const yearMinEl = document.getElementById("year-min");
  const yearMaxEl = document.getElementById("year-max");
  const yearMin = yearMinEl ? parseInt(yearMinEl.value, 10) : state.chronologyYearMin;
  const yearMax = yearMaxEl ? parseInt(yearMaxEl.value, 10) : state.chronologyYearMax;
  return {
    destination: document.getElementById("filter-destination")?.value || "all",
    bind: "all",
    century: document.getElementById("filter-century").value,
    tag: document.getElementById("filter-tag").value,
    episode: document.getElementById("filter-episode").value,
    district: document.getElementById("filter-district")?.value || "all",
    chronology: document.getElementById("filter-chronology")?.value || "all",
    yearMin: Number.isFinite(yearMin) ? yearMin : state.chronologyYearMin,
    yearMax: Number.isFinite(yearMax) ? Math.min(yearMax, state.chronologyYearMax) : state.chronologyYearMax,
  };
}

function itemMatchesYearRange(item, yearMin, yearMax) {
  const y = item.year ?? item.year_from ?? item.year_to;
  const from = item.year_from ?? item.year_to ?? item.year;
  const to = item.year_to ?? item.year_from ?? item.year;
  if (from == null && to == null && y == null) return true;
  const lo = from ?? to ?? y;
  const hi = to ?? from ?? y;
  if (hi < yearMin) return false;
  if (lo > yearMax) return false;
  return true;
}

function itemMatchesChronology(item, chronologyId) {
  if (chronologyId === "all") return true;
  const era = window.OsloHistorieBydel?.chronologyEra(chronologyId, state.chronologyEras);
  if (!era) return true;
  if (item.chronology_era_id && item.chronology_era_id !== chronologyId) return false;
  const from = item.year_from ?? item.year_to ?? item.year;
  const to = item.year_to ?? item.year_from ?? item.year;
  if (from == null && to == null) return item.chronology_era_id === chronologyId;
  const lo = from ?? to;
  const hi = to ?? from;
  return !(hi < era.year_from || lo > era.year_to);
}

function placeDistrictId(place) {
  return place.district_id || window.OsloHistorieBydel?.districtIdAt(place.lat, place.lng, state.districts);
}

function eventInDistrict(event, districtId) {
  if (districtId === "all") return true;
  return (event.place_ids || []).some((pid) => {
    const p = state.places.find((x) => x.id === pid);
    return p && placeDistrictId(p) === districtId;
  });
}

function getFilteredFinds() {
  const f = getFilters();
  if (f.destination === "community" || f.destination === "blaa-skilt") return [];
  const base =
    window.OsloHistorieBydel?.filterFinds(state.finds, {
      district: f.district,
      chronology: f.chronology,
      yearMin: f.yearMin,
      yearMax: f.yearMax,
      chronologyEras: state.chronologyEras,
    }) || [];
  return base.filter((find) => itemMatchesCentury(find, f.century));
}

function filterEvents() {
  const { destination, bind, century, tag, episode, district, chronology, yearMin, yearMax } = getFilters();
  if (destination === "community") return [];
  return state.events
    .filter((e) => {
      if (e.year > state.chronologyYearMax) return false;
      if (!itemMatchesYearRange(e, yearMin, yearMax)) return false;
      if (!itemMatchesChronology(e, chronology)) return false;
      if (!eventInDistrict(e, district)) return false;
      if (bind !== "all" && String(e.bind) !== bind) return false;
      if (!itemMatchesCentury(e, century)) return false;
      if (tag !== "all" && !(e.tags || []).includes(tag)) return false;
      if (episode !== "all" && !eventMatchesEpisode(e, episode)) return false;
      return true;
    })
    .sort((a, b) => a.year - b.year);
}

function placeHasBlaaSkilt(place) {
  return !!place?.blaa_skilt || (place?.tags || []).includes("blaa-skilt");
}

function filterStandaloneBlueSigns() {
  const { destination, tag, district, chronology, yearMin, yearMax } = getFilters();
  if (destination === "historie" || destination === "community") return [];
  return (state.blueSigns || []).filter((s) => {
    if (s.place_id) return false;
    if (destination === "blaa-skilt" || destination === "all") {
      /* vis */
    } else return false;
    if (!itemMatchesYearRange(s, yearMin, yearMax)) return false;
    if (!itemMatchesChronology(s, chronology)) return false;
    if (tag !== "all" && !(s.tags || []).includes(tag)) return false;
    if (district !== "all") {
      const did = window.OsloHistorieBydel?.districtIdAt(s.lat, s.lng, state.districts);
      if (did !== district) return false;
    }
    return true;
  });
}

function filterPlaces() {
  const { destination, bind, century, tag, episode, district, chronology, yearMin, yearMax } = getFilters();
  if (destination === "community") return [];
  return state.places.filter((p) => {
    if (destination === "blaa-skilt" && !placeHasBlaaSkilt(p)) return false;
    if (district !== "all" && placeDistrictId(p) !== district) return false;
    if (!itemMatchesYearRange(p, yearMin, yearMax)) return false;
    if (!itemMatchesChronology(p, chronology)) return false;
    if (bind !== "all" && String(p.bind) !== bind) return false;
    if (!itemMatchesCentury(p, century)) return false;
    if (tag !== "all" && !(p.tags || []).includes(tag)) return false;
    if (episode !== "all" && !placeMatchesEpisode(p, episode)) return false;
    return true;
  });
}

function initMap() {
  const startZoom = state.mapConfig?.default_zoom || 15;
  const maxZoom = state.mapConfig?.max_zoom || 20;
  state.map = L.map("map", {
    scrollWheelZoom: true,
    zoomControl: true,
    maxZoom,
  }).setView([59.908, 10.748], startZoom);
  populateMapLayers();
  state.routeLayer = L.layerGroup().addTo(state.map);
  state.userRouteLayer = L.layerGroup().addTo(state.map);
  state.map.on("click", (e) => onMapExplore(e.latlng));
  if (state.bydelerGeo && window.OsloHistorieBydel) {
    state.districtMapUi = window.OsloHistorieBydel.createDistrictLayers(state.map, state.bydelerGeo, {
      onSelect: (id) => selectDistrict(id),
      getActiveId: () => document.getElementById("filter-district")?.value || "all",
      maxZoomHighlight: state.siteConfig.district_layer_max_zoom ?? 13,
    });
  }
  state.map.on("dragstart", () => {
    if (state.geoActive) {
      state.followUser = false;
      setLocateButtonState();
    }
  });
  window.addEventListener("resize", () => {
    state.map?.invalidateSize();
  });
}

function walkStopIndex(placeId) {
  if (!state.walkMode) return -1;
  const ep = state.episodes.find((e) => e.id === state.currentEpisodeId);
  if (!ep?.place_order) return -1;
  return ep.place_order.indexOf(placeId);
}

function blueSignPinHtml() {
  const active = false;
  return pinHtml({ kindId: "blaa-skilt", active });
}

function placePinHtml(place, stopIndex) {
  const kindId = placeMarkerKind(place);
  const isActive = place.id === state.activePlaceId;
  const walkPlaces = getWalkPlaces();
  const onWalk = state.walkMode && walkPlaces.some((p) => p?.id === place.id);
  const label =
    stopIndex >= 0 ? `<span class="pin-num">${stopIndex + 1}</span>` : "";
  const blaaRing =
    getFilters().destination === "all" && placeHasBlaaSkilt(place) && kindId === "sted";
  return pinHtml({ kindId, active: isActive || onWalk, labelHtml: label, blaaRing });
}

function refreshWalkRoute() {
  if (!state.routeLayer) return;
  state.routeLayer.clearLayers();
  if (!state.walkMode) return;
  const ep = state.episodes.find((e) => e.id === state.currentEpisodeId);
  if (!ep?.place_order?.length) return;
  const latlngs = ep.place_order
    .map((id) => state.places.find((p) => p.id === id))
    .filter(Boolean)
    .map((p) => [p.lat, p.lng]);
  if (latlngs.length < 2) return;
  L.polyline(latlngs, {
    color: markerColor("sted"),
    weight: 4,
    opacity: 0.75,
    dashArray: state.walkMode ? null : "8 10",
  }).addTo(state.routeLayer);
}

function findPinHtml(find) {
  const active = find?.id === state.activeFindId;
  return pinHtml({ kindId: "funn", active });
}

function refreshFindMarkers() {
  Object.values(state.findMarkers).forEach((m) => m.remove());
  state.findMarkers = {};
  if (!state.map) return;
  const pinBox = pinBoxSize();
  const anchor = pinBox / 2;
  getFilteredFinds().forEach((find) => {
    if (find.lat == null || find.lng == null) return;
    const icon = L.divIcon({
      className: "custom-pin custom-pin-funn",
      html: findPinHtml(find),
      iconSize: [pinBox, pinBox],
      iconAnchor: [anchor, anchor],
    });
    const marker = L.marker([find.lat, find.lng], { icon, zIndexOffset: 100 }).addTo(state.map);
    marker.bindPopup(`<strong>${find.title}</strong><p>${find.summary.slice(0, 120)}${find.summary.length > 120 ? "..." : ""}</p>`);
    marker.on("click", () => selectFind(find.id));
    state.findMarkers[find.id] = marker;
  });
}

function refreshPeopleMarkers() {
  Object.values(state.personMarkers).forEach((m) => m.remove());
  state.personMarkers = {};
  if (!state.map || !shouldShowPeopleMarkers()) return;
  const visiblePlaces = new Set(filterPlaces().map((p) => p.id));
  const pinBox = pinBoxSize();
  const anchor = pinBox / 2;
  state.people.forEach((person) => {
    (person.place_ids || []).forEach((pid, idx) => {
      if (!visiblePlaces.has(pid)) return;
      const place = state.places.find((p) => p.id === pid);
      if (!place) return;
      const lat = place.lat + idx * 0.00008;
      const lng = place.lng + idx * 0.00012;
      const isActive = state.activePersonId === person.id;
      const icon = L.divIcon({
        className: "custom-pin custom-pin-person",
        html: pinHtml({ kindId: "person", active: isActive }),
        iconSize: [pinBox, pinBox],
        iconAnchor: [anchor, anchor],
      });
      const marker = L.marker([lat, lng], { icon, zIndexOffset: 115 }).addTo(state.map);
      marker.bindPopup(`<strong>${person.name}</strong><p>Person · ${person.year_from}-${person.year_to}</p>`);
      marker.on("click", () => selectPerson(person.id));
      state.personMarkers[`${person.id}-${pid}`] = marker;
    });
  });
}

function renderMapLegend() {
  const el = document.getElementById("map-legend");
  if (!el) return;
  const kinds = ["sted", "blaa-skilt", "funn", "person"];
  let html = kinds
    .map((id) => {
      const spec = markerKindSpec(id);
      return `<li class="map-legend-item"><span class="map-legend-swatch map-legend-swatch--${id}" aria-hidden="true"></span>${spec.label}</li>`;
    })
    .join("");
  if (state.siteConfig?.community_tags_enabled) {
    html += `<li class="map-legend-item"><span class="map-legend-swatch map-legend-swatch--community" aria-hidden="true">#</span>Brukerbidrag</li>`;
  }
  el.innerHTML = html;
}

function escapeHtml(text) {
  return String(text ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

const COMMUNITY_PINS_KEY = "kristiania-community-pins";

function parseHashtagField(raw) {
  const tags = new Set();
  for (const part of String(raw || "").split(/[\s,]+/)) {
    const t = part.trim().replace(/^#+/, "");
    if (t) tags.add(`#${t.toLowerCase()}`);
  }
  return [...tags];
}

function loadCommunityPins() {
  try {
    const raw = localStorage.getItem(COMMUNITY_PINS_KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list : [];
  } catch {
    return [];
  }
}

function saveCommunityPins(list) {
  localStorage.setItem(COMMUNITY_PINS_KEY, JSON.stringify(list));
}

function communityPinHtml() {
  return `<div class="pin-community" aria-hidden="true">#</div>`;
}

function refreshCommunityMarkers() {
  Object.values(state.communityMarkers || {}).forEach((m) => m.remove());
  state.communityMarkers = {};
  if (!state.siteConfig?.community_tags_enabled || !state.map) return;
  const dest = getFilters().destination;
  if (dest !== "all" && dest !== "community") return;

  const mobilePins = window.matchMedia("(max-width: 900px)").matches;
  const pinBox = mobilePins ? 32 : 26;
  const pinAnchor = pinBox / 2;
  loadCommunityPins().forEach((pin) => {
    if (typeof pin.lat !== "number" || typeof pin.lng !== "number") return;
    const icon = L.divIcon({
      className: "custom-pin custom-pin-community",
      html: communityPinHtml(),
      iconSize: [pinBox, pinBox],
      iconAnchor: [pinAnchor, pinAnchor],
    });
    const tags = (pin.hashtags || []).join(" ");
    const marker = L.marker([pin.lat, pin.lng], { icon, zIndexOffset: 60 }).addTo(state.map);
    marker.bindPopup(
      `<strong>${escapeHtml(pin.title)}</strong><p>${escapeHtml((pin.story || "").slice(0, 160))}${(pin.story || "").length > 160 ? "..." : ""}</p><p class="popup-blaa">${escapeHtml(tags)}</p><p class="popup-cta">Trykk igjen for full tekst</p>`,
    );
    marker.on("click", () => selectCommunityPin(pin.id, { pan: false }));
    state.communityMarkers[pin.id] = marker;
  });
}

function findCommunityPin(pinId) {
  return loadCommunityPins().find((p) => p.id === pinId) || null;
}

function selectCommunityPin(pinId, options = { pan: true }) {
  const pin = findCommunityPin(pinId);
  if (!pin) return;
  state.activePlaceId = null;
  state.activeEventId = null;
  state.activePersonId = null;
  state.activeContextId = null;
  state.activeBlueSignId = null;
  state.activeFindId = null;
  state.activeCommunityPinId = pinId;
  renderTimeline();
  renderDetail();
  if (options.pan !== false && state.map) {
    state.map.panTo([pin.lat, pin.lng], { animate: true });
  }
}

function openCommunityTagDialog() {
  const dlg = document.getElementById("community-tag-dialog");
  if (!dlg || !state.siteConfig?.community_tags_enabled) return;
  exitCommunityMapPick();
  const err = document.getElementById("community-tag-error");
  if (err) err.hidden = true;
  const geo = document.getElementById("community-tag-geo");
  if (geo && !document.getElementById("community-tag-lat").value) geo.textContent = "";
  if (typeof dlg.showModal === "function") dlg.showModal();
}

function initCommunityTagUi() {
  const dlg = document.getElementById("community-tag-dialog");
  const form = document.getElementById("community-tag-form");
  if (!dlg || !form || !state.siteConfig?.community_tags_enabled) return;

  dlg.querySelector('[data-action="community-tag-cancel"]')?.addEventListener("click", () => {
    exitCommunityMapPick();
    dlg.close();
  });

  document.getElementById("community-tag-map-pick")?.addEventListener("click", () => {
    exitCommunityMapPick();
    state.communityMapPick = true;
    setCommunityMapPickBanner(true);
    dlg.close();
    if (isHomeActive()) dismissHome("explore");
    else writeAppRoute("explore", { replace: true });
    window.setTimeout(() => state.map?.invalidateSize(), 120);
  });

  dlg.addEventListener("close", () => {
    if (!state.communityMapPick) exitCommunityMapPick();
  });

  document.getElementById("community-tag-locate")?.addEventListener("click", () => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        document.getElementById("community-tag-lat").value = String(lat);
        document.getElementById("community-tag-lng").value = String(lng);
        const label = await reverseGeocodeLabel(lat, lng);
        const geo = document.getElementById("community-tag-geo");
        if (geo) geo.textContent = label ? `Koordinat satt: ${label}` : "Koordinat satt fra posisjonen din.";
        if (label && !document.getElementById("community-tag-address").value) {
          document.getElementById("community-tag-address").value = label;
        }
      },
      () => {
        const err = document.getElementById("community-tag-error");
        if (err) {
          err.textContent = "Kunne ikke hente posisjon. Prøv adressesøk i kartet.";
          err.hidden = false;
        }
      },
      { enableHighAccuracy: true, timeout: 12000 },
    );
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const err = document.getElementById("community-tag-error");
    if (err) err.hidden = true;

    const title = document.getElementById("community-tag-title-input").value.trim();
    const story = document.getElementById("community-tag-story").value.trim();
    const address = document.getElementById("community-tag-address").value.trim();
    let lat = parseFloat(document.getElementById("community-tag-lat").value);
    let lng = parseFloat(document.getElementById("community-tag-lng").value);

    if (!title || !story) {
      if (err) {
        err.textContent = "Fyll inn tittel og historie.";
        err.hidden = false;
      }
      return;
    }

    if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
      const q = address || title;
      const rows = await nominatimForwardSearch(q);
      if (rows?.[0]) {
        lat = parseFloat(rows[0].lat);
        lng = parseFloat(rows[0].lon);
      }
    }

    if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
      if (err) {
        err.textContent = "Fant ikke stedet. Bruk «Bruk min posisjon» eller mer presis adresse.";
        err.hidden = false;
      }
      return;
    }

    const pin = {
      id: `community-${Date.now()}`,
      title,
      story,
      address,
      lat,
      lng,
      hashtags: parseHashtagField(document.getElementById("community-tag-hashtags").value),
      authorAlias: document.getElementById("community-tag-alias").value.trim() || undefined,
      createdAt: new Date().toISOString(),
    };
    const list = loadCommunityPins();
    list.push(pin);
    saveCommunityPins(list);
    exitCommunityMapPick();
    dlg.close();
    form.reset();
    clearCommunityPickMarker();
    refreshCommunityMarkers();
    updateFilterChrome();
    state.map?.panTo([lat, lng], { animate: true });
  });
}

function refreshMarkers() {
  Object.values(state.markers).forEach((m) => m.remove());
  state.markers = {};
  if (state.blueSignMarkers) {
    Object.values(state.blueSignMarkers).forEach((m) => m.remove());
  }
  state.blueSignMarkers = {};

  const mobilePins = window.matchMedia("(max-width: 900px)").matches;
  const pinBox = mobilePins ? 36 : 26;
  const pinAnchor = pinBox / 2;
  filterPlaces().forEach((place) => {
    const stopIndex = walkStopIndex(place.id);
    const icon = L.divIcon({
      className: "custom-pin",
      html: placePinHtml(place, stopIndex),
      iconSize: [pinBox, pinBox],
      iconAnchor: [pinAnchor, pinAnchor],
    });

    const marker = L.marker([place.lat, place.lng], { icon }).addTo(state.map);
    marker.bindPopup(
      `<strong>${place.name}</strong><p>${place.summary.slice(0, 120)}${place.summary.length > 120 ? "..." : ""}</p><p class="popup-cta">Trykk merket igjen for full tekst.</p>`,
    );
    marker.on("click", () => selectPlace(place.id, { pan: false }));
    state.markers[place.id] = marker;
  });
  filterStandaloneBlueSigns().forEach((sign) => {
    const icon = L.divIcon({
      className: "custom-pin custom-pin-blaa",
      html: blueSignPinHtml(),
      iconSize: [pinBox, pinBox],
      iconAnchor: [pinAnchor, pinAnchor],
    });
    const marker = L.marker([sign.lat, sign.lng], { icon, zIndexOffset: 80 }).addTo(state.map);
    marker.bindPopup(
      `<strong>${sign.name}</strong><p class="popup-blaa">Blå skilt · ${sign.address || ""}</p><p>${sign.summary.slice(0, 100)}${sign.summary.length > 100 ? "..." : ""}</p>`,
    );
    marker.on("click", () => selectBlueSign(sign.id, { pan: false }));
    state.blueSignMarkers[sign.id] = marker;
  });
  refreshWalkRoute();
  refreshFindMarkers();
  refreshPeopleMarkers();
  refreshCommunityMarkers();
  state.districtMapUi?.restyle?.();
}

function formatYearLabel(year) {
  if (year < 0) return `${Math.abs(year)} f.Kr.`;
  return String(year);
}

function renderDistrictPanel(districtId) {
  const el = document.getElementById("detail-panel");
  const district = state.districts.find((d) => d.id === districtId);
  if (!el || !district) return;
  const { chronology } = getFilters();
  const era = window.OsloHistorieBydel?.chronologyEra(chronology, state.chronologyEras);
  const eraNote =
    chronology !== "all" ? district.era_notes?.[chronology] : "";

  const places = filterPlaces();
  const events = filterEvents();
  const finds = getFilteredFinds();

  const findList = finds.length
    ? finds.map((f) => `<li><button type="button" class="linkish" data-find-id="${f.id}"><strong>${f.title}</strong> (${f.year_display || formatYearLabel(window.OsloHistorieBydel.findYear(f))})</button><p>${f.summary}</p></li>`).join("")
    : "<li>Ingen registrerte funn for valgt bydel og tidsalder.</li>";

  const placeList = places.length
    ? places.map((p) => `<li><button type="button" class="linkish" data-place-id="${p.id}">${p.name}</button></li>`).join("")
    : "<li>Ingen steder i utvalget.</li>";

  const eventList = events.length
    ? events.slice(0, 8).map((e) => `<li><button type="button" class="linkish" data-event-id="${e.id}">${e.year_display || e.year}: ${e.title}</button></li>`).join("")
    : "<li>Ingen hendelser i utvalget.</li>";

  el.innerHTML = `
    <h3>${district.name}</h3>
    ${era ? `<p class="chip chronology">${era.label} <span class="era-short">${era.short || ""}</span></p>` : ""}
    ${eraNote ? `<p class="detail-body">${eraNote}</p>` : ""}
    <h4 class="district-section">Funn og arkeologi</h4>
    <ul class="district-list">${findList}</ul>
    <h4 class="district-section">Steder (${places.length})</h4>
    <ul class="district-list compact">${placeList}</ul>
    <h4 class="district-section">Hendelser (${events.length})</h4>
    <ul class="district-list compact">${eventList}</ul>
    <p class="detail-muted">Bydelesgrensene er forenklet. Zoom ut på kartet for å se alle bydeler.</p>
  `;

  el.querySelectorAll("[data-place-id]").forEach((btn) => {
    btn.addEventListener("click", () => selectPlace(btn.dataset.placeId));
  });
  el.querySelectorAll("[data-event-id]").forEach((btn) => {
    btn.addEventListener("click", () => selectEvent(btn.dataset.eventId));
  });
  el.querySelectorAll("[data-find-id]").forEach((btn) => {
    btn.addEventListener("click", () => selectFind(btn.dataset.findId));
  });
}

function selectContext(contextId) {
  const ctx = state.contextEntries.find((c) => c.id === contextId);
  if (!ctx) return;
  state.activeContextId = contextId;
  state.activeEventId = null;
  state.activePlaceId = null;
  state.activePersonId = null;
  state.activeFindId = null;
  state.activeBlueSignId = null;
  state.activeCommunityPinId = null;
  clearUserTravelRoute();
  const el = document.getElementById("detail-panel");
  if (!el) return;
  destroyPlaceMiniMap();
  const yearLabel = ctx.year_display || formatYearLabel(ctx.year_from);
  const ctxPlaces = (ctx.place_ids || [])
    .map((id) => state.places.find((p) => p.id === id))
    .filter(Boolean);
  const travelPlace = ctxPlaces[0];
  const travelDetail =
    travelPlace && !state.walkMode ? travelHintHtml(travelPlace) : "";
  const travelRow = travelDetail
    ? `<p class="detail-travel walk-travel-hint" aria-label="Reisevei til stedet">${travelDetail}</p>`
    : "";
  const placeLinks = ctxPlaces.length
    ? `<p class="detail-related-places">Steder: ${ctxPlaces
        .map(
          (p) =>
            `<button type="button" class="linkish detail-place-jump" data-place-id="${escapeHtml(p.id)}">${escapeHtml(p.name)}</button>`,
        )
        .join(" · ")}</p>`
    : "";
  el.innerHTML = `
    <h3>${ctx.title}</h3>
    <div class="meta-row">
      <span class="chip">Bakgrunn</span>
      ${bindChipHtml(ctx.bind)}
      <span class="chip">${yearLabel}</span>
      ${tagChipsHtml(ctx.tags)}
    </div>
    ${travelRow}
    ${sourceBadgeHtml(ctx)}
    ${sourceBlockHtml(ctx)}
    ${mediaFigureHtml(ctx)}
    <p class="detail-body">${ctx.summary}</p>
    ${placeLinks}
    <p class="detail-actions"><button type="button" class="detail-back linkish" data-action="clear-selection">Lukk</button></p>
  `;
  el.querySelectorAll(".ep-travel-link").forEach((link) => {
    link.addEventListener("click", (ev) => ev.stopPropagation());
  });
  el.querySelectorAll(".detail-place-jump").forEach((btn) => {
    btn.addEventListener("click", () => selectPlace(btn.dataset.placeId));
  });
  focusDetailPanel();
  if (travelPlace) state.map.setView([travelPlace.lat, travelPlace.lng], mapFocusZoom());
  renderTimeline();
  scheduleUserTravelRouteRefresh();
}

function selectPerson(personId) {
  const person = state.people.find((p) => p.id === personId);
  if (!person) return;
  state.activePersonId = personId;
  state.activeContextId = null;
  state.activeEventId = null;
  state.activeFindId = null;
  state.activeCommunityPinId = null;
  state.activeBlueSignId = null;
  clearUserTravelRoute();
  const primary = (person.place_ids || [])[0];
  if (primary) {
    const place = state.places.find((p) => p.id === primary);
    state.activePlaceId = primary;
    if (place && state.map) {
      state.map.setView([place.lat, place.lng], mapFocusZoom());
      state.markers[primary]?.openPopup();
    }
  } else {
    state.activePlaceId = null;
  }
  const el = document.getElementById("detail-panel");
  if (!el) return;
  destroyPlaceMiniMap();
  const places = (person.place_ids || [])
    .map((id) => state.places.find((p) => p.id === id))
    .filter(Boolean);
  const placeLinks = places
    .map(
      (p) =>
        `<button type="button" class="linkish" data-place-id="${p.id}">${p.name}</button>`,
    )
    .join(" · ");
  const travelPlace = primary ? state.places.find((p) => p.id === primary) : null;
  const travelDetail =
    travelPlace && !state.walkMode ? travelHintHtml(travelPlace) : "";
  const travelRow = travelDetail
    ? `<p class="detail-travel walk-travel-hint" aria-label="Reisevei til stedet">${travelDetail}</p>`
    : "";
  el.innerHTML = `
    <h3>${person.name}</h3>
    <div class="meta-row">
      <span class="chip">Person</span>
      ${bindChipHtml(person.bind)}
      <span class="chip">${person.year_from}-${person.year_to}</span>
    </div>
    ${travelRow}
    ${sourceBadgeHtml(person)}
    ${sourceBlockHtml(person)}
    ${mediaFigureHtml(person)}
    <p class="detail-body">${person.summary}</p>
    ${placeLinks ? `<p class="detail-places"><span class="links-label">Steder:</span> ${placeLinks}</p>` : ""}
    <p class="detail-actions"><button type="button" class="detail-back linkish" data-action="clear-selection">Lukk</button></p>
  `;
  el.querySelectorAll(".ep-travel-link").forEach((link) => {
    link.addEventListener("click", (ev) => ev.stopPropagation());
  });
  el.querySelectorAll("[data-place-id]").forEach((btn) => {
    btn.addEventListener("click", () => selectPlace(btn.dataset.placeId));
  });
  focusDetailPanel();
  refreshMarkers();
  refreshPeopleMarkers();
  renderTimeline();
  scheduleUserTravelRouteRefresh();
}

function placesNearPoint(lat, lng, maxM = 450, limit = 4) {
  if (lat == null || lng == null) return [];
  const origin = { lat, lng };
  return state.places
    .map((p) => ({ place: p, meters: haversineMeters(origin, p) }))
    .filter((row) => row.meters <= maxM)
    .sort((a, b) => a.meters - b.meters)
    .slice(0, limit)
    .map((row) => row.place);
}

function selectFind(findId) {
  const find = state.finds.find((f) => f.id === findId);
  if (!find) return;
  state.activePlaceId = null;
  state.activeEventId = null;
  state.activePersonId = null;
  state.activeBlueSignId = null;
  state.activeCommunityPinId = null;
  state.activeFindId = findId;
  clearUserTravelRoute();
  const el = document.getElementById("detail-panel");
  if (!el) return;
  destroyPlaceMiniMap();
  const nearPlaces =
    find.lat != null && find.lng != null
      ? placesNearPoint(find.lat, find.lng)
      : [];
  const nearHtml = nearPlaces.length
    ? `<p class="detail-related-places">Nære stopp: ${nearPlaces
        .map(
          (p) =>
            `<button type="button" class="linkish detail-place-jump" data-place-id="${escapeHtml(p.id)}">${escapeHtml(p.name)}</button>`,
        )
        .join(" · ")}</p>`
    : "";
  el.innerHTML = `
    <h3>${find.title}</h3>
    <div class="meta-row">
      <span class="chip funn-chip">Arkeologisk funn</span>
      <span class="chip chronology">${find.year_display || formatYearLabel(window.OsloHistorieBydel.findYear(find))}</span>
    </div>
    ${mediaFigureHtml(find)}
    <p class="detail-body">${find.summary}</p>
    ${nearHtml}
    <p class="detail-actions"><button type="button" class="detail-back linkish" data-action="clear-selection">Lukk</button></p>
  `;
  el.querySelectorAll(".detail-place-jump").forEach((btn) => {
    btn.addEventListener("click", () => selectPlace(btn.dataset.placeId));
  });
  refreshFindMarkers();
  refreshPeopleMarkers();
  if (find.lat != null && find.lng != null) {
    state.map.setView([find.lat, find.lng], mapFocusZoom());
    state.findMarkers[findId]?.openPopup();
  }
  focusDetailPanel();
}

function selectDistrict(districtId) {
  const sel = document.getElementById("filter-district");
  if (sel) sel.value = districtId;
  state.activePlaceId = null;
  state.activeEventId = null;
  const district = state.districts.find((d) => d.id === districtId);
  if (district?.bbox && state.map) {
    const [minLat, minLng, maxLat, maxLng] = district.bbox;
    state.map.fitBounds(
      [
        [minLat, minLng],
        [maxLat, maxLng],
      ],
      { padding: [32, 32], maxZoom: 14 },
    );
  }
  state.districtMapUi?.restyle?.();
  onFilterChange();
}

function renderTimeline() {
  const list = document.getElementById("timeline-list");
  if (!list) return;
  list.innerHTML = "";
  const events = filterEvents();
  const finds = getFilteredFinds();
  const contexts = filterContextEntries();
  const rows = [
    ...events.map((ev) => ({ kind: "event", year: ev.year, data: ev })),
    ...finds.map((f) => ({
      kind: "find",
      year: window.OsloHistorieBydel.findYear(f),
      data: f,
    })),
    ...contexts.map((c) => ({
      kind: "context",
      year: c.year_from ?? 0,
      data: c,
    })),
  ].sort((a, b) => a.year - b.year);

  let lastHeading = "";
  rows.forEach((row) => {
    if (row.kind === "event") {
    const ev = row.data;
    const heading = centuryHeading(ev.year);
    if (heading !== lastHeading) {
      lastHeading = heading;
      const head = document.createElement("li");
      head.className = "timeline-century";
      head.innerHTML = `<span>${heading}</span>`;
      list.appendChild(head);
    }

    const li = document.createElement("li");
    const card = document.createElement("article");
    card.className = "event-card" + (state.activeEventId === ev.id ? " active" : "");
    card.dataset.eventId = ev.id;

    card.innerHTML = `
      <div class="year">${ev.year_display || ev.year}</div>
      <h3>${ev.title}</h3>
      <p class="event-teaser">${ev.summary}</p>
      <div class="meta-row">
        ${bindChipHtml(ev.bind)}
        ${tagChipsHtml(ev.tags)}
      </div>
    `;
    card.addEventListener("click", () => selectEvent(ev.id));
    li.appendChild(card);
    list.appendChild(li);
    return;
    }
    if (row.kind === "find") {
    const find = row.data;
    const heading = centuryHeading(row.year);
    if (heading !== lastHeading) {
      lastHeading = heading;
      const head = document.createElement("li");
      head.className = "timeline-century";
      head.innerHTML = `<span>${heading}</span>`;
      list.appendChild(head);
    }
    const li = document.createElement("li");
    const card = document.createElement("article");
    card.className = "event-card event-card-find";
    card.innerHTML = `
      <div class="year">${find.year_display || formatYearLabel(row.year)}</div>
      <h3>${find.title}</h3>
      <p class="event-teaser">${find.summary}</p>
      <div class="meta-row"><span class="chip">Funn</span></div>
    `;
    card.addEventListener("click", () => selectFind(find.id));
    li.appendChild(card);
    list.appendChild(li);
    return;
    }
    if (row.kind === "context") {
    const ctx = row.data;
    const heading = centuryHeading(row.year);
    if (heading !== lastHeading) {
      lastHeading = heading;
      const head = document.createElement("li");
      head.className = "timeline-century";
      head.innerHTML = `<span>${heading}</span>`;
      list.appendChild(head);
    }
    const li = document.createElement("li");
    const card = document.createElement("article");
    card.className =
      "event-card event-card-context" + (state.activeContextId === ctx.id ? " active" : "");
    card.innerHTML = `
      <div class="year">${ctx.year_display || formatYearLabel(row.year)}</div>
      <h3>${ctx.title}</h3>
      <p class="event-teaser">${ctx.summary}</p>
      <div class="meta-row">
        <span class="chip">Bakgrunn</span>
        ${bindChipHtml(ctx.bind)}
        ${tagChipsHtml(ctx.tags)}
      </div>
    `;
    card.addEventListener("click", () => selectContext(ctx.id));
    li.appendChild(card);
    list.appendChild(li);
    }
  });

  if (!rows.length) {
    list.innerHTML =
      "<li class='timeline-empty'>Ingen hendelser eller funn med valgte filtre. <button type='button' class='linkish timeline-reset' data-action='reset-filters'>Nullstill filtre</button></li>";
    list.querySelector("[data-action='reset-filters']")?.addEventListener("click", resetFilters);
  }
}

function renderDetail() {
  const el = document.getElementById("detail-panel");
  const place = state.places.find((p) => p.id === state.activePlaceId);
  const event = state.events.find((e) => e.id === state.activeEventId);
  const blueSign = state.blueSigns.find((s) => s.id === state.activeBlueSignId);
  const communityPin = state.activeCommunityPinId
    ? findCommunityPin(state.activeCommunityPinId)
  : null;

  destroyPlaceMiniMap();

  const { district } = getFilters();
  if (!place && !event && !blueSign && !communityPin && district !== "all") {
    renderDistrictPanel(district);
    return;
  }

  if (blueSign && !place && !event) {
    const detailActions = state.walkMode
      ? ""
      : '<p class="detail-actions"><button type="button" class="detail-back linkish" data-action="clear-selection">Lukk og utforsk videre</button></p>';
    el.innerHTML = `
      <h3>${blueSign.name}</h3>
      <div class="meta-row">
        <span class="chip blaa-skilt-chip">Blå skilt</span>
        ${tagChipsHtml(blueSign.tags)}
      </div>
      ${blueSign.address ? `<p class="detail-muted">${blueSign.address}</p>` : ""}
      <p class="detail-body">${blueSign.summary}</p>
      <p class="detail-muted">Kulturhistorisk skilt.</p>
      ${detailActions}
    `;
    return;
  }

  if (communityPin && !place && !event && !blueSign) {
    const tags = (communityPin.hashtags || []).join(" ");
    const detailActions = state.walkMode
      ? ""
      : `<p class="detail-actions"><button type="button" class="detail-back linkish" data-action="clear-selection">Lukk og utforsk videre</button> <button type="button" class="detail-back linkish" data-action="copy-community-pin">Kopier JSON</button> <button type="button" class="detail-back linkish" data-action="delete-community-pin">Slett dette bidraget</button></p>`;
    el.innerHTML = `
      <h3>${escapeHtml(communityPin.title)}</h3>
      <div class="meta-row">
        <span class="chip community-chip">Brukerbidrag</span>
        ${tags ? `<span class="chip">${escapeHtml(tags)}</span>` : ""}
      </div>
      ${communityPin.address ? `<p class="detail-muted">${escapeHtml(communityPin.address)}</p>` : ""}
      <p class="detail-body">${escapeHtml(communityPin.story)}</p>
      <p class="detail-muted">Lagret lokalt på denne enheten.</p>
      <p class="detail-muted community-copy-hint" hidden aria-live="polite"></p>
      ${detailActions}
    `;
    focusDetailPanel();
    return;
  }

  if (!place && !event) {
    if (district !== "all") return;
    renderExploreWelcome();
    return;
  }

  const detailActions = state.walkMode
    ? ""
  : '<p class="detail-actions"><button type="button" class="detail-back linkish" data-action="clear-selection">Lukk og utforsk videre</button></p>';

  if (place) {
    const links = (place.external_links || [])
      .map((l) => `<a href="${l.url}" target="_blank" rel="noopener">${l.label}</a>`)
      .join(" · ");
    const ep = state.episodes.find((e) => e.id === place.episode_id);
    const yearSpan =
      place.year_from != null
        ? `<span class="chip">${place.year_from}${place.year_to && place.year_to !== place.year_from ? `-${place.year_to}` : ""}</span>`
        : "";
    const travelDetail = !state.walkMode ? travelHintHtml(place) : "";
    const travelRow = travelDetail
      ? `<p class="detail-travel walk-travel-hint" aria-label="Reisevei fra posisjonen din">${travelDetail}</p>`
      : "";
    el.innerHTML = `
      <h3>${place.name}</h3>
      ${walkRouteBannerHtml()}
      <div class="meta-row">
        ${bindChipHtml(place.bind)}
        ${yearSpan}
        ${ep ? `<span class="chip lope">${ep.title}</span>` : ""}
        ${tagChipsHtml(place.tags)}
        ${placeHasBlaaSkilt(place) ? `<span class="chip blaa-skilt-chip">Blå skilt</span>` : ""}
      </div>
      ${travelRow}
      ${sourceBadgeHtml(place)}
      ${sourceBlockHtml(place)}
      ${bindSourceLinksHtml(place.bind)}
      ${placeVisualHtml(place)}
      <p class="detail-body">${place.summary}</p>
      ${peopleLinksHtml(place)}
      ${links ? `<p class="popup-links"><span class="links-label">Les mer:</span> ${links}</p>` : ""}
      ${detailActions}
    `;
    el.querySelectorAll(".ep-travel-link").forEach((link) => {
      link.addEventListener("click", (ev) => ev.stopPropagation());
    });
    requestAnimationFrame(() => {
      initPlaceMiniMap(place);
      focusDetailPanel();
    });
    scheduleUserTravelRouteRefresh();
    return;
  }

  const evEp = state.episodes.find((e) => e.id === event.episode_id);
  const travelPlace = event.place_ids?.length
    ? state.places.find((p) => p.id === event.place_ids[0])
    : null;
  const travelDetail = travelPlace && !state.walkMode ? travelHintHtml(travelPlace) : "";
  const travelRow = travelDetail
    ? `<p class="detail-travel walk-travel-hint" aria-label="Reisevei til stedet">${travelDetail}</p>`
    : "";
  const eventPlaces = (event.place_ids || [])
    .map((id) => state.places.find((p) => p.id === id))
    .filter(Boolean);
  const placeLinks = eventPlaces.length
    ? `<p class="detail-related-places">Steder: ${eventPlaces
        .map(
          (p) =>
            `<button type="button" class="linkish detail-place-jump" data-place-id="${escapeHtml(p.id)}">${escapeHtml(p.name)}</button>`,
        )
        .join(" · ")}</p>`
    : "";
  el.innerHTML = `
    <h3>${event.title}</h3>
    <div class="meta-row">
      ${bindChipHtml(event.bind)}
      <span class="chip">${event.year_display || event.year}</span>
      ${evEp ? `<span class="chip lope">${evEp.title}</span>` : ""}
      ${tagChipsHtml(event.tags)}
    </div>
    ${travelRow}
    ${sourceBadgeHtml(event)}
    ${sourceBlockHtml(event)}
    ${bindSourceLinksHtml(event.bind)}
    <p class="detail-body">${event.summary}</p>
    ${placeLinks}
    ${detailActions}
  `;
  el.querySelectorAll(".ep-travel-link").forEach((link) => {
    link.addEventListener("click", (ev) => ev.stopPropagation());
  });
  el.querySelectorAll(".detail-place-jump").forEach((btn) => {
    btn.addEventListener("click", () => selectPlace(btn.dataset.placeId));
  });
  focusDetailPanel();
  scheduleUserTravelRouteRefresh();
}

function clearSelection() {
  if (state.walkMode) return;
  state.activePlaceId = null;
  state.activeEventId = null;
  state.activePersonId = null;
  state.activeContextId = null;
  state.activeBlueSignId = null;
  state.activeFindId = null;
  state.activeCommunityPinId = null;
  clearUserTravelRoute();
  if (state.exploreMarker) {
    state.exploreMarker.remove();
    state.exploreMarker = null;
  }
  clearSearchMarker();
  setSearchStatus("");
  const input = document.getElementById("map-search");
  if (input) input.value = "";
  hideSearchSuggest();
  renderTimeline();
  renderDetail();
  refreshMarkers();
}

function filtersActiveCount() {
  const f = getFilters();
  let n = 0;
  if (f.century !== "all") n += 1;
  if (f.tag !== "all") n += 1;
  if (f.episode !== "all") n += 1;
  if (f.district !== "all") n += 1;
  if (f.chronology !== "all") n += 1;
  if (f.destination && f.destination !== "all") n += 1;
  if (f.yearMin !== state.chronologyYearMin) n += 1;
  if (f.yearMax !== state.chronologyYearMax) n += 1;
  return n;
}

function resetFilters() {
  if (state.walkMode) {
    exitWalkMode({ returnMode: state.sidePanelMode === "explore" ? "explore" : "routes" });
  }
  document.getElementById("filter-century").value = "all";
  document.getElementById("filter-tag").value = "all";
  const dest = document.getElementById("filter-destination");
  if (dest) dest.value = "all";
  document.getElementById("filter-episode").value = "all";
  const dist = document.getElementById("filter-district");
  if (dist) dist.value = "all";
  const chrono = document.getElementById("filter-chronology");
  if (chrono) chrono.value = "all";
  const yearMinEl = document.getElementById("year-min");
  const yearMaxEl = document.getElementById("year-max");
  if (yearMinEl) yearMinEl.value = String(state.chronologyYearMin);
  if (yearMaxEl) yearMaxEl.value = String(state.chronologyYearMax);
  state.lastMapFitKey = "";
  clearSelection();
  renderEpisodeCards();
  onFilterChange();
}

function updateFilterChrome() {
  const placeCountEl = document.getElementById("map-place-count");
  const f = getFilters();
  if (placeCountEl && f.destination === "community") {
    const n = loadCommunityPins().length;
    placeCountEl.textContent = n
      ? `${n} lokalt bidrag på kartet`
      : "Ingen lokale bidrag ennå - bruk Del sted.";
  }
  const count = filterPlaces().length + filterStandaloneBlueSigns().length;
  if (placeCountEl && f.destination !== "community") {
  const communityN =
    state.siteConfig?.community_tags_enabled &&
    f.destination === "all" &&
    f.episode === "all"
      ? loadCommunityPins().length
      : 0;
    if (count || communityN) {
      const base = count
        ? `${count} destinasjon${count === 1 ? "" : "er"} på kartet`
        : "Ingen kuraterte steder med valgte filtre";
      placeCountEl.textContent = communityN
        ? `${base} · ${communityN} lokalt bidrag`
        : `${base}${count ? " nå" : ""}`;
    } else {
      placeCountEl.textContent = "Ingen steder med valgte filtre - bruk Nullstill filtre.";
    }
  }
  const active = filtersActiveCount();
  const summaryEl = document.getElementById("filters-summary-text");
  if (summaryEl) {
    summaryEl.textContent = active ? `Filtre (${active} aktive)` : "Filtre";
  }
  const resetBtn = document.getElementById("btn-reset-filters");
  if (resetBtn) resetBtn.hidden = active === 0;
}

function selectEvent(eventId) {
  const ev = state.events.find((e) => e.id === eventId);
  if (!ev) return;
  state.activeEventId = eventId;
  state.activePlaceId = ev.place_ids?.[0] || null;
  state.activePersonId = null;
  state.activeContextId = null;
  state.activeBlueSignId = null;
  state.activeCommunityPinId = null;
  renderTimeline();
  renderDetail();
  scrollTimelineToActive();

  if (state.activePlaceId && state.markers[state.activePlaceId]) {
    const p = state.places.find((x) => x.id === state.activePlaceId);
    state.map.setView([p.lat, p.lng], mapFocusZoom());
    state.markers[state.activePlaceId].openPopup();
  }
}

function selectBlueSign(signId, options = { pan: true }) {
  const sign = state.blueSigns.find((s) => s.id === signId);
  if (!sign) return;
  if (sign.place_id) {
    selectPlace(sign.place_id, options);
    return;
  }
  state.activeBlueSignId = signId;
  state.activePlaceId = null;
  state.activeCommunityPinId = null;
  state.activePersonId = null;
  state.activeContextId = null;
  state.activeEventId = null;
  setSidePanelMode("explore");
  renderTimeline();
  renderDetail();
  if (options.pan) {
    state.map.setView([sign.lat, sign.lng], mapFocusZoom());
    state.blueSignMarkers[signId]?.openPopup();
  }
  refreshMarkers();
  focusDetailPanel();
}

function selectPlace(placeId, options = { pan: true }) {
  const place = state.places.find((p) => p.id === placeId);
  if (!place) return;
  state.activePlaceId = placeId;
  state.activeBlueSignId = null;
  state.activeCommunityPinId = null;
  state.activePersonId = null;
  state.activeContextId = null;
  const linked = state.events.find((e) => (e.place_ids || []).includes(placeId));
  if (linked) state.activeEventId = linked.id;
  if (state.walkMode) {
    const places = getWalkPlaces();
    const idx = places.findIndex((p) => p.id === placeId);
    if (idx >= 0) {
      state.walkIndex = idx;
      updateWalkBar();
    }
    setSidePanelMode("explore");
  }
  renderTimeline();
  renderDetail();
  if (state.activeEventId) scrollTimelineToActive();
  if (options.pan) {
    state.map.setView([place.lat, place.lng], mapFocusZoom());
    state.markers[placeId]?.openPopup();
  }
  refreshMarkers();
  focusDetailPanel();
}

function populateFilters() {
  const centurySel = document.getElementById("filter-century");
  state.centuries
    .filter((c) => c.id !== "all")
    .forEach((c) => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.label;
      centurySel.appendChild(opt);
    });

  const tagSel = document.getElementById("filter-tag");
  if (state.tagGroups.length) {
    state.tagGroups.forEach((group) => {
      const og = document.createElement("optgroup");
      og.label = group.label;
      (group.tag_ids || []).forEach((id) => {
        const t = state.tags.find((x) => x.id === id);
        if (!t) return;
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.textContent = t.label;
        og.appendChild(opt);
      });
      tagSel.appendChild(og);
    });
  } else {
    state.tags.forEach((t) => {
      const opt = document.createElement("option");
      opt.value = t.id;
      opt.textContent = t.label;
      tagSel.appendChild(opt);
    });
  }

  const epSel = document.getElementById("filter-episode");
  state.eras.forEach((era) => {
    const groupEps = state.episodes.filter((e) => e.era_id === era.id);
    if (!groupEps.length) return;
    const og = document.createElement("optgroup");
    og.label = era.label;
    groupEps.forEach((ep) => {
      const opt = document.createElement("option");
      opt.value = ep.id;
      opt.textContent = ep.title;
      og.appendChild(opt);
    });
    epSel.appendChild(og);
  });
  const ungrouped = state.episodes.filter((e) => !e.era_id);
  ungrouped.forEach((ep) => {
    const opt = document.createElement("option");
    opt.value = ep.id;
    opt.textContent = ep.title;
    epSel.appendChild(opt);
  });
  epSel.value = state.siteConfig.primary_mode === "explore" ? "all" : state.currentEpisodeId;

  const distSel = document.getElementById("filter-district");
  if (distSel) {
    state.districts.forEach((d) => {
      const opt = document.createElement("option");
      opt.value = d.id;
      opt.textContent = d.name;
      distSel.appendChild(opt);
    });
  }

  const chronoSel = document.getElementById("filter-chronology");
  if (chronoSel) {
    state.chronologyEras.forEach((era) => {
      const opt = document.createElement("option");
      opt.value = era.id;
      opt.textContent = `${era.label} (${era.short || ""})`;
      chronoSel.appendChild(opt);
    });
  }

  const yearMinEl = document.getElementById("year-min");
  const yearMaxEl = document.getElementById("year-max");
  if (yearMinEl) {
    yearMinEl.min = String(state.chronologyYearMin);
    yearMinEl.max = String(state.chronologyYearMax);
    yearMinEl.value = String(state.chronologyYearMin);
  }
  if (yearMaxEl) {
    yearMaxEl.min = String(state.chronologyYearMin);
    yearMaxEl.max = String(state.chronologyYearMax);
    yearMaxEl.value = String(state.chronologyYearMax);
  }

}

function onFilterChange() {
  refreshMarkers();
  renderTimeline();
  renderDetail();
  updateFilterChrome();
  const f = getFilters();
  const fitKey = `${f.episode}|${f.district}`;
  if (fitKey === state.lastMapFitKey || !state.map) return;
  state.lastMapFitKey = fitKey;
  if (f.district !== "all") {
    const district = state.districts.find((d) => d.id === f.district);
    if (district?.bbox) {
      const [minLat, minLng, maxLat, maxLng] = district.bbox;
      state.map.fitBounds(
        [
          [minLat, minLng],
          [maxLat, maxLng],
        ],
        { padding: [32, 32], maxZoom: 14 },
      );
    }
    return;
  }
  if (f.episode !== "all") {
    const ep = state.episodes.find((e) => e.id === f.episode);
    const mapIds = ep?.map_place_order;
    const bounds =
      mapIds?.length
        ? mapIds.map((id) => state.places.find((p) => p.id === id)).filter(Boolean)
        : filterPlaces();
    if (bounds.length) {
      const latlngs = bounds.map((p) => [p.lat, p.lng]);
      state.map.fitBounds(latlngs, { padding: [48, 48], maxZoom: mapIds?.length ? 15 : 17 });
    }
  }
}

function getWalkPlaces() {
  const ep = state.episodes.find((e) => e.id === state.currentEpisodeId);
  if (!ep || !ep.place_order.length) return [];
  return ep.place_order
    .map((id) => state.places.find((p) => p.id === id))
    .filter(Boolean);
}

function updateWalkBar() {
  const bar = document.getElementById("walk-bar");
  if (!bar) return;
  const places = getWalkPlaces();
  if (!state.walkMode || !places.length) {
    bar.classList.remove("visible");
    return;
  }
  bar.classList.add("visible");
  renderWalkProgress(state.userMarker ? distanceToNextStopText() : "");
  if (state.userMarker) scheduleUserTravelRouteRefresh();
  document.getElementById("walk-prev").disabled = state.walkIndex === 0;
  document.getElementById("walk-next").disabled = state.walkIndex >= places.length - 1;
}

function startWalk(episodeId) {
  if (!episodeId) return;
  const ep = state.episodes.find((e) => e.id === episodeId);
  if (!ep?.place_order?.length) return;
  state.currentEpisodeId = episodeId;
  const epSel = document.getElementById("filter-episode");
  if (epSel) epSel.value = state.currentEpisodeId;
  state.walkMode = true;
  state.walkIndex = 0;
  document.body.classList.add("side-mode-walking");
  renderEpisodeCards();
  onFilterChange();
  const places = getWalkPlaces();
  setSidePanelMode("explore");
  if (places[0]) selectPlace(places[0].id, { pan: true });
  else updateWalkBar();
  refreshWalkRoute();
  refreshMarkers();
  requestAnimationFrame(() => state.map?.invalidateSize());
  if (state.siteConfig.enable_geolocation) startGeolocation();
}

function walkStep(delta) {
  const places = getWalkPlaces();
  if (!places.length) return;
  state.walkIndex = Math.max(0, Math.min(places.length - 1, state.walkIndex + delta));
  if (places[state.walkIndex]) selectPlace(places[state.walkIndex].id);
  if (state.siteConfig.enable_geolocation) startGeolocation();
}

function bindUi() {
  bindUiJumpLinks();
  ["filter-destination", "filter-century", "filter-tag", "filter-episode", "filter-district", "filter-chronology"].forEach(
    (id) => {
      const el = document.getElementById(id);
      if (!el) return;
      el.addEventListener("change", () => {
        if (state.walkMode && id === "filter-episode") {
          const ep = document.getElementById("filter-episode").value;
          if (ep !== state.currentEpisodeId) {
            document.getElementById("filter-episode").value = state.currentEpisodeId;
            return;
          }
        }
        const ep = document.getElementById("filter-episode").value;
        if (ep !== "all") {
          state.currentEpisodeId = ep;
        } else if (!state.walkMode) {
          state.lastMapFitKey = "";
        }
        renderEpisodeCards();
        onFilterChange();
        updateWalkBar();
      });
    },
  );

  ["year-min", "year-max"].forEach((id) => {
    const el = document.getElementById(id);
    if (!el) return;
    const handler = () => {
      const f = getFilters();
      if (f.yearMin > f.yearMax) {
        if (id === "year-min") document.getElementById("year-max").value = String(f.yearMin);
        else document.getElementById("year-min").value = String(f.yearMax);
      }
      onFilterChange();
    };
    el.addEventListener("change", handler);
    el.addEventListener("input", handler);
  });

  document.getElementById("mode-tab-explore")?.addEventListener("click", () => setSidePanelMode("explore"));
  document.getElementById("mode-tab-routes")?.addEventListener("click", () => setSidePanelMode("routes"));

  document.getElementById("home-btn-search")?.addEventListener("click", () => dismissHome("explore"));
  document.getElementById("home-btn-routes")?.addEventListener("click", () => dismissHome("routes"));
  document.getElementById("home-btn-share")?.addEventListener("click", () =>
    runUiAction("home-share"),
  );
  document.getElementById("btn-map-share")?.addEventListener("click", () => runUiAction("community-tag"));
  document.getElementById("btn-back-home")?.addEventListener("click", (e) => {
    e.preventDefault();
    showHomeScreen();
  });

  window.addEventListener("popstate", () => {
    const parsed = parseAppRoute();
    if (!parsed) {
      applyRouteFromUrl({ forceUrl: true });
      return;
    }
    if (parsed.view === "home") {
      showHomeScreen({ fromHistory: true });
      return;
    }
    if (isHomeActive()) {
      leaveHomeScreenDom(parsed.mode);
    } else {
      setSidePanelMode(parsed.mode, { skipHomeDismiss: true, skipRouteSync: true });
    }
  });

  document.getElementById("walk-prev")?.addEventListener("click", () => walkStep(-1));
  document.getElementById("walk-next")?.addEventListener("click", () => walkStep(1));
  document.getElementById("walk-exit")?.addEventListener("click", () => {
    exitWalkMode({ returnMode: "routes" });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (state.communityMapPick) {
      exitCommunityMapPick();
      const dlg = document.getElementById("community-tag-dialog");
      if (dlg && typeof dlg.showModal === "function") dlg.showModal();
      return;
    }
    if (state.walkMode) {
      exitWalkMode({ returnMode: state.sidePanelMode === "explore" ? "explore" : "routes" });
      return;
    }
    if (state.activePlaceId || state.activeEventId || state.activeFindId || state.activePersonId) {
      clearSelection();
      return;
    }
    if (!isHomeActive()) {
      showHomeScreen();
    }
  });

  document.getElementById("mode-tab-explore")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      setSidePanelMode("explore");
    }
  });
  document.getElementById("mode-tab-routes")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      setSidePanelMode("routes");
    }
  });

  const locateBtn = document.getElementById("btn-map-locate");
  if (locateBtn) {
    locateBtn.addEventListener("click", () => {
      if (!navigator.geolocation) {
        const statusEl = document.getElementById("nearby-status");
        if (statusEl) {
          statusEl.textContent = "Nettleseren støtter ikke posisjon.";
        }
        return;
      }
      if (state.geoActive && state.followUser) {
        state.followUser = false;
        setLocateButtonState();
        return;
      }
      state.followUser = true;
      startGeolocationWatch();
    });
  }

  document.getElementById("btn-reset-filters")?.addEventListener("click", resetFilters);

  const detailPanel = document.getElementById("detail-panel");
  if (detailPanel) {
    detailPanel.addEventListener("click", (e) => {
      if (e.target.closest("[data-action='clear-selection']")) clearSelection();
      if (e.target.closest("[data-action='delete-community-pin']")) {
        const pinId = state.activeCommunityPinId;
        if (pinId) deleteCommunityPin(pinId);
      }
      if (e.target.closest("[data-action='copy-community-pin']")) {
        const pinId = state.activeCommunityPinId;
        if (pinId) copyCommunityPinJson(pinId);
      }
      const personBtn = e.target.closest("[data-person-id]");
      if (personBtn?.dataset.personId) selectPerson(personBtn.dataset.personId);
    });
  }

  const searchForm = document.getElementById("map-search-form");
  const searchInput = document.getElementById("map-search");
  if (searchForm && searchInput && state.siteConfig.search_places_and_addresses !== false) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      runMapSearch(searchInput.value);
    });
    searchInput.addEventListener("input", onSearchInput);
    searchInput.addEventListener("focus", onSearchInput);
  }
}

function renderExploreWelcome() {
  const el = document.getElementById("detail-panel");
  if (!el) return;
  const shortcuts = [
    { id: "kvadraturen-1600", label: "Kvadraturen" },
    { id: "akerselva-tidlig", label: "Akerselva" },
    { id: "1814-hovedstaden", label: "1814" },
    { id: "mot-1924", label: "Mot 1924" },
  ];
  const chips = shortcuts
    .map(
      (s) =>
        `<button type="button" class="quick-start-btn" data-episode-id="${s.id}">${s.label}</button>`,
    )
    .join("");
  el.innerHTML = `
    <h3>Utforsk på kartet</h3>
    <p>Trykk et merke, velg en hendelse i tidslinjen, eller trykk på kartet. Bruk Min posisjon for forslag i nærheten.</p>
    <p class="quick-start-label">Eller gå en ferdig rute:</p>
    <div class="quick-start-row" role="group" aria-label="Hurtigvalg gåtur">${chips}</div>
    <p class="detail-muted">Flere ruter finner du under fanen Gå rute.</p>
  `;
  el.querySelectorAll(".quick-start-btn").forEach((btn) => {
    btn.addEventListener("click", () => startWalk(btn.dataset.episodeId));
  });
}

function recoverSpaPathFromStorage() {
  try {
    const saved = sessionStorage.getItem("kristiania-spa-path");
    if (!saved) return;
    sessionStorage.removeItem("kristiania-spa-path");
    const u = new URL(saved, window.location.origin);
    if (u.pathname && u.pathname !== window.location.pathname) {
      history.replaceState(null, "", u.pathname + u.search + u.hash);
    }
  } catch {
    /* ignore */
  }
}

async function init() {
  recoverSpaPathFromStorage();
  const boot = document.getElementById("detail-panel");
  if (boot) {
    boot.innerHTML = '<p class="detail-muted">Laster kart og historie...</p>';
  }
  document.body.classList.add("app-loading");
  await loadData();
  document.body.classList.remove("app-loading");
  applyBranding();
  applySiteUi();
  populateFilters();
  initMap();
  bindUi();
  initCommunityTagUi();
  applyRouteFromUrl();
  renderEpisodeCards();
  if (state.siteConfig.primary_mode === "explore") {
    document.getElementById("filter-episode").value = "all";
  }
  onFilterChange();
  renderMapLegend();
  renderExploreWelcome();
  renderTimeline();
  updateWalkBar();
  setLocateButtonState();
  if (state.siteConfig.enable_geolocation) {
    refreshGeolocationPermissionState();
    if (state.siteConfig.geolocation_follow_default === true) {
      startGeolocationWatch();
    }
  }
  requestAnimationFrame(() => {
    state.map?.invalidateSize();
  });
}

init().catch((err) => {
  console.error(err);
  document.body.classList.remove("app-loading");
  const boot = document.getElementById("detail-panel");
  const msg = `Kunne ikke laste data. Kjør .\\scripts\\serve.ps1 og åpne http://localhost:8080/ (${err?.message || err})`;
  if (boot) boot.innerHTML = `<p class="detail-muted">${msg}</p>`;
  document.body.insertAdjacentHTML(
    "beforeend",
    `<p style="color:${BIND_COLORS[1]};padding:1rem">${msg}</p>`,
  );
});