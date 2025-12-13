## 2024-05-24 - [Initial Journal]
**Learning:** Journal file was missing.
**Action:** Created .jules/bolt.md to track learnings.

## 2025-12-13 - [Vectorized IMP Score Calculation]
**Learning:** Replaced a row-by-row iteration in Pandas with vectorized operations for calculating Geometric Mean.
**Impact:** 1476x speedup on N=10,000 dataset (26s -> 0.017s).
**Action:** Always look for loops over Pandas DataFrames (`for idx in range(len(df))`) and replace them with vectorized operations.
