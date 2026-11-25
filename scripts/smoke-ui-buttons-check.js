/**
 * Kjøres i nettleser (f.eks. via CDP) mot ferdig lastet app.
 * Returnerer { pass: boolean, results: { name, ok, detail }[] }.
 */
(async () => {
  const results = [];
  const note = (name, ok, detail = "") => results.push({ name, ok, detail });
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  for (let i = 0; i < 80; i += 1) {
    const loaded =
      document.body.classList.contains("app-ready") &&
      document.querySelector("#timeline-list li");
    if (loaded) break;
    await sleep(100);
  }
  note("app-loaded", !!document.querySelector("#timeline-list li"));

  if (document.body.classList.contains("home-active")) {
    const homeSearch = document.getElementById("home-btn-search");
    if (homeSearch) {
      homeSearch.click();
      await sleep(200);
    }
    note("home-dismiss", !document.body.classList.contains("home-active"));
  }

  const clickId = (id) => {
    const el = document.getElementById(id);
    if (!el) return false;
    el.click();
    return true;
  };

  if (!clickId("mode-tab-explore")) note("mode-tab-explore", false, "mangler");
  else {
    await sleep(80);
    note("mode-tab-explore", !document.getElementById("panel-explore")?.hidden);
  }

  if (!clickId("mode-tab-routes")) note("mode-tab-routes", false, "mangler");
  else {
    await sleep(80);
    const routes = !document.getElementById("panel-routes")?.hidden;
    const cards = document.querySelectorAll("#episode-cards .episode-card-btn").length;
    note("mode-tab-routes", routes, `ruter=${cards}`);
    note("episode-card-btns", cards === 6, `fant ${cards}`);
  }

  clickId("mode-tab-explore");
  await sleep(80);
  document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  await sleep(80);

  let quick = document.querySelectorAll(".quick-start-btn");
  if (!quick.length) {
    const welcomeH3 = document.querySelector("#detail-panel h3");
    if (welcomeH3?.textContent !== "Utforsk på kartet") {
      note("quick-start-btns", false, "ingen hurtigstart (ikke velkomst)");
    }
  }
  note("quick-start-btns", quick.length === 4, `fant ${quick.length}`);
  if (quick[0]) {
    quick[0].click();
    await sleep(350);
    const walking = document.body.classList.contains("side-mode-walking");
    note("quick-start-walk", walking);
    note("walk-bar-visible", document.getElementById("walk-bar")?.classList.contains("visible"));
    clickId("walk-next");
    await sleep(120);
    const prog = document.getElementById("walk-progress")?.textContent || "";
    note("walk-next", /Stopp 2 av/.test(prog), prog.slice(0, 40));
    clickId("walk-prev");
    await sleep(120);
    const prog2 = document.getElementById("walk-progress")?.textContent || "";
    note("walk-prev", /Stopp 1 av/.test(prog2));
    clickId("walk-exit");
    await sleep(200);
    note("walk-exit", !document.body.classList.contains("side-mode-walking"));
  }

  clickId("mode-tab-routes");
  await sleep(80);
  const epBtn = document.querySelector("#episode-cards .episode-card-btn");
  if (epBtn) {
    epBtn.click();
    await sleep(350);
    note("episode-card-start", document.body.classList.contains("side-mode-walking"));
    clickId("walk-exit");
    await sleep(200);
  }

  clickId("mode-tab-explore");
  await sleep(80);

  const locate = document.getElementById("btn-map-locate");
  if (locate) {
    locate.click();
    await sleep(500);
    const on1 = locate.getAttribute("aria-pressed") === "true";
    note("btn-map-locate-on", on1, locate.textContent);
    locate.click();
    await sleep(100);
    note("btn-map-locate-pause", locate.getAttribute("aria-pressed") === "false");
    locate.click();
    await sleep(200);
    note("btn-map-locate-resume", locate.getAttribute("aria-pressed") === "true");
    const nearby = document.querySelectorAll("#nearby-list .nearby-btn").length;
    note("nearby-btns", nearby > 0, `liste=${nearby}`);
    const nb = document.querySelector("#nearby-list .nearby-btn");
    if (nb) {
      nb.click();
      await sleep(200);
      note("nearby-pick", !!document.querySelector("#detail-panel h3"));
      const close = document.querySelector("[data-action='clear-selection']");
      if (close) {
        close.click();
        await sleep(100);
        note("detail-lukk", !document.querySelector("[data-action='clear-selection']"));
      } else note("detail-lukk", false, "ingen lukk-knapp");
    }
  } else note("btn-map-locate", false, "mangler");

  const searchInput = document.getElementById("map-search");
  if (searchInput) {
    searchInput.value = "Akershus festning";
    searchInput.dispatchEvent(new Event("input", { bubbles: true }));
    await sleep(200);
    const sug = document.querySelector("#map-search-suggest .map-search-option");
    if (sug) {
      sug.click();
      await sleep(200);
      note("search-suggest", !!document.querySelector("#detail-panel h3"));
    } else {
      document.getElementById("map-search-form")?.requestSubmit();
      await sleep(200);
      note("btn-map-search", !!document.querySelector("#detail-panel h3"));
    }
  }

  const century = document.getElementById("filter-century");
  if (century && century.options.length > 1) {
    const prev = century.value;
    century.value = century.options[1].value;
    century.dispatchEvent(new Event("change", { bubbles: true }));
    await sleep(150);
    const resetVis = !document.getElementById("btn-reset-filters")?.hidden;
    note("filter-century", century.value !== "all");
    if (resetVis) {
      clickId("btn-reset-filters");
      await sleep(150);
      note("btn-reset-filters", century.value === "all" || century.value === prev);
    } else note("btn-reset-filters", false, "skjult");
  }

  const evCard = document.querySelector("#timeline-list .event-card");
  if (evCard) {
    evCard.click();
    await sleep(150);
    note("timeline-event-card", !!document.querySelector("#detail-panel h3"));
  }

  const yearMin = document.getElementById("year-min");
  const yearMax = document.getElementById("year-max");
  if (yearMin && yearMax) {
    yearMin.value = "1900";
    yearMax.value = "1901";
    yearMin.dispatchEvent(new Event("change", { bubbles: true }));
    await sleep(200);
    const timelineReset = document.querySelector("[data-action='reset-filters']");
    if (timelineReset) {
      timelineReset.click();
      await sleep(200);
      note(
        "timeline-reset-filters",
        yearMin.value !== "1900" || yearMax.value === "1924",
        `${yearMin.value}-${yearMax.value}`,
      );
    } else {
      note("timeline-reset-filters", false, "knapp ikke vist");
    }
  }

  const findCard = document.querySelector("#timeline-list .event-card-find");
  if (findCard) {
    findCard.click();
    await sleep(150);
    note("timeline-find-card", !!document.querySelector("#detail-panel h3"));
  } else {
    note("timeline-find-card", true, "ingen funn synlig med filter (OK)");
  }

  const layer = document.getElementById("map-layer");
  if (layer && layer.options.length > 1) {
    const before = layer.value;
    layer.value = layer.options[1].value;
    layer.dispatchEvent(new Event("change", { bubbles: true }));
    await sleep(100);
    note("map-layer-select", layer.value !== before, layer.value);
  }

  const boundIds = [
    "mode-tab-explore",
    "mode-tab-routes",
    "walk-prev",
    "walk-next",
    "walk-exit",
    "btn-map-locate",
    "btn-reset-filters",
  ];
  boundIds.forEach((id) => note(`dom-${id}`, !!document.getElementById(id)));

  const pass = results.every((r) => r.ok);
  return { pass, results };

  function filtersActiveCountSafe() {
    const cen = document.getElementById("filter-century")?.value;
    return cen === "all";
  }
})();