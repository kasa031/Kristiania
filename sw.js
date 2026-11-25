const CACHE = "oslo-historie-v106";
const PRECACHE = [
  "/",
  "/index.html",
  "/404.html",
  "/home",
  "/kart",
  "/tur",
  "/css/style.css",
  "/css/motion.css",
  "/css/theme-kristiania.css",
  "/js/motion.js",
  "/js/app.js",
  "/manifest.webmanifest",
  "/data/places.json",
  "/data/events.json",
  "/data/episodes.json",
  "/data/tags.json",
  "/data/eras.json",
  "/data/map-config.json",
  "/data/site-config.json",
  "/data/chronology.json",
  "/data/districts.json",
  "/data/finds.json",
  "/data/people.json",
  "/data/context.json",
  "/data/blue-signs.json",
  "/data/map-markers.json",
  "/data/bydeler.geojson",
  "/js/bydel.js",
  "/icons/mark.svg",
  "/icons/oslo-vaapen.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE).catch(() => undefined)),
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))),
    ),
  );
  self.clients.claim();
});

const NETWORK_FIRST_PATHS = new Set([
  "/",
  "/index.html",
  "/js/app.js",
  "/js/motion.js",
  "/js/bydel.js",
  "/css/style.css",
  "/css/motion.css",
  "/css/theme-kristiania.css",
  "/data/site-config.json",
  "/manifest.webmanifest",
]);

function pathKey(pathname) {
  return pathname === "" ? "/" : pathname;
}

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  if (event.request.method !== "GET") return;
  const key = pathKey(url.pathname);
  const networkFirst = NETWORK_FIRST_PATHS.has(key);

  event.respondWith(
    caches.match(event.request).then((cached) => {
      const updateCache = (res) => {
        if (!res.ok) return;
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(event.request, copy));
      };
      if (networkFirst) {
        return fetch(event.request)
          .then((res) => {
            updateCache(res);
            return res;
          })
          .catch(() => cached || Response.error());
      }
      const fetchPromise = fetch(event.request)
        .then((res) => {
          if (res.ok && url.pathname.startsWith("/data/")) {
            updateCache(res);
          }
          return res;
        })
        .catch(() => cached);
      return cached || fetchPromise;
    }),
  );
});