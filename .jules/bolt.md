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

## 2026-02-26 - linting-and-dependency-hygiene
**Learning:** CI failures are often caused by:
1.  Checking linting on vendor/backup directories (, ) because configuration files () lack explicit exclusions.
2.  Missing dependencies in  that are installed in the dev environment but not in CI (e.g.,  for tests).
3.  Invalid git submodules (directories with  inside them but no  entry) causing exit code 128.
**Action:** Always verify  exclusions match the project structure. Keep  in sync with imports. Use  for accidental submodules.

## 2026-02-26 - linting-and-dependency-hygiene
**Learning:** CI failures are often caused by:
1.  Checking linting on vendor/backup directories (`99_unsortiert`, `external`) because configuration files (`pyproject.toml`) lack explicit exclusions.
2.  Missing dependencies in `requirements.txt` that are installed in the dev environment but not in CI (e.g., `networkx` for tests).
3.  Invalid git submodules (directories with `.git` inside them but no `.gitmodules` entry) causing exit code 128.
**Action:** Always verify `pyproject.toml` exclusions match the project structure. Keep `requirements_extended.txt` in sync with imports. Use `git rm --cached` for accidental submodules.
