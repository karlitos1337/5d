## 2024-12-14 - Python Vectorization vs Loops
**Learning:** Python loops over Pandas DataFrames are incredibly slow compared to vectorized operations.
**Action:** Always replace row-iteration (`iterrows`, or index loops) with vectorized Pandas/NumPy operations when possible. In this case, `gmean(dataframe, axis=1)` provided a ~1500x speedup over iterating rows.
