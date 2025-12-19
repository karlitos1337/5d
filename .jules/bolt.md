## 2024-12-19 - Vectorized Pandas Operations
**Learning:** Python loops over Pandas DataFrames (`iterrows` or index-based) are extremely slow (~1000x slower) compared to vectorized operations.
**Action:** Always prefer `df.mean(axis=1)` or other vectorized functions over row-by-row iteration for calculations.
