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
