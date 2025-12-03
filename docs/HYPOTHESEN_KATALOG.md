# Hypothesen-Katalog – 5D Intelligence Framework

**Status:** Living Document  
**Last Updated:** 2025-12-03  
**Purpose:** Testbare Hypothesen mit Operationalisierung, Methoden, Abbruchkriterien

---

## 📋 Übersicht

Dieser Katalog listet **alle testbaren Hypothesen** des 5D-Frameworks auf. Jede Hypothese ist:
- **Operationalisierbar:** Messbare Variablen definiert
- **Falsifizierbar:** Abbruchkriterien (wann ist Hypothese widerlegt?)
- **Priorisiert:** Hoch/Mittel/Niedrig (Impact × Feasibility)

---

## 🎯 Kern-Hypothesen (High Priority)

### **H1: IMP korreliert mit Life Satisfaction**
**Status:** ⚠️ Hypothese (Test Q2 2026)

**Behauptung:** IMP-Score (5 Dimensionen) korreliert mit subjektivem Wohlbefinden (r > 0.60)

**Operationalisierung:**
- **IV (Independent Variable):** IMP = f(A, IM, R, SP, Au)
- **DV (Dependent Variable):** SWLS (Satisfaction With Life Scale, 5 items)
- **Messung:** Likert 1-5, Self-Report Survey

**Methode:**
- Design: Cross-sectional survey (n > 400)
- Analyse: Pearson r, 95% CI, Bootstrap
- Kontrollen: Age, Gender, Income, Culture (C-Faktor)

**Erfolgs-Kriterium:**
- r > 0.60 (stark), p < 0.001 → Hypothese bestätigt ✅
- 0.40 < r < 0.60 (mittel) → Teilweise bestätigt ⚠️
- r < 0.40 (schwach), p > 0.05 → Hypothese falsifiziert ❌

**Abbruchkriterium:**
- Falls r < 0.30 (n > 100) → IMP-Formel überarbeiten
- Falls Kultur-Moderator massiv (ΔC > 0.50) → Dimension A überdenken

**Timeline:** Q2 2026 (Apr-Jun)  
**Ressourcen:** Survey via Prolific/MTurk, n=400 ($2000 budget)

---

### **H2: A, IM, R, SP, Au sind distinkte Dimensionen**
**Status:** ⚠️ Hypothese (Test Q2 2026)

**Behauptung:** 5 Dimensionen sind statistisch unabhängig (Faktorenanalyse)

**Operationalisierung:**
- **Methode:** Exploratory Factor Analysis (EFA) oder Confirmatory Factor Analysis (CFA)
- **Kriterien:**
  - 5 Faktoren mit Eigenwert > 1.0
  - Cronbach's α > 0.70 pro Dimension (interne Konsistenz)
  - Inter-Faktor Korrelation < 0.70 (Distinktheit)
  - Model Fit: CFI > 0.95, RMSEA < 0.06

**Erfolgs-Kriterium:**
- Alle Kriterien erfüllt → Hypothese bestätigt ✅
- 3-4 Kriterien erfüllt → Teilweise bestätigt ⚠️
- < 3 Kriterien erfüllt → Hypothese falsifiziert ❌

**Abbruchkriterium:**
- Falls nur 3 Faktoren (A+IM zusammen, R+SP zusammen) → Auf 3D-Modell reduzieren
- Falls α < 0.60 für >2 Dimensionen → Items überarbeiten

**Timeline:** Q2 2026 (nach Survey)  
**Ressourcen:** R/SPSS, Statistik-Expertise

---

### **H3: Alternative Schulen haben höhere IMP-Scores**
**Status:** ⚠️ Hypothese (Test Q3 2026)

**Behauptung:** Sudbury/Folk HS/Tokkatsu > Mainstream Schools (d > 0.50)

**Operationalisierung:**
- **Gruppen:** Alternative (n > 15 Schulen) vs. Mainstream (n > 15 Schulen)
- **Messung:** IMP-Score (Survey Schüler + Lehrer)
- **Kontrollen:** SES (Socioeconomic Status), Schultyp, Land

**Methode:**
- Design: Quasi-experimental, matched samples
- Analyse: Independent t-test, Cohen's d, ANCOVA (SES als Covariate)

**Erfolgs-Kriterium:**
- d > 0.80 (groß), p < 0.01 → Hypothese stark bestätigt ✅
- 0.50 < d < 0.80 (mittel), p < 0.05 → Bestätigt ✅
- 0.20 < d < 0.50 (klein) → Schwach bestätigt ⚠️
- d < 0.20, p > 0.05 → Hypothese falsifiziert ❌

**Abbruchkriterium:**
- Falls d < 0.20 nach SES-Kontrolle → Selection Bias dominant (Hypothese gescheitert)
- Falls Alternative Schulen lower IMP → Fundamentale Revision nötig

