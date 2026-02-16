#!/usr/bin/env python3
"""
5D-Intelligence Visualization Template
======================================
Generates scientific visualizations for the 5D-Competence Framework.

Usage:
    python3 visualization_template.py <data_file.csv>

Requirements:
    - pandas, matplotlib, numpy, seaborn

Input CSV Format:
    Must contain columns starting with:
    - Autonomy_
    - Intrinsic_Motivation_
    - Resilience_
    - Social_Participation_
    - Authenticity_ (or Environment_Optimization depending on mapping)

    Or pre-calculated dimension scores:
    - Autonomy
    - Intrinsic_Motivation
    - Resilience
    - Social_Participation
    - Authenticity
"""

import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

# Configure style
try:
    plt.style.use("seaborn-v0_8-whitegrid")
except:
    plt.style.use("seaborn-whitegrid")  # Fallback for older mpl

DIMENSIONS = [
    "Autonomy",
    "Intrinsic_Motivation",
    "Resilience",
    "Social_Participation",
    "Authenticity",
]


def load_data(filepath):
    """Loads data from CSV."""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} records from {filepath}")
        return df
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)


def calculate_dimension_scores(df):
    """Calculates mean scores for dimensions if raw item data is provided."""
    scores = pd.DataFrame(index=df.index)

    for dim in DIMENSIONS:
        # Check for direct score column
        if dim in df.columns:
            scores[dim] = df[dim]
        else:
            # Check for item columns (prefix matching)
            # Note: Mapping might vary, here we assume standard prefixes or try to match closely
            # Mapping 'Authenticity' might map to 'Environment_Optimization' or similar in some versions
            # We try to find columns starting with the dimension name or a mapped alias

            aliases = [dim]
            if dim == "Authenticity":
                aliases.append("Environment_Optimization")
                aliases.append("Competence")

            dim_cols = []
            for alias in aliases:
                found = [c for c in df.columns if c.startswith(alias) and c != alias]
                if found:
                    dim_cols = found
                    break

            if dim_cols:
                scores[dim] = df[dim_cols].mean(axis=1)
                print(f"   -> Calculated {dim} from {len(dim_cols)} items.")
            else:
                print(
                    f"⚠️  Warning: No data found for dimension '{dim}'. Filling with 0."
                )
                scores[dim] = 0.0

    return scores


def plot_radar_chart(scores_df, output_file="5d_radar_chart.png"):
    """Generates a radar chart of average scores."""

    # Calculate means
    means = scores_df.mean().values.tolist()
    N = len(DIMENSIONS)

    # Compute angle for each axis
    angles = [n / float(N) * 2 * pi for n in range(N)]

    # Close the plot
    means += means[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Draw one axe per variable + labels
    plt.xticks(angles[:-1], DIMENSIONS, color="grey", size=10)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=7)
    plt.ylim(0, 5)

    # Plot data
    ax.plot(
        angles,
        means,
        linewidth=2,
        linestyle="solid",
        color="blue",
        label="Average Profile",
    )
    ax.fill(angles, means, "b", alpha=0.1)

    plt.title("5D-Competence Profile (Average)", size=15, y=1.1)
    plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"✅ Saved Radar Chart: {output_file}")
    plt.close()


def plot_distribution(scores_df, output_file="5d_distribution.png"):
    """Generates a distribution plot of the overall score."""
    # Calculate overall geometric mean score
    # Filter out 0s to avoid log(0) issues if using geometric mean
    data = scores_df.replace(0, np.nan)
    # Using arithmetic mean for simplicity if geometric fails or for better distribution visual
    overall_scores = data.mean(axis=1)

    plt.figure(figsize=(10, 6))
    if not overall_scores.dropna().empty:
        sns.histplot(overall_scores, kde=True, bins=15, color="purple")
        plt.axvline(
            overall_scores.mean(),
            color="red",
            linestyle="--",
            label=f"Mean: {overall_scores.mean():.2f}",
        )
    else:
        print("⚠️  Not enough data to plot distribution.")

    plt.title("Distribution of Overall 5D-Intelligence Scores (Mean)")
    plt.xlabel("Score (0-5)")
    plt.ylabel("Frequency")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"✅ Saved Distribution Plot: {output_file}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate 5D-Intelligence Visualizations"
    )
    parser.add_argument("csv_file", help="Path to input CSV file")
    parser.add_argument(
        "--output-radar",
        default="5d_radar_chart.png",
        help="Output filename for radar chart",
    )
    parser.add_argument(
        "--output-dist",
        default="5d_distribution.png",
        help="Output filename for distribution plot",
    )

    args = parser.parse_args()

    print("📊 5D-Intelligence Visualization Generator")
    print("=" * 40)

    df = load_data(args.csv_file)
    scores = calculate_dimension_scores(df)

    plot_radar_chart(scores, args.output_radar)
    plot_distribution(scores, args.output_dist)

    print("\n✅ Visualization generation complete.")


if __name__ == "__main__":
    main()
