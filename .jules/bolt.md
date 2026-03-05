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

## 2024-05-23 - React Scroll Event Throttling
**Learning:** Attaching standard synchronous event listeners to window `scroll` events in React components forces recalculations (like `offsetTop`) directly on the main thread continuously, causing severe layout thrashing (scroll jank).
**Action:** Always throttle continuous `scroll` events using `window.requestAnimationFrame()` coupled with a boolean tracking flag (a "ticking lock"). Furthermore, append `{ passive: true }` to the event listener options to explicitly tell the browser that the default scrolling mechanism won't be prevented, unlocking significantly smoother browser-level scrolling performance.
