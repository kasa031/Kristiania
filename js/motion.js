/**
 * Kristiania - lette UI-animasjoner uten tung bundler.
 * Valgfri Motion One (ESM) for avanserte sekvenser senere.
 */
(function () {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  function motionAllowed() {
    return !reduced.matches && stateMotionEnabled();
  }

  function stateMotionEnabled() {
    const cfg = window.__KRISTIANIA_SITE__;
    if (cfg && cfg.motion_enabled === false) return false;
    return true;
  }

  let revealTimer;

  function reveal(el, { stagger } = {}) {
    if (!el || !motionAllowed()) return;
    el.classList.remove("ui-reveal");
    if (stagger) el.classList.remove("ui-stagger-reveal");
    void el.offsetWidth;
    el.classList.add("ui-reveal");
    if (stagger) el.classList.add("ui-stagger-reveal");
  }

  function watchPanel(id, options) {
    const el = document.getElementById(id);
    if (!el) return;
    new MutationObserver(() => {
      clearTimeout(revealTimer);
      revealTimer = setTimeout(() => reveal(el, options), 25);
    }).observe(el, { childList: true });
  }

  function markAppReady() {
    document.body.classList.add("app-ready");
  }

  async function tryMotionOneStagger(selector) {
    if (!motionAllowed()) return;
    const nodes = document.querySelectorAll(selector);
    if (!nodes.length) return;
    try {
      const { animate, stagger } = await import(
        "https://cdn.jsdelivr.net/npm/motion@11.13.5/+esm"
      );
      animate(
        nodes,
        { opacity: [0, 1], transform: ["translateY(8px)", "translateY(0)"] },
        { delay: stagger(0.04), duration: 0.35, easing: "cubic-bezier(0.22, 1, 0.36, 1)" },
      );
    } catch (_) {
      /* CSS-stagger fallback i motion.css */
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    watchPanel("detail-panel", {});
    watchPanel("timeline-list", { stagger: true });
    markAppReady();
  });

  window.addEventListener("load", () => {
    if (!document.body.classList.contains("app-ready")) markAppReady();
  });

  window.KristianiaMotion = {
    reveal,
    pulseActiveMarker(marker) {
      if (!marker || !motionAllowed()) return;
      const el = marker.getElement?.();
      if (el) el.classList.add("kristiania-marker-pulse");
    },
    clearMarkerPulse(marker) {
      const el = marker?.getElement?.();
      if (el) el.classList.remove("kristiania-marker-pulse");
    },
    tryMotionOneStagger,
  };
})();