**Timeline:** Q3 2026 (Jul-Sep)  
**Ressourcen:** Schulkontakte, Interview-Kapazität

---

### **H4: IMP-Formel (Multiplikativ vs. Additiv)**
**Status:** ⚠️ Hypothese (Test Q2 2026)

**Behauptung:** Multiplikativ IMP erklärt Wohlbefinden besser als Additiv

**Operationalisierung:**
- **Modell 1 (Multiplikativ):** IMP = A × IM × R × SP × Au
- **Modell 2 (Additiv):** IMP = (A + IM + R + SP + Au) / 5
- **Modell 3 (Geometric Mean):** IMP = (A × IM × R × SP × Au)^(1/5)
- **Modell 4 (Weighted Additive):** IMP = 0.30A + 0.25IM + 0.20R + 0.15SP + 0.10Au

**Methode:**
- Vergleich: R², AIC, BIC, Cross-Validation
- Pre-Registration: OSF (Q1 2026)

**Erfolgs-Kriterium:**
- **Multiplikativ gewinnt:** ΔR² > 0.05, ΔAIC > 10 → Hypothese bestätigt ✅
- **Geometric Mean gewinnt:** Kompromiss → Formel anpassen ⚠️
- **Additiv gewinnt:** ΔR² > 0.05 → Hypothese falsifiziert ❌

**Abbruchkriterium:**
- Falls Additiv signifikant besser (p < 0.01) → IMP-Formel auf Additiv umstellen
- Falls alle 4 Modelle ähnlich (ΔR² < 0.02) → Einfachstes Modell wählen (Additiv)

**Timeline:** Q2 2026  
**Ressourcen:** R-Script, Pre-Registration

---

### **H5: Zwanglosigkeit führt zu höherer Diversität**
**Status:** ✅ Teilweise bestätigt (GoL Experiment 2025-12-03)

**Behauptung:** Nicht-koerzitive Initialisierung → höhere Musterdiversität

**Operationalisierung:**
- **Koerzitiv:** Fixed Glider (deterministisch)
- **Nicht-koerzitiv:** Random initialization (stochastisch)
- **Messung:** Shannon-Entropie H (Diversität), Generationen (Lebensdauer)

**Resultate (GoL Experiment):**
- **Diversität:** H_random = 0.56 vs H_glider = 0.10 (5.7× höher, p<0.001) ✅
- **Lebensdauer:** Gen_random = 149 vs Gen_glider = 200 (25% kürzer, p<0.001) ❌

**Interpretation:**
- ✅ Zwanglosigkeit → höhere Diversität (bestätigt)
- ❌ Zwanglosigkeit → längere Lebensdauer (falsifiziert)
- ⚠️ Trade-Off: Diversität vs. Stabilität (nicht vorhersehbar)

**Lesson:** Zwanglosigkeit ≠ automatische Resilienz, braucht **emergente Struktur** (Ostrom)

---

## 🌍 Kontext-Hypothesen (Medium Priority)

### **H6: SDT-Effekt ist kulturabhängig**
**Status:** ✅ Bestätigt (Church 2013, n=7248)

**Behauptung:** Autonomie → IM Effekt ist schwächer in kollektivistischen Kulturen

**Evidenz:**
- **WEIRD:** r = 0.35-0.50 (Deci & Ryan 1985, USA/Europa)
- **Kollektivismus:** r = 0.22-0.30 (Church 2013, Asien/LatAm)
- **Differenz:** Δr = 0.13 (37% schwächer)

**Implikation:**
- IMP-Formel braucht **Kultur-Moderator (C-Faktor)**
- Dimension A muss erweitert werden: Independence + Relational Autonomy

**Status:** ✅ Fakt (1000+ Studien, repliziert)

---

### **H7: Perry Preschool ROI ist nicht skalierbar**
**Status:** ⚠️ Hypothese (kritisch evaluiert)

**Behauptung:** Head Start (n=5000) zeigt Fade-Out, Perry ROI $7.16 → $2-4 realistisch

**Evidenz:**
- **Perry:** $7.16 per dollar (Schweinhart 2005, n=123, intensive intervention)
- **Head Start:** Fade-Out nach Klasse 3 (Puma 2012, n=5000)
- **Meta-Analyse:** 78% Early Intervention zeigen Fade-Out (Duncan 2013)

**Realistische Schätzung:**
- **Best Case:** $4-7 (intensive, gut-finanziert, n<200)
- **Realistic:** $2-4 (skaliert, n>1000, normale Ressourcen)
- **Worst Case:** $0-2 (Fade-Out, keine Langzeiteffekte)

**Status:** ⚠️ Teilweise falsifiziert (Perry nicht replizierbar at scale)

---

### **H8: Interaktionen sind instabil**
**Status:** ✅ Bestätigt (Aguinis 2005, k=127 Meta)

**Behauptung:** Interaktionseffekte haben niedrige Test-Retest Reliability

