/* global L */

window.OsloHistorieBydel = (() => {
  const ACTIVE_STYLE = {
    fillColor: "#2a6f97",
    fillOpacity: 0.22,
    color: "#1e2433",
    weight: 2,
  };
  const IDLE_STYLE = {
    fillColor: "#2a6f97",
    fillOpacity: 0.07,
    color: "#5c6370",
    weight: 1,
  };

  function districtIdAt(lat, lng, districts) {
    for (const d of districts || []) {
      const [minLat, minLng, maxLat, maxLng] = d.bbox;
      if (lat >= minLat && lat <= maxLat && lng >= minLng && lng <= maxLng) return d.id;
    }
    return null;
  }

  function assignDistrictsToPlaces(places, districts) {
    (places || []).forEach((p) => {
      if (!p.district_id && p.lat != null && p.lng != null) {
        p.district_id = districtIdAt(p.lat, p.lng, districts);
      }
    });
  }

  function chronologyEra(id, eras) {
    return (eras || []).find((e) => e.id === id);
  }

  function yearInEra(year, era) {
    if (!era || year == null) return true;
    const from = era.year_from;
    const to = era.year_to;
    if (from != null && year < from) return false;
    if (to != null && year > to) return false;
    return true;
  }

  function findYear(f) {
    return f.year_from ?? f.year_to ?? 0;
  }

  function filterFinds(finds, { district, chronology, yearMin, yearMax, chronologyEras }) {
    const eraDef = chronology !== "all" ? chronologyEra(chronology, chronologyEras) : null;
    return (finds || []).filter((f) => {
      const y = findYear(f);
      if (yearMin != null && y < yearMin) return false;
      if (yearMax != null && y > yearMax) return false;
      if (district !== "all" && f.district_id !== district) return false;
      if (chronology !== "all") {
        if (f.chronology_era_id && f.chronology_era_id !== chronology) return false;
        if (!yearInEra(y, eraDef)) return false;
      }
      return true;
    });
  }

  function createDistrictLayers(map, geojson, { onSelect, getActiveId, maxZoomHighlight }) {
    const layer = L.geoJSON(geojson, {
      style: (feature) => {
        const id = feature.properties?.id;
        return getActiveId() === id ? { ...ACTIVE_STYLE } : { ...IDLE_STYLE };
      },
      onEachFeature: (feature, l) => {
        const name = feature.properties?.name || "";
        l.bindTooltip(name, {
          permanent: false,
          direction: "center",
          className: "bydel-tip",
        });
        l.on("click", () => {
          if (feature.properties?.id) onSelect(feature.properties.id);
        });
      },
    });
    layer.addTo(map);

    function restyle() {
      const z = map.getZoom();
      const maxHi = maxZoomHighlight ?? 13;
      const emphasize = z <= maxHi;
      const streetZoom = z >= maxHi + 2;
      layer.eachLayer((l) => {
        const id = l.feature?.properties?.id;
        const base = getActiveId() === id ? ACTIVE_STYLE : IDLE_STYLE;
        let fillOpacity = emphasize ? base.fillOpacity + 0.06 : base.fillOpacity * 0.6;
        let weight = emphasize ? base.weight : 0.5;
        if (streetZoom) {
          fillOpacity = getActiveId() === id ? 0.06 : 0;
          weight = getActiveId() === id ? 1.2 : 0;
        }
        l.setStyle({
          ...base,
          fillOpacity,
          weight,
        });
        if (emphasize) l.bringToBack();
      });
    }

    map.on("zoomend", restyle);
    restyle();
    return { layer, restyle };
  }

  return {
    districtIdAt,
    assignDistrictsToPlaces,
    filterFinds,
    chronologyEra,
    yearInEra,
    createDistrictLayers,
    findYear,
  };
})();