#!/usr/bin/env python3
"""
5D-Intelligence Framework - Validation Study
============================================
Academic Validation Study for the 5D-Framework
Based on the analysis of 2026-02-05

Author: Professor Dr. A. I. Nexus
Goal: Empirical Validation of the 5 Dimensions (Pilot Study, N=30)
"""

import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import gmean

# Questionnaire Definitions (Aligned with 5D-Intelligence Framework)
QUESTIONS = {
    "Autonomy": [
        "I feel I have a choice in how I do my work.",
        "I can make decisions that affect my life.",
        "I feel free to express my opinions.",
        "I have control over my daily schedule.",
        "I take responsibility for my own actions.",
    ],
    "Intrinsic_Motivation": [
        "I work on tasks because they truly interest me.",
        "Challenges motivate me, even without external rewards.",
        "I set ambitious goals for myself independently.",
        "I persist with my projects even when difficulties arise.",
        "Learning and growth are more important to me than grades or recognition.",
    ],
    "Social_Participation": [
        "I actively contribute to solutions in group projects.",
        "I can communicate my ideas clearly and convincingly.",
        "I listen attentively to others and build on their ideas.",
        "Collaboration with others enriches my work.",
        "I can empathize well with the perspectives of others.",
    ],
    "Resilience": [
        "I quickly recover my performance after setbacks.",
        "I can regulate my emotions even in difficult situations.",
        "Stress influences my performance only temporarily.",
        "I learn constructively from mistakes for the future.",
        "I remain focused and capable of acting even under pressure.",
    ],
    "Authenticity": [
        "I act in accordance with my values and beliefs.",
        "I feel I can be myself around others.",
        "I am honest about my feelings and thoughts.",
        "My actions reflect who I really am.",
        "I do not pretend to be someone I am not.",
    ],
}


