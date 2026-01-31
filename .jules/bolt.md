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

## 2024-05-24 - Decouple UI from Expensive Logic
**Learning:** Synchronous updates on high-frequency events (like 'input' on sliders) block the main thread and degrade perceived performance, even if the logic seems fast.
**Action:** Decouple the immediate UI feedback (e.g., label update) from the expensive operation (e.g., map rendering) using `debounce` or `requestAnimationFrame`.

## 2024-05-24 - CI Dependency and Linting
**Learning:** CI failures can occur due to missing dependencies in test environments (e.g., `networkx`, `pytest` itself) and strict linting rules (e.g., unused imports, deprecated type hints) in legacy or generated code.
**Action:** Ensure all test dependencies are explicitly listed in `requirements_extended.txt` or installed in the CI workflow. Exclude legacy/backup directories (like `99_unsortiert`) from linting/testing configurations if they are not meant to be maintained.

## 2024-05-24 - Missing dependencies
**Learning:** CI failures can occur due to missing dependencies in test environments (e.g., `networkx`, `pytest` itself) and strict linting rules (e.g., unused imports, deprecated type hints) in legacy or generated code.
**Action:** Ensure all test dependencies are explicitly listed in `requirements_extended.txt` or installed in the CI workflow. Exclude legacy/backup directories (like `99_unsortiert`) from linting/testing configurations if they are not meant to be maintained.
