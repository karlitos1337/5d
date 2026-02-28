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

## 2026-02-28 - CSV Parsing String Allocation Bottleneck
**Learning:** In the `api-fetcher.js` module for the 5D map, the `splitCSVLine` function previously built fields by concatenating characters one by one (`cur += ch`). This creates a massive number of intermediate, short-lived strings in JavaScript engines like V8, triggering frequent garbage collection during large CSV loads. Similarly, `parseCSV` used `.split().filter(Boolean)` which allocated an entirely new array just to remove empty lines.
**Action:** Use `String.prototype.substring(start, i)` with index tracking instead of character-by-character concatenation to drastically reduce GC overhead and speed up string extraction. Skip empty lines within a `for` loop instead of creating intermediate arrays with `filter(Boolean)`. This reduced parsing time from ~345ms to ~239ms for a 50k line test CSV.
