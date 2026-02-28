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

## 2025-02-28 - Pytest Local Module Resolution
**Learning:** Running `pytest` directly in certain environments (like the CI or locally without specific venvs) may fail to resolve top-level packages (e.g., `storage`, `models`), resulting in `ModuleNotFoundError`.
**Action:** Always verify local tests with `PYTHONPATH=. python3 -m pytest` or ensure an `__init__.py` in the root of missing packages and a `tests/conftest.py` that modifies `sys.path`.
