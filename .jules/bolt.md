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

## 2024-05-23 - ESLint Version Mismatch
**Learning:** The `docs/analysis` project expects ESLint v8 (based on flags like `--ext`), but the environment has ESLint v9, which requires `eslint.config.js`. The config file appears to be missing entirely, causing `npm run lint` to fail.
**Action:** When working in `docs/analysis`, rely on `npm run build` for verification until the linting configuration is fixed or migrated.

## 2024-05-23 - Missing PostCSS Config
**Learning:** Vite projects using Tailwind CSS require a `postcss.config.js` file to process styles correctly. If missing, the build may succeed but produce empty or unstyled CSS.
**Action:** Ensure `postcss.config.js` exists in Vite/Tailwind projects. If styles are missing despite a successful build, check for this configuration file.
