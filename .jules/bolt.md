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

## 2026-03-01 - Prevent localStorage race conditions when using Promise.all
**Learning:** When refactoring sequential `await fetchWithCache()` calls to run concurrently via `Promise.all()`, you can inadvertently introduce race conditions if the cache function reads the state *once* before the fetch. Multiple concurrent fetches will read the exact same cache state, complete at slightly different times, and then overwrite each other's results when saving back to `localStorage`.
**Action:** When parallelizing cache-dependent operations, ensure you re-read the cache state *immediately* before writing the updated entry (e.g., `const freshCache = loadCache(); freshCache[key] = data; saveCache(freshCache);`) to prevent lost writes.
