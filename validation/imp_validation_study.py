#!/usr/bin/env python3
"""
5D-Intelligence Framework - IMP Validation Study
================================================
Akademische Validierungsstudie für das 5D-Framework
Basierend auf der Analyse vom 04.12.2025

Autor: karlitos1337
Ziel: Empirische Validierung der 5 Dimensionen mit 30+ Probanden
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Fragebogen-Definitionen
QUESTIONS = {
    "Autonomie": [
        "Ich treffe meine eigenen Entscheidungen frei und unabhängig.",
        "Ich habe Kontrolle über wichtige Aspekte meines Lebens.",
        "Ich handle nach meinen eigenen Überzeugungen.",
        "Ich fühle mich in meinen Entscheidungen selbstbestimmt.",
        "Externe Zwänge beeinflussen mich kaum."
    ],
    "Intrinsische_Motivation": [
        "Ich erlebe häufig Flow-Zustände bei meinen Tätigkeiten.",
        "Ich bin innerlich motiviert, meine Ziele zu erreichen.",
        "Ich tue Dinge aus innerem Antrieb, nicht für Belohnungen.",
        "Meine Arbeit erfüllt mich von innen heraus.",
        "Ich vergesse die Zeit, wenn ich meinen Interessen nachgehe."
    ],
    "Resilienz": [
        "Ich erhole mich schnell von Rückschlägen.",
        "Schwierigkeiten bringen mich nicht aus der Bahn.",
        "Ich passe mich flexibel an Veränderungen an.",
        "Ich sehe Herausforderungen als Chancen.",
        "Stress bewältige ich konstruktiv."
    ],
    "Soziale_Partizipation": [
        "Ich engagiere mich aktiv in meiner Gemeinschaft.",
        "Ich trage zur Gesellschaft bei.",
        "Ich fühle mich als Teil einer größeren Gemeinschaft.",
        "Ich nehme regelmäßig an sozialen Aktivitäten teil.",
        "Meine Meinung wird in meinem Umfeld gehört."
    ],
    "Authentizität": [
        "Ich zeige mich anderen gegenüber so, wie ich wirklich bin.",
        "Ich handle im Einklang mit meinen Werten.",
        "Ich verstelle mich nicht, um anderen zu gefallen.",
        "Ich bin ehrlich zu mir selbst.",
        "Ich akzeptiere mich mit meinen Stärken und Schwächen."
    ]
}

class IMPValidationStudy:
    """Haupt-Klasse für die IMP-Validierungsstudie"""
    
    def __init__(self):
        self.data = None
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate_questionnaire(self, output_format='json'):
        """Generiert den Fragebogen"""
        questionnaire = []
        q_id = 1
        
        for dimension, questions in QUESTIONS.items():
            for question in questions:
                questionnaire.append({
                    "id": q_id,
                    "dimension": dimension,
                    "question": question,
                    "scale": "1 (stimme gar nicht zu) - 7 (stimme voll zu)"
                })
                q_id += 1
        
        if output_format == 'json':
            filename = f'questionnaire_{self.timestamp}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(questionnaire, f, ensure_ascii=False, indent=2)
            print(f"✅ Fragebogen gespeichert: {filename}")
        
        return questionnaire
    
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
        
        # Cronbach's Alpha
        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
        
        return alpha
    
    def load_responses(self, filename):
        """Lädt Probandendaten aus CSV"""
        self.data = pd.read_csv(filename)
        print(f"✅ {len(self.data)} Antworten geladen")
        return self.data
    
    def analyze_dimensions(self):
        """Analysiert alle 5 Dimensionen"""
        if self.data is None:
            print("❌ Keine Daten geladen. Bitte load_responses() aufrufen.")
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
                "interpretation": self._interpret_alpha(alpha)
            }
            
            print(f"\n{dim}:")
            print(f"  Cronbach's α: {alpha:.3f} - {self._interpret_alpha(alpha)}")
            print(f"  Mittelwert: {mean_score:.2f} (±{std_score:.2f})")
        
        return self.results
    
    def _interpret_alpha(self, alpha):
        """Interpretiert Cronbach's Alpha"""
        if alpha >= 0.9:
            return "Exzellent"
        elif alpha >= 0.8:
            return "Gut"
        elif alpha >= 0.7:
            return "Akzeptabel"
        elif alpha >= 0.6:
            return "Fragwürdig"
        else:
            return "Inakzeptabel"
    
    def calculate_imp_score(self, row):
        """Berechnet IMP-Score für einen Probanden"""
        dimensions = list(QUESTIONS.keys())
        scores = {}
        
        for dim in dimensions:
            dim_cols = [col for col in row.index if col.startswith(dim)]
            scores[dim] = row[dim_cols].mean()
        
        # Multiplikatives Modell: IMP = A × IM × R × SP × Au
        imp_multiplicative = 1.0
        for score in scores.values():
            imp_multiplicative *= (score / 7.0)  # Normalisiert auf [0,1]
        
        # Additives Modell (zum Vergleich)
        imp_additive = sum(scores.values()) / len(scores)
        
        return {
            "dimensions": scores,
            "IMP_multiplicative": imp_multiplicative * 100,  # in %
            "IMP_additive": imp_additive
        }
    
    def correlation_analysis(self):
        """Korrelationsanalyse zwischen Dimensionen"""
        dimensions = list(QUESTIONS.keys())
        dim_means = {}
        
        for dim in dimensions:
            dim_cols = [col for col in self.data.columns if col.startswith(dim)]
            dim_means[dim] = self.data[dim_cols].mean(axis=1)
        
        corr_df = pd.DataFrame(dim_means)
        correlation_matrix = corr_df.corr()
        
        print("\n=== KORRELATIONSMATRIX ===")
        print(correlation_matrix.round(3))
        
        return correlation_matrix
    
    def visualize_results(self):
        """Erstellt Visualisierungen"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Cronbach's Alpha Balkendiagramm
        alphas = [self.results[dim]['cronbach_alpha'] for dim in QUESTIONS.keys()]
        axes[0, 0].barh(list(QUESTIONS.keys()), alphas, color='skyblue')
        axes[0, 0].axvline(x=0.7, color='red', linestyle='--', label='Akzeptabel-Schwelle')
        axes[0, 0].set_xlabel('Cronbach\'s Alpha')
        axes[0, 0].set_title('Reliabilität der Dimensionen')
        axes[0, 0].legend()
        
        # 2. Mittelwerte der Dimensionen
        means = [self.results[dim]['mean'] for dim in QUESTIONS.keys()]
        axes[0, 1].bar(list(QUESTIONS.keys()), means, color='lightgreen')
        axes[0, 1].set_ylabel('Mittelwert (1-7)')
        axes[0, 1].set_title('Durchschnittliche Bewertungen')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Korrelations-Heatmap
        corr_matrix = self.correlation_analysis()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[1, 0])
        axes[1, 0].set_title('Korrelationen zwischen Dimensionen')
        
        # 4. IMP-Score Verteilung
        imp_scores = []
        for idx in range(len(self.data)):
            imp_score = self.calculate_imp_score(self.data.iloc[idx])
            imp_scores.append(imp_score['IMP_multiplicative'])
        
        axes[1, 1].hist(imp_scores, bins=15, color='purple', alpha=0.7, edgecolor='black')
        axes[1, 1].set_xlabel('IMP-Score (%)')
        axes[1, 1].set_ylabel('Häufigkeit')
        axes[1, 1].set_title('Verteilung der IMP-Scores (Multiplikativ)')
        axes[1, 1].axvline(x=np.mean(imp_scores), color='red', linestyle='--', label=f'Mittelwert: {np.mean(imp_scores):.1f}%')
        axes[1, 1].legend()
        
        plt.tight_layout()
        filename = f'validation_results_{self.timestamp}.png'
        plt.savefig(filename, dpi=300)
        print(f"\n✅ Visualisierung gespeichert: {filename}")
        plt.show()
    
    def generate_report(self):
        """Generiert Abschlussbericht"""
        report = {
            "timestamp": self.timestamp,
            "n_participants": len(self.data) if self.data is not None else 0,
            "dimensions": self.results,
            "overall_reliability": np.mean([r['cronbach_alpha'] for r in self.results.values()]),
            "recommendation": self._generate_recommendation()
        }
        
        filename = f'validation_report_{self.timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Bericht gespeichert: {filename}")
        return report
    
    def _generate_recommendation(self):
        """Generiert Empfehlungen basierend auf Ergebnissen"""
        avg_alpha = np.mean([r['cronbach_alpha'] for r in self.results.values()])
        
        if avg_alpha >= 0.8:
            return "Das 5D-Framework zeigt gute bis exzellente Reliabilität. Bereit für Preprint-Publikation."
        elif avg_alpha >= 0.7:
            return "Das Framework ist akzeptabel, aber Verbesserung einzelner Items empfohlen."
        else:
            return "Reliabilität unter Schwelle. Items müssen überarbeitet werden."

# MAIN EXECUTION
def main():
    print("⚡ 5D-IMP VALIDIERUNGSSTUDIE GESTARTET \u26a1")
    print("="*50)
    
    study = IMPValidationStudy()
    
    # 1. Fragebogen generieren
    print("\n[1/5] Generiere Fragebogen...")
    questionnaire = study.generate_questionnaire()
    print(f"    → {len(questionnaire)} Fragen erstellt")
    
    # 2. Beispiel-Daten generieren (für Demo - später durch echte Daten ersetzen)
    print("\n[2/5] Generiere Beispiel-Daten (30 Probanden)...")
    np.random.seed(42)
    example_data = {}
    
    for dimension, questions in QUESTIONS.items():
        for i, question in enumerate(questions, 1):
            col_name = f"{dimension}_{i}"
            # Simuliere Antworten zwischen 4-7 (tendenziell positiv)
            example_data[col_name] = np.random.randint(4, 8, size=30)
    
    df = pd.DataFrame(example_data)
    df.to_csv(f'example_responses_{study.timestamp}.csv', index=False)
    print("    → Beispiel-CSV erstellt")
    
    # 3. Daten laden
    print("\n[3/5] Lade Daten...")
    study.load_responses(f'example_responses_{study.timestamp}.csv')
    
    # 4. Analyse durchführen
    print("\n[4/5] Führe Dimensionsanalyse durch...")
    print("="*50)
    study.analyze_dimensions()
    
    # 5. Visualisierungen und Bericht
    print("\n[5/5] Erstelle Visualisierungen und Bericht...")
    study.visualize_results()
    report = study.generate_report()
    
    print("\n" + "="*50)
    print("✅ VALIDIERUNGSSTUDIE ABGESCHLOSSEN!")
    print(f"\nEMPFEHLUNG: {report['recommendation']}")
    print(f"Durchschnittliche Reliabilität (α): {report['overall_reliability']:.3f}")
    print("\nNÄCHSTE SCHRITTE:")
    print("  1. Echte Probanden rekrutieren (Ziel: 30+)")
    print("  2. Fragebogen online stellen (z.B. Google Forms, LimeSurvey)")
    print("  3. Daten sammeln und in CSV exportieren")
    print("  4. Dieses Skript erneut mit echten Daten ausführen")
    print("  5. Ergebnisse in Preprint-Paper integrieren")

if __name__ == "__main__":
    main()
