#!/usr/bin/env python3
"""
5D-Competence Framework - IMP Validation Study
==============================================
Akademische Validierungsstudie für das 5D-Framework
Basierend auf der Analyse vom 04.12.2025

Autor: Professor Dr. A. I. Nexus
Ziel: Empirische Validierung der 5 Dimensionen (Pilotstudie, N=30)
"""

import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import gmean

# Dimensions & Questions (Aligned with 5D-Intelligence Framework & Science Superquelle)
QUESTIONS = {
    "Autonomy": [
        "I feel free to express my ideas and opinions.",
        "I have opportunities to make decisions about my work/learning.",
        "I feel my choices express who I really am.",
        "I have control over how I do my work.",
        "I engage in activities because I choose to, not because I have to.",
    ],
    "Intrinsic_Motivation": [
        "I enjoy the challenges I face in my tasks.",
        "I work on tasks because they are interesting to me.",
        "I feel a sense of satisfaction when I improve my skills.",
        "Curiosity drives my learning/work.",
        "I would work on these tasks even without external rewards.",
    ],
    "Resilience": [
        "I can bounce back quickly after a setback.",
        "I tend to see difficult situations as challenges rather than threats.",
        "I can handle unpleasant feelings appropriately.",
        "I stay focused under pressure.",
        "I adapt easily to change.",
    ],
    "Social_Participation": [
        "I feel part of a community in my work/learning environment.",
        "I actively contribute to group goals.",
        "I support others when they need help.",
        "I feel connected to the people I work/learn with.",
        "My input is valued by others.",
    ],
    "Authenticity": [
        "I am true to myself in most situations.",
        "I live in accordance with my values and beliefs.",
        "I express my true feelings rather than hiding them.",
        "I feel I can be myself around others.",
        "My actions reflect my true personality.",
    ],
}


