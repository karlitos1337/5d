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

## 2025-03-04 - Promise.all and Synchronous Stores
**Learning:** Concurrent async executions (e.g., using `Promise.all` for fetch requests) that modify a shared synchronous store like `localStorage` can cause race conditions. If you read the cache state before awaiting a fetch, and then save the cache after the fetch, you might overwrite changes made by other parallel fetches that completed in the meantime.
**Action:** Always re-read the cache from `localStorage` immediately prior to writing back to it within the async function.
