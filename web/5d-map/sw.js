// 5D-Map Service Worker - Progressive Web App
// Version: 1.0.0
// Purpose: Offline caching, faster load times, PWA functionality

const CACHE_VERSION = 'v1.0.0';
const CACHE_NAME = `5d-map-${CACHE_VERSION}`;

// Assets to cache immediately on install
const STATIC_ASSETS = [
  './',
  './index.html',
  './css/styles.css',
  './js/5d-map.js',
  './js/data-loader.js',
  './js/heatmap-layer.js',
  './js/imp-choropleth.js',
  './js/school-markers.js',
  './js/time-travel.js',
  './data/baseline.json',
  './data/country-boundaries.geojson',
  // Leaflet CDN files
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js',
  // Chart.js for radar charts
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js'
];

// API endpoints to cache (with network-first strategy)
const API_ENDPOINTS = [
  'https://ourworldindata.org/grapher/',
  'https://api.worldbank.org/v2/',
  '../../../5d_solutions.json',
  '../../../5d_research_data.json',
  '../../../5d_github_data.json'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing version', CACHE_VERSION);
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching static assets');
        return cache.addAll(STATIC_ASSETS.map(url => new Request(url, { mode: 'no-cors' })))
          .catch((error) => {
            console.error('[Service Worker] Failed to cache some assets:', error);
            // Continue even if some assets fail
          });
      })
      .then(() => self.skipWaiting()) // Activate immediately
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating version', CACHE_VERSION);
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name.startsWith('5d-map-') && name !== CACHE_NAME)
            .map((name) => {
              console.log('[Service Worker] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => self.clients.claim()) // Take control immediately
  );
});

// Fetch event - serve from cache with fallback strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip chrome-extension and other non-http(s) requests
  if (!url.protocol.startsWith('http')) {
    return;
  }
  
  // Strategy 1: Network-first for API endpoints (fresh data priority)
  if (isAPIEndpoint(url.href)) {
    event.respondWith(networkFirstStrategy(request));
    return;
  }
  
  // Strategy 2: Cache-first for static assets (speed priority)
  if (isStaticAsset(url.href)) {
    event.respondWith(cacheFirstStrategy(request));
    return;
  }
  
  // Strategy 3: Stale-while-revalidate for external CDNs
  if (isExternalCDN(url.href)) {
    event.respondWith(staleWhileRevalidateStrategy(request));
    return;
  }
  
  // Default: Network-first with cache fallback
  event.respondWith(networkFirstStrategy(request));
});

// Helper: Check if URL is an API endpoint
function isAPIEndpoint(url) {
  return API_ENDPOINTS.some(endpoint => url.includes(endpoint));
}

// Helper: Check if URL is a static asset
function isStaticAsset(url) {
  return url.match(/\.(css|js|json|html|png|jpg|svg|woff2?)$/i);
}

// Helper: Check if URL is an external CDN
function isExternalCDN(url) {
  try {
    const parsed = new URL(url, self.location.origin); // Support relative URLs
    const hostname = parsed.hostname;
    return (
      hostname === 'unpkg.com' || hostname.endsWith('.unpkg.com') ||
      hostname === 'cdn.jsdelivr.net' || hostname.endsWith('.cdn.jsdelivr.net') ||
      hostname === 'cdnjs.cloudflare.com' || hostname.endsWith('.cdnjs.cloudflare.com')
    );
  } catch (e) {
    // If url cannot be parsed, treat as not external CDN
    return false;
  }
}

// Strategy 1: Network-first (try network, fallback to cache)
async function networkFirstStrategy(request) {
  const cache = await caches.open(CACHE_NAME);
  
  try {
    const networkResponse = await fetch(request, { mode: 'cors' });
    
    // Cache successful responses (excluding 404, 500, etc.)
    if (networkResponse && networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[Service Worker] Network failed, serving from cache:', request.url);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page or error response
    return new Response('Offline - data not available in cache', {
      status: 503,
      statusText: 'Service Unavailable',
      headers: { 'Content-Type': 'text/plain' }
    });
  }
}

// Strategy 2: Cache-first (try cache, fallback to network)
async function cacheFirstStrategy(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  if (cachedResponse) {
    console.log('[Service Worker] Serving from cache:', request.url);
    return cachedResponse;
  }
  
  console.log('[Service Worker] Cache miss, fetching:', request.url);
  
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse && networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('[Service Worker] Fetch failed:', error);
    return new Response('Offline', { status: 503 });
  }
}

// Strategy 3: Stale-while-revalidate (serve cache, update in background)
async function staleWhileRevalidateStrategy(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  // Fetch in background to update cache
  const fetchPromise = fetch(request).then((networkResponse) => {
    if (networkResponse && networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  });
  
  // Return cached version immediately (if available)
  return cachedResponse || fetchPromise;
}

// Message event - manual cache refresh
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.delete(CACHE_NAME).then(() => {
        console.log('[Service Worker] Cache cleared');
      })
    );
  }
});

// Background sync for failed requests (future enhancement)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-analytics') {
    event.waitUntil(syncAnalytics());
  }
});

async function syncAnalytics() {
  // Future: Sync analytics when back online
  console.log('[Service Worker] Background sync triggered');
}

// Push notifications (future enhancement)
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'New 5D data available',
    icon: './favicon.ico',
    badge: './favicon.ico'
  };
  
  event.waitUntil(
    self.registration.showNotification('5D Intelligence Map', options)
  );
});
