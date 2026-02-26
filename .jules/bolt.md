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

## 2026-02-26 - race-condition-localstorage-parallel-fetch
**Learning:** `localStorage` is synchronous, but `await fetch()` releases the thread. If you implement a cache with `read -> await -> write`, you create a race condition when multiple async functions run in parallel. Updates made by other functions during the `await` are lost because the final write overwrites the state with the stale copy read at the beginning.
**Action:** Always re-read `localStorage` (or any shared mutable state) immediately before writing in an async function to ensure you are modifying the latest state. For simple key-value caches, this optimistic locking strategy (read-modify-write in critical section) is sufficient and performant.