class IMPValidationStudy:
    """Main Class for 5D Validation Study"""

    def __init__(self):
        self.data = None
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_questionnaire(self, output_format="json"):
        """Generates the questionnaire"""
        questionnaire = []
        q_id = 1

        for dimension, questions in QUESTIONS.items():
            for question in questions:
                questionnaire.append(
                    {
                        "id": q_id,
                        "dimension": dimension,
                        "question": question,
                        "scale": "0 (strongly disagree) - 5 (strongly agree)",
                    }
                )
                q_id += 1

        if output_format == "json":
            filename = f"questionnaire_{self.timestamp}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(questionnaire, f, ensure_ascii=False, indent=2)
            print(f"✅ Questionnaire saved: {filename}")

        return questionnaire

    def calculate_cronbach_alpha(self, items):
        """
        Calculates Cronbach's Alpha for Reliability
        Items: List of answers for a dimension
        """
        items_array = np.array(items)
        n_items = items_array.shape[1]

        # Variance of each item
        item_variances = np.var(items_array, axis=0, ddof=1)

        # Total variance
        total_variance = np.var(items_array.sum(axis=1), ddof=1)

        # Cronbach's Alpha - Safety Checks
        if n_items <= 1 or total_variance == 0:
            return 0.0  # Avoid division by zero

        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)

        return alpha

    def load_responses(self, filename):
        """Loads participant data from CSV"""
        self.data = pd.read_csv(filename)
        print(f"✅ {len(self.data)} responses loaded")
        return self.data

    def analyze_dimensions(self):
        """Analyzes all 5 Dimensions"""
        if self.data is None:
            print("❌ No data loaded. Please call load_responses().")
            return

        dimensions = list(QUESTIONS.keys())

        for dim in dimensions:
            # Filter columns for this dimension
            dim_cols = [col for col in self.data.columns if col.startswith(dim)]
            dim_data = self.data[dim_cols]

            # Cronbach's Alpha
            alpha = self.calculate_cronbach_alpha(dim_data.values)

            # Descriptive Statistics
            mean_score = dim_data.mean().mean()
            std_score = dim_data.std().mean()

            self.results[dim] = {
                "cronbach_alpha": alpha,
                "mean": mean_score,
                "std": std_score,
                "interpretation": self._interpret_alpha(alpha),
            }

            print(f"\n{dim}:")
            print(f"  Cronbach's α: {alpha:.3f} - {self._interpret_alpha(alpha)}")
            print(f"  Mean: {mean_score:.2f} (±{std_score:.2f})")

        return self.results

    def _interpret_alpha(self, alpha):
        """Interprets Cronbach's Alpha"""
        if alpha >= 0.9:
            return "Excellent"
        elif alpha >= 0.8:
            return "Good"
        elif alpha >= 0.7:
            return "Acceptable"
        elif alpha >= 0.6:
            return "Questionable"
        else:
            return "Unacceptable"

    def calculate_imp_score(self, row):
        """Calculates 5D-Score for a participant"""
        dimensions = list(QUESTIONS.keys())
        scores = {}

        for dim in dimensions:
            dim_cols = [col for col in row.index if col.startswith(dim)]
            scores[dim] = row[dim_cols].mean()

        score_values = list(scores.values())

        # Geometric Mean Model: Score = (A * I * S * R * A)^(1/5)
        imp_geometric = gmean(score_values)

        # Additive Model (for comparison)
        imp_additive = np.mean(score_values)

        return {"dimensions": scores, "Score_geometric": imp_geometric, "Score_additive": imp_additive}

    def calculate_imp_scores_vectorized(self, df):
        """Calculates 5D-Scores for a DataFrame (vectorized)"""
        dimensions = list(QUESTIONS.keys())
        dim_scores = pd.DataFrame(index=df.index)

        # Calculate means per dimension
        for dim in dimensions:
            dim_cols = [col for col in df.columns if col.startswith(dim)]
            if dim_cols:
                dim_scores[dim] = df[dim_cols].mean(axis=1)
            else:
                dim_scores[dim] = 0.0

        # Geometric mean across dimensions
        imp_geometric = gmean(dim_scores.values, axis=1)

        # Additive Model
        imp_additive = dim_scores.mean(axis=1)

        return {
            "dimensions": dim_scores,
            "Score_geometric": imp_geometric,
            "Score_additive": imp_additive
        }

    def correlation_analysis(self):
        """Correlation analysis between dimensions"""
        dimensions = list(QUESTIONS.keys())
        dim_means = {}

        for dim in dimensions:
            dim_cols = [col for col in self.data.columns if col.startswith(dim)]
            dim_means[dim] = self.data[dim_cols].mean(axis=1)

        corr_df = pd.DataFrame(dim_means)
        correlation_matrix = corr_df.corr()

        print("\n=== CORRELATION MATRIX ===")
        print(correlation_matrix.round(3))

        return correlation_matrix

    def visualize_results(self):
        """Creates Visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # 1. Cronbach's Alpha Bar Chart
        alphas = [self.results[dim]["cronbach_alpha"] for dim in QUESTIONS.keys()]
        axes[0, 0].barh(list(QUESTIONS.keys()), alphas, color="skyblue")
        axes[0, 0].axvline(x=0.7, color="red", linestyle="--", label="Acceptable Threshold")
        axes[0, 0].set_xlabel("Cronbach's Alpha")
        axes[0, 0].set_title("Reliability of Dimensions")
        axes[0, 0].legend()

        # 2. Mean Scores of Dimensions
        means = [self.results[dim]["mean"] for dim in QUESTIONS.keys()]
        axes[0, 1].bar(list(QUESTIONS.keys()), means, color="lightgreen")
        axes[0, 1].set_ylabel("Mean Score (0-5)")
        axes[0, 1].set_title("Average Ratings")
        axes[0, 1].tick_params(axis="x", rotation=45)

        # 3. Correlation Heatmap
        corr_matrix = self.correlation_analysis()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, ax=axes[1, 0])
        axes[1, 0].set_title("Correlations between Dimensions")

        # 4. Score Distribution
        results_vec = self.calculate_imp_scores_vectorized(self.data)
        imp_scores = results_vec["Score_geometric"]

        axes[1, 1].hist(imp_scores, bins=10, color="purple", alpha=0.7, edgecolor="black")
        axes[1, 1].set_xlabel("5D-Score (0-5)")
        axes[1, 1].set_ylabel("Frequency")
        axes[1, 1].set_title("Distribution of 5D-Scores (Geometric)")
        axes[1, 1].axvline(
            x=np.mean(imp_scores),
            color="red",
            linestyle="--",
            label=f"Mean: {np.mean(imp_scores):.2f}",
        )
        axes[1, 1].legend()

        plt.tight_layout()
        filename = f"validation_results_{self.timestamp}.png"
        plt.savefig(filename, dpi=300)
        print(f"\n✅ Visualization saved: {filename}")
        plt.close()

    def generate_report(self):
        """Generates Final Report"""
        report = {
            "timestamp": self.timestamp,
            "n_participants": len(self.data) if self.data is not None else 0,
            "dimensions": self.results,
            "overall_reliability": np.mean([r["cronbach_alpha"] for r in self.results.values()]),
            "recommendation": self._generate_recommendation(),
        }

        filename = f"validation_report_{self.timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Report saved: {filename}")
        return report

    def _generate_recommendation(self):
        """Generates recommendations based on results"""
        avg_alpha = np.mean([r["cronbach_alpha"] for r in self.results.values()])

        if avg_alpha >= 0.8:
            return "The 5D-Framework shows good to excellent reliability. Ready for preprint publication (Pilot Study)."
        elif avg_alpha >= 0.7:
            return "The Framework is acceptable, but improvement of individual items is recommended."
        else:
            return "Reliability below threshold. Items must be revised."


# MAIN EXECUTION
def main():
    print("⚡ 5D-INTELLIGENCE VALIDATION STUDY (PILOT) STARTED \u26a1")
    print("=" * 50)

    study = IMPValidationStudy()

    # 1. Generate Questionnaire
    print("\n[1/5] Generating Questionnaire...")
    questionnaire = study.generate_questionnaire()
    print(f"    → {len(questionnaire)} questions created")

    # 2. Generate Example Data (for Demo - simulating realistic correlations)
    print("\n[2/5] Generating Example Data (30 Participants)...")
    np.random.seed(42)
    example_data = {}

    n_participants = 30

    for dimension, questions in QUESTIONS.items():
        # Latent ability of the participant in this dimension
        latent_ability = np.random.normal(3.5, 0.8, n_participants)
        latent_ability = np.clip(latent_ability, 1, 4.5)

        for i, _question in enumerate(questions, 1):
            col_name = f"{dimension}_{i}"
            # Item response is latent_ability + Noise
            item_scores = latent_ability + np.random.normal(0, 0.6, n_participants)
            item_scores = np.clip(np.round(item_scores), 0, 5).astype(int)
            example_data[col_name] = item_scores

    df = pd.DataFrame(example_data)
    df.to_csv(f"example_responses_{study.timestamp}.csv", index=False)
    print("    → Example CSV created (with correlated data for realistic Alpha)")

    # 3. Load Data
    print("\n[3/5] Loading Data...")
    study.load_responses(f"example_responses_{study.timestamp}.csv")

    # 4. Perform Analysis
    print("\n[4/5] Analyzing Dimensions...")
    print("=" * 50)
    study.analyze_dimensions()

    # 5. Visualizations and Report
    print("\n[5/5] Creating Visualizations and Report...")
    study.visualize_results()
    report = study.generate_report()

    print("\n" + "=" * 50)
    print("✅ VALIDATION STUDY COMPLETED!")
    print(f"\nRECOMMENDATION: {report['recommendation']}")
    print(f"Average Reliability (α): {report['overall_reliability']:.3f}")
    print("\nNEXT STEPS:")
    print("  1. Recruit real participants (Target: 30+)")
    print("  2. Put questionnaire online")
    print("  3. Collect data and export to CSV")
    print("  4. Run this script again with real data")
    print("  5. Integrate results into Preprint Paper")


if __name__ == "__main__":
    main()
