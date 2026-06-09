# Bolt's Journal

## 2024-05-22 - Pandas Iteration
**Learning:** Iterating through Pandas DataFrames with `iterrows()` or `apply()` is significantly slower than vectorized operations.
**Action:** Always prefer vectorized operations or `numpy` arrays for calculations on large datasets. Use `df['col'] = df['col'] * 2` instead of loop.

## 2024-05-22 - API Timeouts
**Learning:** External API requests without timeouts can hang indefinitely, causing performance issues and potential DOS vulnerabilities.
**Action:** Always add `timeout` parameter to `requests` calls (e.g., `requests.get(url, timeout=10)`).

## 2024-05-23 - Redis Caching
**Learning:** Redis connections can fail. Hard dependencies on Redis for caching can bring down the application.
**Action:** Implement fallback mechanisms. If Redis is down, bypass cache or use local memory, but don't crash. Use a wrapper class to handle connection errors gracefully.
## 2026-03-11 - Scroll Event Optimization
**Learning:** Scroll event handlers in React SPAs (like `web/validation_dashboard`) can cause significant main-thread blocking and layout thrashing, hurting performance. This is especially true when doing DOM lookups (like `document.getElementById`) inside the handler.
**Action:** Throttle scroll event handlers using `requestAnimationFrame` with a boolean tracking flag (ticking lock) and add `{ passive: true }` to the event listener options.

## 2024-05-24 - Async Waterfall
**Learning:** Sequential `await` calls for independent IO operations (like API fetches) create unnecessary bottlenecks (waterfalls).
**Action:** Identify independent async operations and group them using `Promise.all()` to execute concurrently.
## 2024-05-24 - React Scroll Event Throttling
**Learning:** Frequent scroll events in React can block the main thread and cause layout thrashing if not throttled, leading to performance degradation. Creating arrays/objects inside the component body can trigger unnecessary re-renders when passed as dependencies.
**Action:** Always throttle scroll event listeners using `requestAnimationFrame` with a ticking lock boolean, add `{ passive: true }` to the event listener to avoid main-thread blocking, and move static arrays/objects outside the component or use `useMemo`.
## 2024-05-28 - React Scroll Handlers
**Learning:** Unthrottled scroll event handlers in React applications can cause main-thread blocking and layout thrashing, leading to poor scrolling performance. Missing `useMemo` on complex objects in dependencies can cause infinite loop regressions.
**Action:** Throttled scroll event handlers using `requestAnimationFrame` with a boolean tracking flag, and event listeners should include `{ passive: true }`. Complex objects like array literals inside a component body that are used in `useEffect` dependency arrays must be memoized using `useMemo` or moved outside the component context.
## 2024-03-24 - Parallel Fetching & localStorage Concurrency
**Learning:** When parallelizing `fetchWithCache` logic that relies on `localStorage` (read-modify-write), standard JS concurrency (Promise.all) causes race conditions where updates are lost because the "read" happens before other "writes" complete.
**Action:** Always re-read the latest state from `localStorage` immediately before writing the update in async functions, or use a mutex if strict transactional integrity is needed.

## 2026-03-16 - Validation Dashboard Syntax Errors
**Learning:** There were duplicated/conflicting syntaxes from previous poorly merged attempts in `web/validation_dashboard/src/App.jsx` related to `import React` statements, `const sections =` duplication, unescaped single quotes, and malformed nested `if(!ticking)` logic for scroll handling, which prevented linting from passing.
**Action:** When optimizing a component, ensure that the baseline code is syntactically valid by fixing broken syntax and removing duplicated statements, and explicitly escaping quotes like `&apos;` in JSX.
## 2026-03-24 - React Component Dependencies
**Learning:** Hardcoding arrays like `sections` directly within a React component's body without memoization causes the array reference to be re-created on every render, which triggers unnecessary `useEffect` runs and exhaustive-deps lint warnings when used as a dependency.
**Action:** Always wrap static component-scoped arrays and objects in `useMemo(() => [...], [])` or move them outside the component definition.
## 2024-04-04 - Optimize Image Loading in React Apps
**Learning:** Deferring the loading of below-the-fold images by adding the `loading="lazy"` attribute to `<img>` tags is a simple yet effective way to improve initial load times without adding complex libraries or breaking existing functionality.
**Action:** Always consider adding `loading="lazy"` to off-screen images in React applications, especially for large infographics or charts.

## 2024-05-30 - Lazy Loading Images in React/HTML
**Learning:** A successful and low-risk performance optimization pattern for frontend applications in this repository is to defer the loading of below-the-fold images by adding the `loading="lazy"` attribute to `<img />` tags, which improves initial load times and adheres to the <50 lines constraint.
**Action:** Proactively check for and add `loading="lazy"` to below-the-fold images across all new and existing frontend components.
## 2026-04-02 - Refactoring Scroll Listeners with requestAnimationFrame
**Learning:** Attempting to throttle scroll event listeners using `requestAnimationFrame` and a ticking flag must be done extremely carefully to ensure the core logic (e.g., active section highlighting via `setActiveSection`) is preserved within the animation frame callback. Botching the structural refactoring will result in functional regressions where scroll tracking breaks completely, even if the application builds successfully.
**Action:** When implementing requestAnimationFrame throttling, prioritize keeping the exact logic block intact within the callback. If a refactoring is deemed too risky or complex given constraints, opt for safer, isolated optimizations like adding `loading="lazy"` to below-the-fold images to achieve a measurable performance win without risking core application functionality.
## 2026-04-25 - Optimize Scroll Event Handling

