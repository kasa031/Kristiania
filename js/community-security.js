/**
 * Klient-sikkerhet for brukerbidrag (lokalt i nettleseren).
 * Ikke erstatning for server-moderering når innhold deles offentlig.
 */
(function () {
  const SUBMIT_LOG_KEY = "kristiania-community-submit-log";
  const MAX_PINS_STORED = 500;
  const MAX_SUBMITS_PER_HOUR = 8;
  const MAX_SUBMITS_PER_DAY = 25;
  const OSLO_LAT_MIN = 59.78;
  const OSLO_LAT_MAX = 60.05;
  const OSLO_LNG_MIN = 10.55;
  const OSLO_LNG_MAX = 11.05;

  /** Vedlikeholdes - utvid med backend-liste senere (T14). */
  const BLOCKED_PATTERN_SOURCES = [
    String.raw`\bfitt[eæ]\b`,
    String.raw`\bfaen\b`,
    String.raw`\bjævla\b`,
    String.raw`\bhelvetes\b`,
    String.raw`\bforbanna?d\b`,
    String.raw`\bsatan\b`,
    String.raw`\b(jæv|drit)[ -]?[aæ]ss\b`,
    String.raw`<\s*(script|iframe|object|embed|svg|math)\b`,
    String.raw`javascript\s*:`,
    String.raw`on\w+\s*=`,
  ];

  const blockedPatterns = BLOCKED_PATTERN_SOURCES.map(
    (src) => new RegExp(src, "i"),
  );

  function stripDangerousMarkup(text) {
    return String(text || "")
      .replace(/<[^>]*>/g, "")
      .replace(/\u0000/g, "")
      .trim();
  }

  function containsBlockedContent(text) {
    const normalized = stripDangerousMarkup(text);
    return blockedPatterns.some((re) => re.test(normalized));
  }

  function readSubmitLog() {
    try {
      const raw = localStorage.getItem(SUBMIT_LOG_KEY);
      const list = raw ? JSON.parse(raw) : [];
      return Array.isArray(list) ? list.filter((t) => typeof t === "number") : [];
    } catch {
      return [];
    }
  }

  function pruneSubmitLog(now = Date.now()) {
    const dayAgo = now - 24 * 60 * 60 * 1000;
    const kept = readSubmitLog().filter((t) => t >= dayAgo);
    localStorage.setItem(SUBMIT_LOG_KEY, JSON.stringify(kept));
    return kept;
  }

  function checkSubmitRateLimit() {
    const now = Date.now();
    const log = pruneSubmitLog(now);
    const hourAgo = now - 60 * 60 * 1000;
    const inHour = log.filter((t) => t >= hourAgo).length;
    const inDay = log.length;
    if (inHour >= MAX_SUBMITS_PER_HOUR) {
      return {
        ok: false,
        message: "Du har lagt til mange steder kort tid. Vent litt før du legger inn flere.",
      };
    }
    if (inDay >= MAX_SUBMITS_PER_DAY) {
      return {
        ok: false,
        message: "Daglig grense for nye innlegg er nådd. Prøv igjen i morgen.",
      };
    }
    return { ok: true };
  }

  function recordSubmit() {
    const now = Date.now();
    const log = pruneSubmitLog(now);
    log.push(now);
    localStorage.setItem(SUBMIT_LOG_KEY, JSON.stringify(log));
  }

  function isOsloArea(lat, lng) {
    return (
      Number.isFinite(lat) &&
      Number.isFinite(lng) &&
      lat >= OSLO_LAT_MIN &&
      lat <= OSLO_LAT_MAX &&
      lng >= OSLO_LNG_MIN &&
      lng <= OSLO_LNG_MAX
    );
  }

  function validateCommunityFields(fields) {
    const title = stripDangerousMarkup(fields.title);
    const story = stripDangerousMarkup(fields.story);
    const address = stripDangerousMarkup(fields.address);
    const alias = stripDangerousMarkup(fields.alias);

    if (!title || title.length < 2) {
      return { ok: false, message: "Tittelen må ha minst 2 tegn." };
    }
    if (!story || story.length < 10) {
      return { ok: false, message: "Historien må ha minst 10 tegn." };
    }
    if (title.length > 120 || story.length > 2000 || address.length > 200 || alias.length > 40) {
      return { ok: false, message: "Teksten er for lang for skjemaet." };
    }
    const combined = `${title}\n${story}\n${address}\n${alias}`;
    if (containsBlockedContent(combined)) {
      return {
        ok: false,
        message: "Innholdet kan ikke godkjennes. Fjern grovt språk, scripting eller koder i teksten.",
      };
    }
    if (!isOsloArea(fields.lat, fields.lng)) {
      return {
        ok: false,
        message: "Stedet må ligge innenfor Oslo-området på kartet.",
      };
    }
    return {
      ok: true,
      cleaned: { title, story, address, alias },
    };
  }

  function sanitizeStoredPin(pin) {
    if (!pin || typeof pin !== "object") return null;
    const lat = parseFloat(pin.lat);
    const lng = parseFloat(pin.lng);
    if (!isOsloArea(lat, lng)) return null;
    const title = stripDangerousMarkup(pin.title).slice(0, 120);
    const story = stripDangerousMarkup(pin.story).slice(0, 2000);
    if (!title || !story) return null;
    if (containsBlockedContent(`${title}\n${story}`)) return null;
    const id = typeof pin.id === "string" && pin.id.startsWith("community-") ? pin.id : null;
    if (!id) return null;
    return {
      id,
      title,
      story,
      address: stripDangerousMarkup(pin.address).slice(0, 200),
      lat,
      lng,
      hashtags: Array.isArray(pin.hashtags)
        ? pin.hashtags
            .filter((h) => typeof h === "string")
            .map((h) => stripDangerousMarkup(h).slice(0, 40))
            .filter(Boolean)
            .slice(0, 12)
        : [],
      authorAlias: stripDangerousMarkup(pin.authorAlias).slice(0, 40) || undefined,
      createdAt: typeof pin.createdAt === "string" ? pin.createdAt : undefined,
    };
  }

  function sanitizePinList(list) {
    if (!Array.isArray(list)) return [];
    return list
      .map(sanitizeStoredPin)
      .filter(Boolean)
      .slice(-MAX_PINS_STORED);
  }

  window.KristianiaCommunitySecurity = {
    checkSubmitRateLimit,
    recordSubmit,
    validateCommunityFields,
    sanitizePinList,
    stripDangerousMarkup,
    containsBlockedContent,
    MAX_PINS_STORED,
  };
})();