## 2024-05-23 - NumPy Slicing vs DataFrame Subsetting
**Learning:** Pandas DataFrame subsetting inside a loop (e.g., `df[cols].mean()`) is significantly slower than extracting the underlying NumPy array once and using slices (`arr[:, start:end].mean()`), especially when repeated multiple times.
**Action:** When calculating aggregates over multiple groups of columns, extract `df.values` once and use integer-based slicing if possible, or `np.mean(values[:, indices], axis=1)` if columns are not contiguous. This yielded a ~3x speedup.
