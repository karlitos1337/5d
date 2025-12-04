#!/usr/bin/env python3
"""
5D-Framework: Modellvergleich-Simulation
=========================================
Multiplikatives vs. Additives IMP-Modell

Ziel: Beweise die Überlegenheit des multiplikativen Ansatzes
      und zeige die Problematik von Null-Werten
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D

class IMPModelComparison:
    """Vergleicht multiplikatives vs. additives IMP-Modell"""
    
    def __init__(self, n_simulations=1000):
        self.n_simulations = n_simulations
        self.results = None
        
    def generate_dimension_scores(self, mean=5.0, std=1.2):
        """
        Generiert realistische Dimensionswerte
        Likert-Skala 1-7, Normalverteilung
        """
        scores = np.random.normal(mean, std, (self.n_simulations, 5))
        scores = np.clip(scores, 1, 7)  # Begrenze auf 1-7
        return scores
    
    def calculate_imp_multiplicative(self, dimensions):
        """IMP = A × IM × R × SP × Au (normalisiert)"""
        normalized = dimensions / 7.0  # Auf [0,1]
        imp = np.prod(normalized, axis=1) * 100  # In Prozent
        return imp
    
    def calculate_imp_additive(self, dimensions):
        """IMP = (A + IM + R + SP + Au) / 5"""
        imp = np.mean(dimensions, axis=1)
        return imp
    
    def simulate_zero_impact(self):
        """
        Zeigt dramatischen Effekt von Null-Werten
        """
        print("\n💥 ZERO-IMPACT-ANALYSE")
        print("="*50)
        
        # Szenario: 4 Dimensionen perfekt (7), 1 Dimension = 0
        perfect = np.array([[7, 7, 7, 7, 0]])
        
        mult = self.calculate_imp_multiplicative(perfect)[0]
        add = self.calculate_imp_additive(perfect)[0]
        
        print(f"Dimensions: {perfect[0]}")
        print(f"Multiplikativ: {mult:.1f}% → KOLLAPS bei Null!")
        print(f"Additiv: {add:.1f} → Noch 80% trotz Null")
        print("\n⚠️  Das Multiplikative Modell MUSS Nullen vermeiden!")
        
        return mult, add
    
    def run_comparison(self):
        """
        Führt vollständige Modellvergleich-Simulation durch
        """
        print("⚡ STARTE MODELLVERGLEICH-SIMULATION \u26a1")
        print("="*50)
        
        # Generiere Dimensionswerte
        dimensions = self.generate_dimension_scores()
        
        # Berechne beide Modelle
        imp_mult = self.calculate_imp_multiplicative(dimensions)
        imp_add = self.calculate_imp_additive(dimensions)
        
        # Speichere Ergebnisse
        self.results = pd.DataFrame({
            'Autonomie': dimensions[:, 0],
            'Motivation': dimensions[:, 1],
            'Resilienz': dimensions[:, 2],
            'Partizipation': dimensions[:, 3],
            'Authentizität': dimensions[:, 4],
            'IMP_Multiplikativ': imp_mult,
            'IMP_Additiv': imp_add,
            'Differenz': imp_mult - (imp_add * 100 / 7)  # Normalisiert
        })
        
        print(f"\n✅ {self.n_simulations} Simulationen durchgeführt")
        
        # Statistiken
        print("\n=== VERGLEICHSSTATISTIKEN ===")
        print(f"Multiplikativ: M={imp_mult.mean():.1f}%, SD={imp_mult.std():.1f}")
        print(f"Additiv: M={imp_add.mean():.1f}, SD={imp_add.std():.1f}")
        print(f"Korrelation: r={stats.pearsonr(imp_mult, imp_add)[0]:.3f}")
        
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
        self.results['IMP_Multiplikativ'].hist(bins=30, alpha=0.7, color='blue', label='Multiplikativ', ax=ax1)
        (self.results['IMP_Additiv'] * 100 / 7).hist(bins=30, alpha=0.7, color='red', label='Additiv (norm.)', ax=ax1)
        ax1.set_xlabel('IMP-Score (%)')
        ax1.set_ylabel('Häufigkeit')
        ax1.set_title('Verteilungsvergleich')
        ax1.legend()
        ax1.axvline(self.results['IMP_Multiplikativ'].mean(), color='blue', linestyle='--')
        ax1.axvline((self.results['IMP_Additiv'] * 100 / 7).mean(), color='red', linestyle='--')
        
        # 2. Scatter-Plot
        ax2 = plt.subplot(2, 3, 2)
        ax2.scatter(self.results['IMP_Additiv'], self.results['IMP_Multiplikativ'], alpha=0.3)
        ax2.set_xlabel('IMP Additiv')
        ax2.set_ylabel('IMP Multiplikativ (%)')
        ax2.set_title('Modellkorrelation')
        z = np.polyfit(self.results['IMP_Additiv'], self.results['IMP_Multiplikativ'], 1)
        p = np.poly1d(z)
        ax2.plot(self.results['IMP_Additiv'], p(self.results['IMP_Additiv']), "r--", alpha=0.8)
        
        # 3. Sensitivitätsanalyse: Effekt von niedrigen Werten
        ax3 = plt.subplot(2, 3, 3)
        min_dims = self.results[['Autonomie', 'Motivation', 'Resilienz', 'Partizipation', 'Authentizität']].min(axis=1)
        ax3.scatter(min_dims, self.results['IMP_Multiplikativ'], alpha=0.3, color='purple')
        ax3.set_xlabel('Minimale Dimension')
        ax3.set_ylabel('IMP Multiplikativ (%)')
        ax3.set_title('Sensitivität gegenüber Minimum')
        ax3.axhline(y=50, color='orange', linestyle='--', label='Schwelle 50%')
        ax3.legend()
        
        # 4. Boxplots der Dimensionen
        ax4 = plt.subplot(2, 3, 4)
        dim_cols = ['Autonomie', 'Motivation', 'Resilienz', 'Partizipation', 'Authentizität']
        self.results[dim_cols].boxplot(ax=ax4)
        ax4.set_ylabel('Score (1-7)')
        ax4.set_title('Dimensionsverteilungen')
        ax4.tick_params(axis='x', rotation=45)
        
        # 5. Differenzanalyse
        ax5 = plt.subplot(2, 3, 5)
        self.results['Differenz'].hist(bins=30, color='green', alpha=0.7, ax=ax5)
        ax5.set_xlabel('Differenz (Mult - Add normalized)')
        ax5.set_ylabel('Häufigkeit')
        ax5.set_title('Modelldifferenz')
        ax5.axvline(0, color='black', linestyle='--')
        
        # 6. 3D-Scatter (3 Dimensionen)
        ax6 = fig.add_subplot(2, 3, 6, projection='3d')
        scatter = ax6.scatter(self.results['Autonomie'], 
                              self.results['Motivation'], 
                              self.results['Resilienz'],
                              c=self.results['IMP_Multiplikativ'],
                              cmap='viridis', alpha=0.6)
        ax6.set_xlabel('Autonomie')
        ax6.set_ylabel('Motivation')
        ax6.set_zlabel('Resilienz')
        ax6.set_title('3D-Dimensionsraum')
        plt.colorbar(scatter, ax=ax6, label='IMP %')
        
        plt.tight_layout()
        plt.savefig('model_comparison_results.png', dpi=300)
        print("\n✅ Visualisierung gespeichert: model_comparison_results.png")
        plt.show()
    
    def sensitivity_analysis(self):
        """
        Analysiert Sensitivität des multiplikativen Modells
        """
        print("\n🔍 SENSITIVITÄTSANALYSE")
        print("="*50)
        
        # Teste verschiedene Szenarien
        scenarios = [
            ([7, 7, 7, 7, 7], "Perfekt"),
            ([7, 7, 7, 7, 1], "Eine Dimension schwach"),
            ([7, 7, 1, 1, 1], "Drei Dimensionen schwach"),
            ([5, 5, 5, 5, 5], "Durchschnitt"),
            ([3, 3, 3, 3, 3], "Niedrig")
        ]
        
        for dims, label in scenarios:
            dims_arr = np.array([dims])
            mult = self.calculate_imp_multiplicative(dims_arr)[0]
            add = self.calculate_imp_additive(dims_arr)[0]
            
            print(f"\n{label}: {dims}")
            print(f"  Multiplikativ: {mult:.1f}%")
            print(f"  Additiv: {add:.1f}")
            print(f"  Verhältnis: {mult / (add * 100 / 7):.2f}x")

def main():
    print("🎯 5D-MODELLVERGLEICH GESTARTET 🎯")
    print("="*60)
    
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
    results.to_csv('model_comparison_data.csv', index=False)
    print("\n✅ Daten exportiert: model_comparison_data.csv")
    
    # FAZIT
    print("\n" + "="*60)
    print("🏆 FAZIT")
    print("="*60)
    print("Das MULTIPLIKATIVE Modell ist überlegen, weil:")
    print("  1. Interdependenz: Alle Dimensionen müssen stark sein")
    print("  2. Realität: Eine schwache Dimension limitiert Gesamtpotential")
    print("  3. Nicht-Linearität: Resonanzeffekte werden berücksichtigt")
    print("\n⚠️  ABER: Erfordert Vermeidung von Null-Werten!")
    print("     Lösung: Mindestwert 1 (nicht 0) verwenden")
    
if __name__ == "__main__":
    main()
