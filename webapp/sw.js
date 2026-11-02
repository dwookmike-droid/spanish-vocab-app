/* Offline support: the app shell and data are cached on install; images and audio are cached the first time
   they are used. Bump VERSION whenever app.js / app.css / data change so phones pick up the new files. */
const VERSION = "vv-3";
const SHELL = ["./", "index.html", "app.js", "app.css", "data/bundle.js", "manifest.webmanifest", "icons/icon-192.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  const isMedia = url.pathname.includes("/media/");
  e.respondWith(caches.open(VERSION).then(async (cache) => {
    const hit = await cache.match(e.request, { ignoreSearch: true });
    if (hit && isMedia) return hit; // media never changes for the same name
    const net = fetch(e.request).then((res) => {
      if (res.ok && res.status === 200) cache.put(e.request, res.clone());
      return res;
    }).catch(() => hit || Response.error());
    return hit || net; // shell: serve cached copy, refresh it in the background
  }));
});
