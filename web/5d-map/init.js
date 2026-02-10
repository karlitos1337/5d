// Core Web Vitals tracking
import {onCLS, onFID, onLCP, onFCP, onTTFB} from 'https://unpkg.com/web-vitals@3/dist/web-vitals.js?module';

function sendToAnalytics({name, value, rating}) {
  console.log(`[Web Vitals] ${name}: ${value.toFixed(2)}ms (${rating})`);

  // Optional: Send to analytics service
  // fetch('/analytics', {
  //   method: 'POST',
  //   body: JSON.stringify({metric: name, value, rating})
  // });
}

onCLS(sendToAnalytics);  // Cumulative Layout Shift
onFID(sendToAnalytics);  // First Input Delay
onLCP(sendToAnalytics);  // Largest Contentful Paint
onFCP(sendToAnalytics);  // First Contentful Paint
onTTFB(sendToAnalytics); // Time to First Byte

// Register service worker for PWA functionality
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js')
      .then((registration) => {
        console.log('✓ Service Worker registered:', registration.scope);

        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          console.log('Service Worker update found');

          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New version available, show update notification
              if (confirm('Neue Version verfügbar! Seite neu laden?')) {
                newWorker.postMessage({ type: 'SKIP_WAITING' });
                window.location.reload();
              }
            }
          });
        });
      })
      .catch((error) => {
        console.warn('Service Worker registration failed:', error);
      });
  });

  // Listen for controller change (new service worker activated)
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    console.log('Service Worker updated, reloading...');
    window.location.reload();
  });
}

// PWA install prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;

  // Show custom install button (optional)
  const installBtn = document.getElementById('install-btn');
  if (installBtn) {
    installBtn.style.display = 'block';
    installBtn.addEventListener('click', () => {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then((choice) => {
        console.log('PWA install choice:', choice.outcome);
        deferredPrompt = null;
        installBtn.style.display = 'none';
      });
    });
  }
});

// Track PWA installation
window.addEventListener('appinstalled', () => {
  console.log('✓ PWA installed successfully');
  deferredPrompt = null;
});
