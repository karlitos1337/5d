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

## 2026-03-07 - React Scroll Event Throttling
**Learning:** High-frequency scroll events in React components can cause significant layout thrashing and main-thread blocking, particularly when combined with DOM queries or state updates on every tick.
**Action:** Always throttle scroll handlers using `requestAnimationFrame` with a boolean tracking flag (ticking lock) to synchronize execution with the browser's repaint cycle, and use `{ passive: true }` for the event listener to prevent scrolling performance degradation.
