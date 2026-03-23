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
## 2024-05-28 - Optimize React Scroll Handlers
**Learning:** React scroll listeners should use `{ passive: true }` to avoid blocking the main thread, and `requestAnimationFrame` to throttle rapid scroll events. Failing to clean up scroll listeners or handle them natively in React without `useEffect` causes degraded performance, especially when checking offsets of multiple sections on the page.
**Action:** Always wrap `window.addEventListener('scroll', handler, { passive: true })` inside `useEffect` and throttle heavy DOM reads (like `offsetTop`) using `requestAnimationFrame` with a tracking boolean flag to prevent unnecessary recalculations.