**Evidenz:**
- **Main Effects:** r = 0.72 (retest), 60% replicate (OSC 2015)
- **Interactions:** r = 0.38 (retest), 20% replicate (OSC 2015)
- **Average ΔR²:** 0.009 (0.9%, Aguinis 2005)

**Implikation:**
- Multiplikative IMP-Formel ist **riskant** (Noise > Signal)
- Need n > 400 für 80% Power (McClelland 1993)

**Status:** ✅ Fakt (Meta k=127 Studien)

---

## 🧠 Neurobiologie-Hypothesen (Low Priority, Spekulativ)

### **H9: Perkolationstheorie erklärt Bewusstsein**
**Status:** 🔮 Spekulation (teilweise externally supported)

**Behauptung:** Giant Component im Connectome = neurales Korrelat von Bewusstsein

**Evidenz:**
- **Perkolationstheorie:** Erdős & Rényi 1960 (6000+ Zit., etabliert)
- **Anwendung auf Gehirn:** Tagliazucchi & Chialvo 2016 (220 Zit., "Unbewusstsein = Abweichung von kritisch")
- **Problem:** Kein direkter Test auf Bewusstsein (nur Anästhesie, Schlaf)

**Testbarkeit:**
- EEG/fMRI: Konnektivität während Wachheit vs. Anästhesie
- Graph-Metriken: Giant Component Size, Clustering, Path Length
- Erwartung: Wachheit → höhere Konnektivität, größere Giant Component

**Status:** 🔮 Spekulation (plausibel, aber nicht getestet in 5D-Framework)

---

### **H10: DMN-Aktivität korreliert mit Authentizität**
**Status:** 🔮 Spekulation

**Behauptung:** Default Mode Network = Selbst-Referenz → höhere Au-Scores

**Operationalisierung:**
- **fMRI:** DMN activation during self-reflection tasks
- **Survey:** Authenticity Scale (5 items)
- **Erwartung:** r > 0.40 (DMN activation vs. Au)

**Problem:** Kostspielig (fMRI €500-1000 per scan), n > 30 nötig

**Timeline:** Q4 2026+ (Funding nötig)

---

## 📊 Prioritätsmatrix

| Hypothese | Impact | Feasibility | Priority | Timeline |
|-----------|--------|-------------|----------|----------|
| **H1 (IMP ↔ Life Sat)** | Hoch | Hoch | ⭐⭐⭐ | Q2 2026 |
| **H2 (5 Dimensionen distinkt)** | Hoch | Hoch | ⭐⭐⭐ | Q2 2026 |
| **H3 (Alternative Schulen)** | Hoch | Mittel | ⭐⭐ | Q3 2026 |
| **H4 (Multiplikativ vs. Additiv)** | Hoch | Hoch | ⭐⭐⭐ | Q2 2026 |
| **H5 (Zwanglosigkeit → Diversität)** | Mittel | Hoch | ⭐⭐ | ✅ Done |
| **H6 (SDT kulturabhängig)** | Hoch | N/A | ✅ Bestätigt | Done |
| **H7 (Perry ROI nicht skalierbar)** | Mittel | Mittel | ⭐ | Q3 2026 |
| **H8 (Interaktionen instabil)** | Mittel | N/A | ✅ Bestätigt | Done |
| **H9 (Perkolation → Bewusstsein)** | Niedrig | Niedrig | 🔮 | Q4 2026+ |
| **H10 (DMN → Authentizität)** | Niedrig | Niedrig | 🔮 | Q4 2026+ |

---

## 🚨 Abbruchkriterien (Gesamt)

**Framework muss fundamental überarbeitet werden, falls:**

1. **H1 falsifiziert:** IMP r < 0.30 (n > 100) → Formel ungültig
2. **H2 falsifiziert:** Nur 3 Faktoren (nicht 5) → Auf 3D-Modell reduzieren
3. **H3 falsifiziert:** Alternative Schulen NICHT höher IMP → Hypothese gescheitert
4. **H4 falsifiziert:** Additiv signifikant besser (ΔR² > 5%) → Formel umstellen
5. **3+ Kern-Hypothesen falsifiziert** → Neukonzeption Q2 2026

**Transparenz:** Alle Abbruchkriterien sind **vor** Datensammlung definiert (kein p-Hacking).

---

## 📚 Siehe auch

- **[CLAIMS_EVIDENCE_MATRIX.md](CLAIMS_EVIDENCE_MATRIX.md)** – 40 Behauptungen mit Evidenzlabels
- **[ETHIK_MANIFEST.md](../ETHIK_MANIFEST.md)** – Bias-Log, Forschungsethik
- **[TODO_RESEARCH.md](../TODO_RESEARCH.md)** – Forschungs-Roadmap (85+ Tasks)
- **[VISION.md](../VISION.md)** – Zentrale Definition, 1D-5D Definitionen

---

**Last Updated:** 2025-12-03  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License:** CC BY 4.0
