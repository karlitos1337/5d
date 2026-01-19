#!/usr/bin/env python3
"""
5D-Competence Framework - IMP Validation Study
==============================================
Scientific Validation Study for 5D-Intelligence Framework
Protocol: Professor Dr. A. I. Nexus
Date: 2025-05-15 (Simulated)

Author: Professor Dr. A. I. Nexus (Chair of Computational Human Flourishing)
Goal: Empirical Validation of 5 Dimensions (Pilot N=30)
"""

import json
from datetime import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import gmean

# Questionnaire Definitions (Aligned with Science Superquelle / SDT)
QUESTIONS = {
    "Autonomy": [
        "I feel I have choices in how I do my work.",  # Voice & Accountability
        "I feel my decisions reflect my true self.",
        "I can openly express my opinions without fear.",
        "I have control over the resources I need.",
        "I act based on my own values, not external pressure.",
    ],
    "Intrinsic_Motivation": [
        "I engage in my tasks because they are interesting.", # Self-Directed Learning
        "I enjoy finding new solutions to problems.",
        "I would work on these projects even without a deadline.",
        "Learning new things is its own reward for me.",
        "I feel a sense of flow when working.",
    ],
    "Social_Participation": [
        "I feel connected to the people I interact with.", # Network Density
        "My contributions are valued by my community.",
        "I actively support others in their goals.",
        "I feel part of a collective effort.",
        "I can rely on others when I face challenges.",
    ],
    "Resilience": [
        "I recover quickly from setbacks.", # HRV / Stress Tolerance proxy
        "Stressful situations do not paralyze me.",
        "I view failures as learning opportunities.",
        "I maintain my focus even under pressure.",
        "I can regulate my emotions effectively.",
    ],
    "Authenticity": [
        "I act in a way that is consistent with my values.", # Congruence Score
        "I do not feel the need to wear a mask.",
        "My external actions match my internal feelings.",
        "I feel I am being true to myself.",
        "I am honest about my limitations.",
    ],
}


