/**
 * Klient-sikkerhet for brukerbidrag (lokalt i nettleseren).
 * Ikke erstatning for server-moderering når innhold deles offentlig.
 */
(function () {
  const SUBMIT_LOG_KEY = "kristiania-community-submit-log";
  const MAX_PINS_STORED = 500;
  const MAX_SUBMITS_PER_HOUR = 8;
  const MAX_SUBMITS_PER_DAY = 25;
  const MAX_EXPORT_BYTES = 2 * 1024 * 1024;
  const OSLO_LAT_MIN = 59.78;
  const OSLO_LAT_MAX = 60.05;
  const OSLO_LNG_MIN = 10.55;
  const OSLO_LNG_MAX = 11.05;

  const ALLOWED_IMAGE_HOST_SUFFIXES = ["upload.wikimedia.org", "commons.wikimedia.org"];

  /** Vedlikeholdes - utvid med backend-liste senere (T14). */
  const BLOCKED_PATTERN_SOURCES = [
    String.raw`\bfitt[eæ]\b`,
    String.raw`\bfaen\b`,
    String.raw`\bfaenskap\b`,
    String.raw`\bjævla\b`,
    String.raw`\bhelvetes\b`,
    String.raw`\bforbanna?d\b`,
    String.raw`\bsatan\b`,
    String.raw`\b(jæv|drit)[ -]?[aæ]ss\b`,
    String.raw`\b(kuk|pikk)\b`,
    String.raw`<\s*(script|iframe|object|embed|svg|math|link|meta|style)\b`,
    String.raw`javascript\s*:`,
    String.raw`vbscript\s*:`,
    String.raw`data\s*:\s*text\/html`,
    String.raw`on\w+\s*=`,
  ];

  const SENSITIVE_PATTERN_SOURCES = [
    String.raw`\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b`,
    String.raw`\b(?:\+47|0047)[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}\b`,
    String.raw`\b\d{8}\b`,
    String.raw`\b\d{5,}\b`,
  ];

  const blockedPatterns = BLOCKED_PATTERN_SOURCES.map((src) => new RegExp(src, "i"));
  const sensitivePatterns = SENSITIVE_PATTERN_SOURCES.map((src) => new RegExp(src, "i"));

  function normalizeTextForScan(text) {
    return String(text || "")
      .normalize("NFKC")
      .replace(/[\u200B-\u200D\uFEFF]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function stripDangerousMarkup(text) {
    return normalizeTextForScan(String(text || "").replace(/<[^>]*>/g, "").replace(/\u0000/g, ""));
  }

  function containsBlockedContent(text) {
    const normalized = stripDangerousMarkup(text);
    return blockedPatterns.some((re) => re.test(normalized));
  }

  function containsSensitivePersonalData(text) {
    const normalized = normalizeTextForScan(stripDangerousMarkup(text));
    if (!normalized) return false;
    return sensitivePatterns.some((re) => re.test(normalized));
  }

  function safeHttpUrl(url) {
    if (!url || typeof url !== "string") return null;
    const trimmed = url.trim();
    if (!trimmed || /[\x00-\x1f\x7f]/.test(trimmed)) return null;
    try {
      const u = new URL(trimmed, "https://example.invalid/");
      if (u.protocol !== "https:" && u.protocol !== "http:") return null;
      if (u.username || u.password) return null;
      return u.href;
    } catch {
      return null;
    }
  }

  function safeImageUrl(url) {
    const href = safeHttpUrl(url);
    if (!href) return null;
    try {
      const u = new URL(href);
      if (u.protocol !== "https:") return null;
      const host = u.hostname.toLowerCase();
      const ok = ALLOWED_IMAGE_HOST_SUFFIXES.some(
        (suffix) => host === suffix || host.endsWith(`.${suffix}`),
      );
      return ok ? u.href : null;
    } catch {
      return null;
    }
  }

  function sanitizeHashtagList(raw) {
    const tags = new Set();
    for (const part of String(raw || "").split(/[\s,]+/)) {
      let t = part.trim().replace(/^#+/, "").toLowerCase();
      t = stripDangerousMarkup(t);
      if (!t || t.length > 32) continue;
      if (!/^[a-z0-9æøå_-]+$/.test(t)) continue;
      if (containsBlockedContent(t)) continue;
      tags.add(`#${t}`);
      if (tags.size >= 12) break;
    }
    return [...tags];
  }

  function createCommunityPinId() {
    if (typeof crypto !== "undefined" && crypto.randomUUID) {
      return `community-${crypto.randomUUID()}`;
    }
    return `community-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
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
    if (containsSensitivePersonalData(`${address}\n${story}\n${alias}`)) {
      return {
        ok: false,
        message:
          "Ikke legg inn e-post, telefon, lange tallrekker eller andre personopplysninger. Bruk nick uten kontaktinfo.",
      };
    }
    if (alias && containsSensitivePersonalData(alias)) {
      return {
        ok: false,
        message: "Kallenavn skal ikke inneholde e-post eller telefon.",
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

  function parseCommunityPinsJson(raw) {
    if (raw == null) return [];
    if (typeof raw !== "string") return [];
    if (raw.length > MAX_EXPORT_BYTES) return [];
    try {
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return [];
      return parsed;
    } catch {
      return null;
    }
  }

  function sanitizeStoredPin(pin) {
    if (!pin || typeof pin !== "object" || Array.isArray(pin)) return null;
    if (Object.prototype.hasOwnProperty.call(pin, "__proto__")) return null;
    const lat = parseFloat(pin.lat);
    const lng = parseFloat(pin.lng);
    if (!isOsloArea(lat, lng)) return null;
    const title = stripDangerousMarkup(pin.title).slice(0, 120);
    const story = stripDangerousMarkup(pin.story).slice(0, 2000);
    if (!title || !story) return null;
    if (containsBlockedContent(`${title}\n${story}`)) return null;
    if (containsSensitivePersonalData(`${pin.address || ""}\n${story}\n${pin.authorAlias || ""}`)) {
      return null;
    }
    const id = typeof pin.id === "string" && pin.id.startsWith("community-") ? pin.id.slice(0, 80) : null;
    if (!id || !/^community-[a-zA-Z0-9-]+$/.test(id)) return null;
    return {
      id,
      title,
      story,
      address: stripDangerousMarkup(pin.address).slice(0, 200),
      lat,
      lng,
      hashtags: Array.isArray(pin.hashtags)
        ? pin.hashtags
            .map((h) => (typeof h === "string" ? stripDangerousMarkup(h).slice(0, 40) : ""))
            .filter((h) => h && /^#[a-z0-9æøå_-]+$/.test(h))
            .slice(0, 12)
        : [],
      authorAlias: stripDangerousMarkup(pin.authorAlias).slice(0, 40) || undefined,
      createdAt:
        typeof pin.createdAt === "string" && pin.createdAt.length <= 40 ? pin.createdAt : undefined,
    };
  }

  function sanitizePinList(list) {
    if (!Array.isArray(list)) return [];
    return list
      .map(sanitizeStoredPin)
      .filter(Boolean)
      .slice(-MAX_PINS_STORED);
  }

  function assertExportSizeOk(jsonText) {
    const bytes = new TextEncoder().encode(String(jsonText || "")).length;
    return bytes <= MAX_EXPORT_BYTES;
  }

  window.KristianiaCommunitySecurity = {
    checkSubmitRateLimit,
    recordSubmit,
    validateCommunityFields,
    parseCommunityPinsJson,
    sanitizePinList,
    sanitizeHashtagList,
    stripDangerousMarkup,
    containsBlockedContent,
    containsSensitivePersonalData,
    safeHttpUrl,
    safeImageUrl,
    createCommunityPinId,
    assertExportSizeOk,
    MAX_PINS_STORED,
    MAX_EXPORT_BYTES,
  };
})();