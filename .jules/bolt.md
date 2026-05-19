## 2025-02-20 - Cache DOM Elements Outside React Event Handlers
**Learning:** In Vite/React dashboards like `web/validation_dashboard/src/App.jsx`, querying DOM elements (e.g., `document.getElementById`) repeatedly inside high-frequency event handlers like `window.addEventListener('scroll')` causes unnecessary main-thread blocking and re-evaluations on every scroll event.
**Action:** When optimizing React scroll event listeners, map and cache necessary DOM elements once outside the scroll handler (such as in a `useEffect` closure) to prevent layout thrashing and main-thread blocking.

