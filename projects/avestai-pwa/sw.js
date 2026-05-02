/**
 * AvestAI PWA - Service Worker
 * Handles offline support and caching
 */

const CACHE_NAME = 'avestai-v1';
const ASSETS = [
    '/',
    '/index.html',
    '/app.js',
    '/styles.css',
    '/manifest.json'
];

// Install event
self.addEventListener('install', (event) => {
    console.log('[SW] Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[SW] Caching assets');
            return cache.addAll(ASSETS);
        })
    );
    self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event
self.addEventListener('fetch', (event) => {
    const { request } = event;
    
    // Skip WebSocket and non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    event.respondWith(
        caches.match(request).then((response) => {
            if (response) {
                return response;
            }
            
            return fetch(request).then((response) => {
                // Don't cache non-200 responses
                if (!response || response.status !== 200 || response.type === 'error') {
                    return response;
                }
                
                // Clone and cache the response
                const responseToCache = response.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(request, responseToCache);
                });
                
                return response;
            }).catch(() => {
                // Return cached version if offline
                return caches.match(request);
            });
        })
    );
});