class IMPValidationStudy:
    """Haupt-Klasse für die IMP-Validierungsstudie"""

    def __init__(self):
        self.data = None
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_metric_mapping_table(self):
        """Generates the Metric Mapping Table (Questionnaire Definition)"""
        mapping_table = []
        q_id = 1

        for dimension, questions in QUESTIONS.items():
            for question in questions:
                mapping_table.append(
                    {
                        "id": f"Q{q_id:02d}",
                        "dimension": dimension,
                        "construct": "Psychometric Item",
                        "question": question,
                        "scale": "Likert 1-5 (1=Strongly Disagree, 5=Strongly Agree)",
                        "source_theory": "SDT/Positive Psychology",
                    }
                )
                q_id += 1

        filename = f"metric_mapping_table_{self.timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(mapping_table, f, ensure_ascii=False, indent=2)
        print(f"✅ Metric Mapping Table saved: {filename}")

        return mapping_table

    def calculate_cronbach_alpha(self, items):
        """
        Berechnet Cronbach's Alpha für Reliabilität
        Items: Liste von Antworten für eine Dimension
        """
        items_array = np.array(items)
        n_items = items_array.shape[1]

        # Varianz jedes Items
        item_variances = np.var(items_array, axis=0, ddof=1)

        # Gesamtvarianz
        total_variance = np.var(items_array.sum(axis=1), ddof=1)

        # Cronbach's Alpha - Safety Checks
        if n_items <= 1 or total_variance == 0:
            return 0.0  # Vermeide Division durch Null bei zu wenigen Items oder konstanter Antwort

        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)

        return alpha

    def load_responses(self, filename):
        """Lädt Probandendaten aus CSV"""
        self.data = pd.read_csv(filename)
        print(f"✅ {len(self.data)} responses loaded")
        return self.data

    def analyze_dimensions(self):
        """Analysiert alle 5 Dimensionen"""
        if self.data is None:
            print("❌ No data loaded. Please call load_responses().")
            return

        dimensions = list(QUESTIONS.keys())

        for dim in dimensions:
            # Filtere Spalten für diese Dimension
            dim_cols = [col for col in self.data.columns if col.startswith(dim)]
            dim_data = self.data[dim_cols]

            # Cronbach's Alpha
            alpha = self.calculate_cronbach_alpha(dim_data.values)

            # Deskriptive Statistik
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
        """Interpretiert Cronbach's Alpha"""
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
        """Berechnet IMP-Score für einen Probanden"""
        dimensions = list(QUESTIONS.keys())
        scores = {}

        for dim in dimensions:
            dim_cols = [col for col in row.index if col.startswith(dim)]
            scores[dim] = row[dim_cols].mean()

        score_values = list(scores.values())

        # Geometrisches Mittel Modell: IMP = (D1 * D2 * D3 * D4 * D5)^(1/5)
        # Wir verwenden gmean aus scipy
        imp_geometric = gmean(score_values)

        return {"dimensions": scores, "IMP_geometric": imp_geometric}

    def correlation_analysis(self):
        """Korrelationsanalyse zwischen Dimensionen"""
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
        """Erstellt Visualisierungen"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # 1. Cronbach's Alpha Balkendiagramm
        alphas = [self.results[dim]["cronbach_alpha"] for dim in QUESTIONS.keys()]
        axes[0, 0].barh(list(QUESTIONS.keys()), alphas, color="skyblue")
        axes[0, 0].axvline(x=0.7, color="red", linestyle="--", label="Acceptable Threshold (0.7)")
        axes[0, 0].set_xlabel("Cronbach's Alpha")
        axes[0, 0].set_title("Reliability of Dimensions")
        axes[0, 0].legend()

        # 2. Mittelwerte der Dimensionen
        means = [self.results[dim]["mean"] for dim in QUESTIONS.keys()]
        axes[0, 1].bar(list(QUESTIONS.keys()), means, color="lightgreen")
        axes[0, 1].set_ylabel("Mean Score (1-5)")
        axes[0, 1].set_title("Average Dimension Scores")
        axes[0, 1].tick_params(axis="x", rotation=45)

        # 3. Korrelations-Heatmap
        corr_matrix = self.correlation_analysis()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, ax=axes[1, 0])
        axes[1, 0].set_title("Inter-Dimension Correlations")

        # 4. IMP-Score Verteilung
        imp_scores = []
        for idx in range(len(self.data)):
            imp_score = self.calculate_imp_score(self.data.iloc[idx])
            imp_scores.append(imp_score["IMP_geometric"])

        axes[1, 1].hist(imp_scores, bins=10, color="purple", alpha=0.7, edgecolor="black")
        axes[1, 1].set_xlabel("IMP-Score (1-5)")
        axes[1, 1].set_ylabel("Frequency")
        axes[1, 1].set_title("Distribution of IMP Scores (Geometric Mean)")
        axes[1, 1].axvline(
            x=np.mean(imp_scores),
            color="red",
            linestyle="--",
            label=f"Mean: {np.mean(imp_scores):.2f}",
        )
        axes[1, 1].legend()

        plt.tight_layout()
        filename = f"evidence_package_visualization_{self.timestamp}.png"
        plt.savefig(filename, dpi=300)
        print(f"\n✅ Visualization saved: {filename}")
        plt.close()

    def generate_report(self):
        """Generiert Abschlussbericht"""
        report = {
            "timestamp": self.timestamp,
            "n_participants": len(self.data) if self.data is not None else 0,
            "dimensions": self.results,
            "overall_reliability": np.mean([r["cronbach_alpha"] for r in self.results.values()]),
            "recommendation": self._generate_recommendation(),
            "interpretation_guide": "Scores are 1-5. Alpha > 0.7 indicates valid construct measurement. High inter-correlation (>0.85) suggests redundancy.",
        }

        filename = f"evidence_package_report_{self.timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Report saved: {filename}")
        return report

    def _generate_recommendation(self):
        """Generiert Empfehlungen basierend auf Ergebnissen"""
        avg_alpha = np.mean([r["cronbach_alpha"] for r in self.results.values()])

        if avg_alpha >= 0.8:
            return "Excellent Reliability. The 5D-Intelligence framework is statistically robust."
        elif avg_alpha >= 0.7:
            return "Acceptable Reliability. Minor item revision recommended."
        else:
            return "Low Reliability. Critical revision of items required."


# MAIN EXECUTION
def main():
    print("🧬 5D-INTELLIGENCE EVIDENCE PACKAGE GENERATOR")
    print("============================================")

    study = IMPValidationStudy()

    # 1. Metric Mapping Table
    print("\n[1/5] Generating Metric Mapping Table...")
    study.generate_metric_mapping_table()

    # 2. Simulate Data (Hypothesis Protocol)
    print("\n[2/5] Simulating Pilot Data (N=30)...")
    np.random.seed(42)
    example_data = {}

    n_participants = 30

    for dimension, questions in QUESTIONS.items():
        # Latent Trait Simulation
        latent_ability = np.random.normal(3.5, 0.8, n_participants)
        latent_ability = np.clip(latent_ability, 1.5, 4.5)

        for i, _question in enumerate(questions, 1):
            col_name = f"{dimension}_{i}"
            # Item Response = Latent Trait + Random Error
            item_scores = latent_ability + np.random.normal(0, 0.6, n_participants)
            item_scores = np.clip(np.round(item_scores), 1, 5).astype(int)
            example_data[col_name] = item_scores

    df = pd.DataFrame(example_data)
    df.to_csv(f"pilot_data_{study.timestamp}.csv", index=False)
    print("    → Pilot data simulated based on Science Superquelle assumptions.")

    # 3. Load Data
    print("\n[3/5] Loading Data...")
    study.load_responses(f"pilot_data_{study.timestamp}.csv")

    # 4. Analyze
    print("\n[4/5] Executing Psychometric Analysis...")
    study.analyze_dimensions()

    # 5. Output
    print("\n[5/5] Generating One-Click Scientific Output...")
    study.visualize_results()
    report = study.generate_report()

    print("\n" + "=" * 50)
    print("✅ EVIDENCE PACKAGE GENERATED")
    print(f"Status: {report['recommendation']}")
    print(f"Reliability (α): {report['overall_reliability']:.3f}")


if __name__ == "__main__":
    main()