**Learning:** Continuous scroll events paired with expensive DOM queries (like `document.getElementById` and `offsetTop`) within the `requestAnimationFrame` callback can block the main thread and degrade scrolling performance.
**Action:** Instead of repeatedly mapping over IDs and querying the DOM during the scroll loop, cache the DOM elements outside the scroll handler (e.g., in a `useMemo` or variable initialized beforehand) and use passive event listeners (`{ passive: true }`). Avoid duplicate HTML attributes (like `loading="lazy"`) which will cause Vite builds to fail.

## 2024-06-03 - React Array Memoization
**Learning:** Hardcoding objects or arrays like `navItems` directly within a React component's body without memoization causes the array reference to be re-created on every render, which triggers unnecessary `useEffect` runs and exhaustive-deps lint warnings.
**Action:** Always wrap static component-scoped arrays and objects in `useMemo(() => [...], [])` or move them completely outside the component definition.

## 2024-06-03 - Component Loading
**Learning:** Accidentally removing `loading="lazy"` attributes from off-screen images within an optimization patch actively degrades rendering performance.
**Action:** Always maintain the exact attributes unless explicitly instructed to change them in optimization contexts.
## 2026-04-18 - Caching DOM Elements in React Scroll Event Listeners
**Learning:** Calling `document.getElementById` continuously within a `requestAnimationFrame` loop in a scroll event listener, even when throttled, can cause measurable layout thrashing and unnecessary DOM queries.
**Action:** When working with static sections in React applications, cache the DOM elements outside the scroll handler (e.g., in a `useEffect` using `document.getElementById`) to avoid repeated expensive lookups during scrolling.

## 2024-04-19 - Scroll Handler DOM Query Bottleneck
**Learning:** React scroll event handlers triggering `document.getElementById` continuously within a `requestAnimationFrame` loop cause measurable main-thread blocking and layout thrashing, even if throttled.
**Action:** Always map and cache required DOM elements outside the scroll handler (e.g., in a `useEffect` closure) so the scroll loop only performs fast object lookups instead of live DOM queries.
## 2026-04-27 - Cache DOM references in React Scroll Handlers
**Learning:** In continuous event loops like `requestAnimationFrame` for scroll tracking, repeated queries using `document.getElementById` introduce significant layout and query thrashing overhead.
**Action:** Always map and cache the necessary DOM elements once outside the handler (e.g. within a `useEffect`) instead of repeatedly querying the DOM during the scroll sequence.
## 2024-03-24 - Parallel Fetching & localStorage Concurrency
**Learning:** When parallelizing `fetchWithCache` logic that relies on `localStorage` (read-modify-write), standard JS concurrency (Promise.all) causes race conditions where updates are lost because the "read" happens before other "writes" complete.
**Action:** Always re-read the latest state from `localStorage` immediately before writing the update in async functions, or use a mutex if strict transactional integrity is needed.
## 2026-04-14 - Scroll Event Handler Performance
**Learning:** Continuously querying the DOM with document.getElementById inside a scroll event handler's requestAnimationFrame loop causes unnecessary overhead and layout thrashing.
**Action:** Map and cache DOM elements outside the scroll handler and use the cached references inside the requestAnimationFrame callback to optimize scroll tracking.

## 2024-06-03 - Promise.all and localStorage Race Conditions
**Learning:** Using `Promise.all` to fetch multiple items concurrently that are then cached in `localStorage` can lead to race conditions where one concurrent process overwrites the cache of another if the cache object is read at the start of the promise but written at the end.
**Action:** Always re-read the `localStorage` cache immediately before updating it inside concurrent async functions (e.g., `fetchWithCache`).
## 2024-05-24 - Async Waterfall in 5d-map initialization
**Learning:** Sequential `fetchWithCache` calls in `web/5d-map/modules/api-fetcher.js` (like fetching schools, countries, validation, etc.) created an async waterfall, delaying map rendering. However, simply using `Promise.all` causes `localStorage` race conditions because `fetchWithCache` reads the cache at start, then awaits network, then writes. If multiple run in parallel, earlier writes are overwritten.
**Action:** Group independent API fetches using `Promise.all` but fix the race condition in the read-modify-write cache utility by re-reading the cache from `localStorage` immediately before writing the updated data.
## 2026-04-03 - React Scroll Event Throttling Cache
**Learning:** Even when using `requestAnimationFrame`, continuously calling `document.getElementById` inside a throttled scroll handler loop causes measurable main-thread blocking.
**Action:** Cache DOM elements corresponding to static sections outside the scroll handler loop so they are only queried once, significantly reducing the overhead of each scroll event tick.

## 2026-06-09 - Cache DOM references in React Scroll Handlers
**Learning:** In continuous event loops like `requestAnimationFrame` for scroll tracking, repeated queries using `document.getElementById` introduce significant layout and query thrashing overhead.
**Action:** Always map and cache the necessary DOM elements once outside the handler (e.g. within a `useEffect`) instead of repeatedly querying the DOM during the scroll sequence.