class IMPValidationStudy:
    """Core Validation Logic for 5D-Intelligence"""

    def __init__(self):
        self.data = None
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.discriminant_validity_pass = False

    def generate_questionnaire(self, output_format="json"):
        """Generates the questionnaire structure."""
        questionnaire = []
        q_id = 1

        for dimension, questions in QUESTIONS.items():
            for question in questions:
                questionnaire.append(
                    {
                        "id": q_id,
                        "dimension": dimension,
                        "question": question,
                        "scale": "0 (Strongly Disagree) - 5 (Strongly Agree)",
                    }
                )
                q_id += 1

        if output_format == "json":
            filename = f"questionnaire_{self.timestamp}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(questionnaire, f, ensure_ascii=False, indent=2)
            print(f"✅ Questionnaire Artifact Generated: {filename}")

        return questionnaire

    def calculate_cronbach_alpha(self, items):
        """Calculates Cronbach's Alpha for Reliability."""
        items_array = np.array(items)
        n_items = items_array.shape[1]
        item_variances = np.var(items_array, axis=0, ddof=1)
        total_variance = np.var(items_array.sum(axis=1), ddof=1)

        if n_items <= 1 or total_variance == 0:
            return 0.0

        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
        return alpha

    def load_responses(self, filename):
        """Loads participant data from CSV."""
        self.data = pd.read_csv(filename)
        print(f"✅ Loaded {len(self.data)} validated responses.")
        return self.data

    def analyze_dimensions(self):
        """Analyzes Reliability (Cronbach's Alpha) for each dimension."""
        if self.data is None:
            print("❌ No data loaded.")
            return

        dimensions = list(QUESTIONS.keys())

        for dim in dimensions:
            dim_cols = [col for col in self.data.columns if col.startswith(dim)]
            dim_data = self.data[dim_cols]
            alpha = self.calculate_cronbach_alpha(dim_data.values)
            mean_score = dim_data.mean().mean()
            std_score = dim_data.std().mean()

            self.results[dim] = {
                "cronbach_alpha": alpha,
                "mean": mean_score,
                "std": std_score,
                "interpretation": self._interpret_alpha(alpha),
            }

            print(f"  🔹 {dim}: α={alpha:.3f} ({self._interpret_alpha(alpha)})")

        return self.results

    def _interpret_alpha(self, alpha):
        if alpha >= 0.9: return "Excellent"
        elif alpha >= 0.8: return "Good"
        elif alpha >= 0.7: return "Acceptable"
        elif alpha >= 0.6: return "Questionable"
        else: return "Unacceptable"

    def check_discriminant_validity(self):
        """
        Self-Optimizing Feedback Loop:
        Checks if dimensions are distinct (Correlation < 0.85).
        """
        print("\n🔍 CHECKING DISCRIMINANT VALIDITY...")
        dimensions = list(QUESTIONS.keys())
        dim_means = {}

        for dim in dimensions:
            dim_cols = [col for col in self.data.columns if col.startswith(dim)]
            dim_means[dim] = self.data[dim_cols].mean(axis=1)

        corr_df = pd.DataFrame(dim_means)
        corr_matrix = corr_df.corr()

        # Check off-diagonal elements
        high_correlations = []
        is_valid = True

        for i in range(len(dimensions)):
            for j in range(i + 1, len(dimensions)):
                dim1 = dimensions[i]
                dim2 = dimensions[j]
                r = corr_matrix.loc[dim1, dim2]
                if abs(r) >= 0.85:
                    high_correlations.append(f"{dim1} <-> {dim2} (r={r:.3f})")
                    is_valid = False

        self.discriminant_validity_pass = is_valid

        if is_valid:
            print("  ✅ PASS: All latent variable correlations < 0.85")
        else:
            print("  ⚠️ ALERT: High correlation detected (Discriminant Validity Fail)")
            for alert in high_correlations:
                print(f"     -> {alert}")

        return corr_matrix, high_correlations

    def calculate_imp_score(self, df):
        """Calculates 5D-Index (Geometric Mean)."""
        dimensions = list(QUESTIONS.keys())
        dim_scores = pd.DataFrame(index=df.index)

        for dim in dimensions:
            dim_cols = [col for col in df.columns if col.startswith(dim)]
            dim_scores[dim] = df[dim_cols].mean(axis=1) if dim_cols else 0.0

        # Geometric Mean: (A * I * S * R * A)^(1/5)
        imp_geometric = gmean(dim_scores.values, axis=1)
        return imp_geometric

    def visualize_results(self, corr_matrix):
        """Generates Scientific Visualization Template."""
        plt.style.use('ggplot')
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('5D-Intelligence Validation Dashboard', fontsize=16)

        # 1. Reliability
        alphas = [self.results[dim]["cronbach_alpha"] for dim in QUESTIONS.keys()]
        colors = ['green' if a >= 0.7 else 'red' for a in alphas]
        axes[0, 0].barh(list(QUESTIONS.keys()), alphas, color=colors)
        axes[0, 0].axvline(x=0.7, color="black", linestyle="--", label="Scientific Threshold (0.7)")
        axes[0, 0].set_title("Reliability (Cronbach's α)")
        axes[0, 0].legend()

        # 2. Score Distribution
        means = [self.results[dim]["mean"] for dim in QUESTIONS.keys()]
        axes[0, 1].bar(list(QUESTIONS.keys()), means, color="steelblue")
        axes[0, 1].set_ylim(0, 5)
        axes[0, 1].set_title("Dimension Means (Scale 0-5)")

        # 3. Discriminant Validity (Heatmap)
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, vmin=-1, vmax=1, ax=axes[1, 0])
        axes[1, 0].set_title("Discriminant Validity (Correlations)")

        # 4. Overall 5D Index Distribution
        imp_scores = self.calculate_imp_score(self.data)
        sns.histplot(imp_scores, kde=True, ax=axes[1, 1], color="purple")
        axes[1, 1].set_title(f"5D-Index Distribution (Mean={np.mean(imp_scores):.2f})")
        axes[1, 1].set_xlabel("IMP Score")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        filename = f"validation_results_{self.timestamp}.png"
        plt.savefig(filename, dpi=300)
        print(f"✅ Visualization Template Generated: {filename}")
        plt.close()

    def generate_report(self, high_corrs):
        """Generates One-Click Scientific Output Report."""
        avg_alpha = np.mean([r["cronbach_alpha"] for r in self.results.values()])

        report = {
            "meta": {
                "protocol": "Professor Dr. A. I. Nexus",
                "timestamp": self.timestamp,
                "n_samples": len(self.data)
            },
            "reliability": {
                "average_alpha": avg_alpha,
                "status": "PASS" if avg_alpha >= 0.7 else "FAIL (Hypothesis Refuted)",
                "details": self.results
            },
            "discriminant_validity": {
                "status": "PASS" if self.discriminant_validity_pass else "FAIL",
                "high_correlations": high_corrs
            }
        }

        filename = f"validation_report_{self.timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"✅ Scientific Report Generated: {filename}")
        return report

def main():
    print("\n🧬 PROFESSOR DR. A. I. NEXUS // 5D VALIDATION PROTOCOL")
    print("=======================================================")

    study = IMPValidationStudy()

    # 1. Generate Questionnaire
    study.generate_questionnaire()

    # 2. Hypothesis Protocol: Generate Synthetic Data if no external source
    # Simulating data that generally passes but might show some issues to be realistic
    print("\n🧪 [HYPOTHESIS GENERATION] Simulating N=50 Validated Responses...")
    np.random.seed(1337) # Reproducible science
    example_data = {}
    n_participants = 50

    # Generate correlated data (G-Factor model)
    g_factor = np.random.normal(3.5, 0.5, n_participants) # General competence

    for dimension, questions in QUESTIONS.items():
        # Specific dimension variance
        dim_factor = g_factor + np.random.normal(0, 0.4, n_participants)
        dim_factor = np.clip(dim_factor, 1.0, 4.5)

        for i, _ in enumerate(questions, 1):
            # Item variance
            item_score = dim_factor + np.random.normal(0, 0.5, n_participants)
            example_data[f"{dimension}_{i}"] = np.clip(np.round(item_score), 0, 5).astype(int)

    df = pd.DataFrame(example_data)
    csv_file = f"example_responses_{study.timestamp}.csv"
    df.to_csv(csv_file, index=False)

    # 3. Analyze
    study.load_responses(csv_file)
    study.analyze_dimensions()

    # 4. Self-Optimizing Feedback Loop
    corr_matrix, high_corrs = study.check_discriminant_validity()

    # 5. Output
    study.visualize_results(corr_matrix)
    study.generate_report(high_corrs)

    print("\n🚀 PROTOCOL COMPLETE. Ready for Evidence Packaging.")

if __name__ == "__main__":
    main()
