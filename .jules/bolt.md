## 2024-05-24 - React Scroll Event Throttling
**Learning:** Frequent scroll events in React can block the main thread and cause layout thrashing if not throttled, leading to performance degradation. Creating arrays/objects inside the component body can trigger unnecessary re-renders when passed as dependencies.
**Action:** Always throttle scroll event listeners using `requestAnimationFrame` with a ticking lock boolean, add `{ passive: true }` to the event listener to avoid main-thread blocking, and move static arrays/objects outside the component or use `useMemo`.
## 2026-05-08 - React Scroll Handlers Validation
**Learning:** Fixing React scroll handlers requires removing un-throttled duplicate syntax inside the `useEffect`.
**Action:** When fixing scroll handlers, always ensure the file syntax compiles successfully and doesn't introduce duplicate component arrays or hooks.
## 2024-06-15 - Throttling React Scroll Handlers Validation
**Learning:** Refactoring React scroll handlers to use requestAnimationFrame can result in build errors or duplicate logic if exact code substitutions are not strictly preserved and linted.
**Action:** When implementing requestAnimationFrame throttling, ensure no duplicate variables or functions are introduced and always verify by running a local build before submitting.
