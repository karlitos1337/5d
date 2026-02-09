#!/usr/bin/env python3
"""
5D-Competence Framework: Modellvergleich-Simulation
===================================================
Geometrisches Mittel vs. Additives IMP-Modell

Ziel: Zeige die Vorteile des geometrischen Mittels
      (keine Überkompensation, aber faire Skalierung)
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import gmean


class IMPModelComparison:
    """Vergleicht Geometrisches Mittel vs. additives IMP-Modell"""

    def __init__(self, n_simulations=1000):
        self.n_simulations = n_simulations
        self.results = None

    def generate_dimension_scores(self, mean=3.5, std=1.0):
        """
        Generiert realistische Dimensionswerte
        Skala 0-5, Normalverteilung
        """
        scores = np.random.normal(mean, std, (self.n_simulations, 5))
        scores = np.clip(
            scores, 0.1, 5
        )  # Begrenze auf 0.1-5 (vermeide absolute 0 für Simulation der Skalierung)
        return scores

    def calculate_imp_geometric(self, dimensions):
        """IMP = (C * M * S * R * E)^(1/5)"""
        imp = gmean(dimensions, axis=1)
        return imp

    def calculate_imp_additive(self, dimensions):
        """IMP = (C + M + S + R + E) / 5"""
        imp = np.mean(dimensions, axis=1)
        return imp

    def simulate_zero_impact(self):
        """
        Zeigt Effekt von Null-Werten (Zero-Impact Principle)
        """
        print("\n💥 ZERO-IMPACT-ANALYSE")
        print("=" * 50)

        # Szenario: 4 Dimensionen perfekt (5), 1 Dimension = 0
        perfect_zero = np.array([[5, 5, 5, 5, 0]])
        # Szenario: 4 Dimensionen perfekt (5), 1 Dimension = 0.5 (schwach)
        perfect_weak = np.array([[5, 5, 5, 5, 0.5]])

        # Zero Check
        geo_zero = self.calculate_imp_geometric(perfect_zero)[0]
        add_zero = self.calculate_imp_additive(perfect_zero)[0]

        print("Szenario: 1 Dimension = 0, Rest = 5")
        print(f"  Geometrisch: {geo_zero:.2f} → Korrekt (0)")
        print(f"  Additiv:     {add_zero:.2f} → Falsch ( suggeriert hohe Kompetenz)")

        # Weak Check
        geo_weak = self.calculate_imp_geometric(perfect_weak)[0]
        add_weak = self.calculate_imp_additive(perfect_weak)[0]

        print("\nSzenario: 1 Dimension = 0.5 (sehr schwach), Rest = 5")
        print(f"  Geometrisch: {geo_weak:.2f} → Zieht Score deutlich runter")
        print(f"  Additiv:     {add_weak:.2f} → Ignoriert Schwäche weitgehend")

        return geo_zero, add_zero

    def run_comparison(self):
        """
        Führt vollständige Modellvergleich-Simulation durch
        """
        print("⚡ STARTE MODELLVERGLEICH-SIMULATION \u26a1")
        print("=" * 50)

        # Generiere Dimensionswerte
        dimensions = self.generate_dimension_scores()

        # Berechne beide Modelle
        imp_geo = self.calculate_imp_geometric(dimensions)
        imp_add = self.calculate_imp_additive(dimensions)

        # Speichere Ergebnisse
        self.results = pd.DataFrame(
            {
                "Cognitive": dimensions[:, 0],
                "Motivation": dimensions[:, 1],
                "Social": dimensions[:, 2],
                "Resilience": dimensions[:, 3],
                "Environment": dimensions[:, 4],
                "IMP_Geometric": imp_geo,
                "IMP_Additive": imp_add,
                "Differenz": imp_geo - imp_add,
            }
        )

        print(f"\n✅ {self.n_simulations} Simulationen durchgeführt")

        # Statistiken
        print("\n=== VERGLEICHSSTATISTIKEN ===")
        print(f"Geometrisch: M={imp_geo.mean():.2f}, SD={imp_geo.std():.2f}")
        print(f"Additiv:     M={imp_add.mean():.2f}, SD={imp_add.std():.2f}")
        print(f"Korrelation: r={stats.pearsonr(imp_geo, imp_add)[0]:.3f}")

        return self.results

    def visualize_comparison(self):
        """
        Erstellt umfassende Visualisierungen
        """
        if self.results is None:
            print("❌ Keine Ergebnisse. Bitte run_comparison() aufrufen.")
            return

        fig = plt.figure(figsize=(18, 12))

        # 1. Verteilungsvergleich
        ax1 = plt.subplot(2, 3, 1)
        self.results["IMP_Geometric"].hist(
            bins=30, alpha=0.7, color="blue", label="Geometrisch", ax=ax1
        )
        self.results["IMP_Additive"].hist(bins=30, alpha=0.7, color="red", label="Additiv", ax=ax1)
        ax1.set_xlabel("IMP-Score (0-5)")
        ax1.set_ylabel("Häufigkeit")
        ax1.set_title("Verteilungsvergleich")
        ax1.legend()

        # 2. Scatter-Plot
        ax2 = plt.subplot(2, 3, 2)
        ax2.scatter(self.results["IMP_Additive"], self.results["IMP_Geometric"], alpha=0.3)
        ax2.set_xlabel("IMP Additiv")
        ax2.set_ylabel("IMP Geometrisch")
        ax2.set_title("Modellkorrelation")
        # Diagonale Linie (y=x)
        ax2.plot([0, 5], [0, 5], "k--", alpha=0.5, label="y=x")
        ax2.legend()

        # 3. Sensitivitätsanalyse: Effekt von niedrigen Werten
        ax3 = plt.subplot(2, 3, 3)
        min_dims = self.results[
            ["Cognitive", "Motivation", "Social", "Resilience", "Environment"]
        ].min(axis=1)
        ax3.scatter(min_dims, self.results["IMP_Geometric"], alpha=0.3, color="purple")
        ax3.set_xlabel("Minimale Dimension")
        ax3.set_ylabel("IMP Geometrisch")
        ax3.set_title("Sensitivität gegenüber Minimum")

        # 4. Boxplots der Dimensionen
        ax4 = plt.subplot(2, 3, 4)
        dim_cols = ["Cognitive", "Motivation", "Social", "Resilience", "Environment"]
        self.results[dim_cols].boxplot(ax=ax4)
        ax4.set_ylabel("Score (0-5)")
        ax4.set_title("Dimensionsverteilungen")
        ax4.tick_params(axis="x", rotation=45)

        # 5. Differenzanalyse
        ax5 = plt.subplot(2, 3, 5)
        self.results["Differenz"].hist(bins=30, color="green", alpha=0.7, ax=ax5)
        ax5.set_xlabel("Differenz (Geo - Add)")
        ax5.set_ylabel("Häufigkeit")
        ax5.set_title("Geometrisch < Additiv (Normalfall)")
        ax5.axvline(0, color="black", linestyle="--")

        # 6. 3D-Scatter (3 Dimensionen)
        ax6 = fig.add_subplot(2, 3, 6, projection="3d")
        scatter = ax6.scatter(
            self.results["Cognitive"],
            self.results["Motivation"],
            self.results["Resilience"],
            c=self.results["IMP_Geometric"],
            cmap="viridis",
            alpha=0.6,
        )
        ax6.set_xlabel("Cognitive")
        ax6.set_ylabel("Motivation")
        ax6.set_zlabel("Resilience")
        ax6.set_title("3D-Dimensionsraum")
        plt.colorbar(scatter, ax=ax6, label="IMP Geo")

        plt.tight_layout()
        plt.savefig("model_comparison_results.png", dpi=300)
        print("\n✅ Visualisierung gespeichert: model_comparison_results.png")
        plt.close()

    def sensitivity_analysis(self):
        """
        Analysiert Sensitivität des geometrischen Modells
        """
        print("\n🔍 SENSITIVITÄTSANALYSE")
        print("=" * 50)

        # Teste verschiedene Szenarien (Skala 0-5)
        scenarios = [
            ([5, 5, 5, 5, 5], "Perfekt"),
            ([5, 5, 5, 5, 1], "Eine Dimension schwach (1)"),
            ([5, 5, 1, 1, 1], "Drei Dimensionen schwach (1)"),
            ([3, 3, 3, 3, 3], "Durchschnitt (3)"),
            ([2, 2, 2, 2, 2], "Niedrig (2)"),
        ]

        for dims, label in scenarios:
            dims_arr = np.array([dims])
            geo = self.calculate_imp_geometric(dims_arr)[0]
            add = self.calculate_imp_additive(dims_arr)[0]

            print(f"\n{label}: {dims}")
            print(f"  Geometrisch: {geo:.2f}")
            print(f"  Additiv:     {add:.2f}")
            if add > 0:
                print(f"  Verhältnis:  {geo / add:.2f} (Geo/Add)")


def main():
    print("🎯 5D-COMPETENCE MODELLVERGLEICH GESTARTET 🎯")
    print("=" * 60)

    # Initialisiere Simulation
    sim = IMPModelComparison(n_simulations=1000)

    # 1. Simulation durchführen
    results = sim.run_comparison()

    # 2. Zero-Impact zeigen
    sim.simulate_zero_impact()

    # 3. Sensitivitätsanalyse
    sim.sensitivity_analysis()

    # 4. Visualisierungen
    print("\n📊 Erstelle Visualisierungen...")
    sim.visualize_comparison()

    # 5. Exportiere Ergebnisse
    results.to_csv("model_comparison_data.csv", index=False)
    print("\n✅ Daten exportiert: model_comparison_data.csv")

    # FAZIT
    print("\n" + "=" * 60)
    print("🏆 FAZIT")
    print("=" * 60)
    print("Das GEOMETRISCHE MITTEL ist überlegen, weil:")
    print("  1. Skalentreue: Durchschnitt bleibt Durchschnitt (3,3,3,3,3 -> 3)")
    print("  2. Bestrafung von Schwächen: 1 schwache Dimension zieht den Score runter")
    print("     (aber nicht so extrem wie das Produkt)")
    print("  3. Zero-Impact: Eine 0 führt trotzdem zu 0")


if __name__ == "__main__":
    main()
