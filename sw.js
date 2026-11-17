// Ghumakkad offline support: the page shell is kept so the app opens with no signal.
// Place data (guides, sights, stays, weather) is saved by the page itself as you browse.
const CACHE = "ghum-shell-v1";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png",
  "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js",
  "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => Promise.all(SHELL.map(u => c.add(u).catch(() => {})))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("ghum-shell") && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const shell = url.origin === location.origin || url.host === "cdnjs.cloudflare.com" || url.host.startsWith("fonts.");
  if (!shell) return;  // data APIs are cached by the page
  e.respondWith(fetch(req).then(res => {
    if (res.ok || res.type === "opaque") { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
    return res;
  }).catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || (req.mode === "navigate" ? caches.match("index.html") : undefined))));
});
