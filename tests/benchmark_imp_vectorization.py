import time
import numpy as np
import pandas as pd
from scipy.stats import gmean
import sys
import os

# Import the class from the source file
sys.path.append(os.getcwd())
from validation.imp_validation_study import IMPValidationStudy, QUESTIONS

def generate_large_dataset(n_participants=10000):
    data = {}
    for dimension, questions in QUESTIONS.items():
        # Match the column naming convention of the original script: f"{dimension}_{i}"
        for i, _ in enumerate(questions, 1):
             col_name = f"{dimension}_{i}"
             data[col_name] = np.random.randint(1, 6, n_participants) # Use 1-5 to avoid 0s for gmean if strict
    return pd.DataFrame(data)

def main():
    print("Generating dataset...")
    # Using 1-5 range to ensure gmean doesn't hit 0 (though 0 is valid for gmean -> 0)
    # But let's use 1-5 to match typical Likert scale responses usually being 1-5 or similar.
    # The original script uses 0-5.
    df = generate_large_dataset(n_participants=10000)
    print(f"Dataset shape: {df.shape}")

    study = IMPValidationStudy()

    # Benchmark Loop (Old method simulation)
    # Since we replaced the method in the class, we need to define the old method locally
    # or rely on the fact that I didn't remove the old method?
    # Wait, I REMOVED the old method call from visualize_results, but I KEPT calculate_imp_score method in the class!
    # Let's verify. Yes, I added calculate_imp_scores_vectorized but I did not delete calculate_imp_score.

    print("Starting loop-based calculation...")
    start_time = time.time()

    imp_scores_loop = []
    for idx in range(len(df)):
        imp_score = study.calculate_imp_score(df.iloc[idx])
        imp_scores_loop.append(imp_score["IMP_geometric"])

    loop_duration = time.time() - start_time
    print(f"Loop-based calculation took: {loop_duration:.4f} seconds")

    # Benchmark Vectorized (New method)
    print("Starting vectorized calculation...")
    start_time = time.time()

    imp_results_vec = study.calculate_imp_scores_vectorized(df)
    imp_scores_vec = imp_results_vec["IMP_geometric"]

    vec_duration = time.time() - start_time
    print(f"Vectorized calculation took: {vec_duration:.4f} seconds")

    # Debugging
    print("\nDebugging...")
    print(f"Loop first 5: {imp_scores_loop[:5]}")
    print(f"Vec first 5: {imp_scores_vec[:5]}")

    # Check for NaNs
    print(f"NaNs in Loop: {np.isnan(imp_scores_loop).sum()}")
    print(f"NaNs in Vec: {np.isnan(imp_scores_vec).sum()}")

    # Validation
    print("\nValidating results...")
    # Convert both to numpy arrays for comparison
    loop_arr = np.array(imp_scores_loop)
    vec_arr = np.array(imp_scores_vec)

    # Check if they are close (floating point differences possible)
    is_close = np.allclose(loop_arr, vec_arr)
    print(f"Results match: {is_close}")

    if not is_close:
        diff = np.abs(loop_arr - vec_arr)
        print(f"Max difference: {np.nanmax(diff)}")

    speedup = loop_duration / vec_duration
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == "__main__":
    main()
