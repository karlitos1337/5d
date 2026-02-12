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

## 2024-05-24 - Parallel Fetching & Cache Race Conditions
**Learning:** When parallelizing API fetches that share a monolithic storage (like a single localStorage key), race conditions occur where parallel updates overwrite each other.
**Action:** When using `Promise.all` for parallel fetching with a shared cache, ensure the cache read-update-write cycle is atomic or re-read the cache state immediately before writing. Ideally, use granular cache keys to avoid shared state contention.
