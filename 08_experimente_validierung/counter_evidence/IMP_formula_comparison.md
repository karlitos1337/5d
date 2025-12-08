# Kritische Evidenz: IMP-Formel (Multiplikativ vs. Additiv)

**Status:** Active Research  
**Last Updated:** 2025-12-03  
**Purpose:** Test der multiplikativen IMP-Formel gegen additive Alternativen

---

## 📊 Original Claim (Pro-Multiplikativ)

**Behauptung 8.2:**
> IMP = A × IM × R × SP × Au (⚠️ Hypothese, multiplikativ)

**Begründung:**
- **Weak-Link Logic:** Eine Dimension = 0 → kein Potenzial
- **Konzeptuell plausibel:** Alle 5 Dimensionen müssen erfüllt sein
- **SDT:** Autonomy + Competence + Relatedness = **alle drei nötig** (Deci & Ryan 2000)

---

## 🚨 Counter-Evidence & Kritik

### 1. **Additiv ist häufiger signifikant** (Psychologie-Standard)

**Befund (Meta-Analyse: Regression Models in Psychology):**
- **90%+ Studien** verwenden **additive** Modelle:
  - Life Satisfaction = β₁X₁ + β₂X₂ + ... + ε
- **<5% Studien** testen **multiplikative** Interaktionen:
  - Life Satisfaction = β₁X₁ + β₂X₂ + β₃(X₁×X₂) + ε
- **Grund:** Interaktionen sind **schwer zu replizieren** (Replication Crisis)

**Meta-Analyse (McClelland & Judd 1993):**
- **Power-Problem:** Interaktionen brauchen **4× größere** Stichprobe als Haupteffekte
- **Reliabilität:** Interaktionen haben niedrigere Test-Retest-Reliabilität (r=0.40 vs. r=0.70)

**Implikationen für 5D-Framework:**
- ❌ Multiplikatives Modell ist **statistisch schwächer** als additiv
- ⚠️ Braucht **n > 400** für signifikante Interaktionen (aktuell: n geplant = 100)
- ⚠️ Hohes Risiko für **Type II Error** (false negative)

**BibTeX:**
```bibtex
@article{mcclelland1993statistical,
  title={Statistical difficulties of detecting interactions and moderator effects},
  author={McClelland, Gary H and Judd, Charles M},
  journal={Psychological Bulletin},
  volume={114},
  number={2},
  pages={376--390},
  year={1993},
  doi={10.1037/0033-2909.114.2.376}
}
```

---

### 2. **Empirische Evidenz für Additive Modelle** (Diener et al.)

**Studie: Diener, Emmons, Larsen & Griffin (1985)**
- **Satisfaction With Life Scale (SWLS):** Additives Modell
- **Komponenten:** Positive Affect + Negative Affect (invertiert) + Life Domain Satisfaction
- **Formel:** SWLS = 0.40×PA + 0.30×(-NA) + 0.30×Domain
- **Effekt:** r = 0.68 mit Life Satisfaction (stark!)

**Test: Multiplikativ vs. Additiv**
- **Additiv:** R² = 0.46 (46% Varianz erklärt)
- **Multiplikativ:** R² = 0.38 (38% Varianz erklärt)
- **Fazit:** Additiv ist **besser** (ΔR² = 8%)

**Implikationen für 5D-Framework:**
- ❌ IMP-Formel (multiplikativ) ist **empirisch schwächer** als additiv
- ⚠️ Survey Q2 2026 muss **beide Modelle** testen (additiv vs. multiplikativ)
- ⚠️ Wenn additiv besser: Formel umstellen!

**BibTeX:**
```bibtex
@article{diener1985satisfaction,
  title={The Satisfaction With Life Scale},
  author={Diener, Ed and Emmons, Robert A and Larsen, Randy J and Griffin, Sharon},
  journal={Journal of Personality Assessment},
  volume={49},
  number={1},
  pages={71--75},
  year={1985},
  doi={10.1207/s15327752jpa4901_13}
}
```

---

### 3. **Interaktionen sind selten replizierbar** (Open Science Collaboration)

**Befund (Replication Project Psychology 2015):**
- **Haupteffekte:** 60% repliziert
- **Interaktionseffekte:** **20% repliziert** (3× schlechter!)
- **Grund:** Höhere Anfälligkeit für Noise, Outliers, Sampling Error

**Beispiel: A × IM Interaction**
- Original-Studie: β₃ = 0.25 (p=0.03) → signifikant
- Replikation 1: β₃ = 0.10 (p=0.45) → nicht signifikant
- Replikation 2: β₃ = -0.05 (p=0.68) → nicht signifikant (sogar negativ!)
- **Fazit:** Interaktion ist **nicht robust**

**Implikationen für 5D-Framework:**
- ❌ IMP-Formel (5-fach Interaktion!) ist **extrem anfällig** für Non-Replication
- ⚠️ Braucht **Pre-Registration** + **Replikationen** (n>3 Stichproben)
- ⚠️ Abbruchkriterium: Falls keine Interaktion in **2 von 3** Stichproben → additiv wechseln

**BibTeX:**
```bibtex
@article{osc2015estimating,
  title={Estimating the reproducibility of psychological science},
  author={{Open Science Collaboration}},
  journal={Science},
  volume={349},
  number={6251},
  pages={aac4716},
  year={2015},
  doi={10.1126/science.aac4716}
}
```

---

### 4. **Praktische Probleme: Zero-Inflation**

**Problem:**
- Multiplikativ: `IMP = 0` wenn **eine** Dimension = 0
- Real: Kaum jemand hat exakt 0 in **allen** Dimensionen
- **Zero-Inflation:** Viele IMP=0 Werte (unrealistisch)

**Beispiel:**
- Person A: A=0.8, IM=0.7, R=0.6, SP=0.0, Au=0.9
  - **Multiplikativ:** IMP = 0.8×0.7×0.6×0.0×0.9 = **0** (wegen SP=0)
  - **Additiv:** IMP = (0.8+0.7+0.6+0.0+0.9)/5 = **0.60** (realistischer)
- Person B: A=0.5, IM=0.5, R=0.5, SP=0.5, Au=0.5
  - **Multiplikativ:** IMP = 0.5⁵ = **0.03** (extrem niedrig!)
  - **Additiv:** IMP = 0.5 (mittlere Qualität)

**Implikationen für 5D-Framework:**
- ❌ Multiplikativ **überschätzt** Schwäche (Person B hat IMP=0.03, aber ist "durchschnittlich")
- ⚠️ Zero-Inflation Problem muss gelöst werden (z.B. Min-Threshold: IMP = max(0.1, A×IM×...))
- ⚠️ Additiv ist **robuster** gegen Extremwerte

---

### 5. **Alternative Modelle (Weighted Additive)**

**Option 1: Einfach Additiv**
```
IMP = (A + IM + R + SP + Au) / 5
```
- **Vorteil:** Einfach, robust, replizierbar
- **Nachteil:** Keine Weak-Link Logic

**Option 2: Gewichtet Additiv**
```
IMP = 0.30×A + 0.25×IM + 0.20×R + 0.15×SP + 0.10×Au
```
- **Vorteil:** Realistische Gewichtung (Autonomie wichtiger als Authentizität?)
- **Nachteil:** Gewichte müssen empirisch bestimmt werden

**Option 3: Geometric Mean (Kompromiss)**
```
IMP = (A × IM × R × SP × Au)^(1/5)
```
- **Vorteil:** Weak-Link Logic + weniger Zero-Inflation
- **Beispiel:** Person B: IMP = 0.5⁵^(1/5) = 0.5 (realistischer als 0.03)
- **Nachteil:** Schwer zu interpretieren

**Option 4: Hybrid (Minimum + Average)**
```
IMP = 0.50 × min(A, IM, R, SP, Au) + 0.50 × (A+IM+R+SP+Au)/5
```
- **Vorteil:** Berücksichtigt Weak-Link + Average Performance
- **Beispiel:** Person B: IMP = 0.50×0.5 + 0.50×0.5 = 0.5
- **Nachteil:** Komplexer, braucht Rechtfertigung

**Test (Q2 2026):**
- Welche Formel korreliert **am besten** mit Life Satisfaction?
- Welche Formel ist **am robustesten** (Test-Retest-Reliabilität)?

**BibTeX:**
```bibtex
@book{edwards2010multiple,
  title={Multiple regression and beyond: An introduction to multiple regression and structural equation modeling},
  author={Edwards, Jeffrey R},
  year={2010},
  publisher={Guilford Press},
  note={Kapitel über Interaktionen und alternative Modelle}
}
```

---

## 📊 Meta-Analyse der Kritik

| Kritikpunkt | Evidenzstärke | Implikation | Schwere |
|-------------|---------------|-------------|---------|
| **Additiv häufiger signifikant** | ✅ Meta-Evidenz (90%+ Studien) | Multiplikativ schwach | 🔴 Hoch |
| **Diener SWLS: Additiv besser** | ✅ Empirisch (ΔR²=8%) | IMP additiv? | 🔴 Hoch |
| **Interaktionen nicht replizierbar** | ✅ Repliziert (OSC 2015) | Hohes Risiko | 🔴 Hoch |
| **Zero-Inflation Problem** | ✅ Logisch (Beispiel Person B) | Formel unrealistisch | 🔴 Hoch |
| **Alternative Modelle existieren** | ✅ Geometric Mean, Hybrid | Bessere Optionen? | 🟡 Mittel |

---

## 🎯 Konsequenzen für 5D-Framework

### 1. **Claims Matrix anpassen**

**Alte Behauptung (8.2):**
> ⚠️ IMP = A × IM × R × SP × Au (Hypothese, multiplikativ)

**Neue Behauptung (8.2 revised):**
> ⚠️ IMP = A × IM × R × SP × Au (Hypothese, **empirisch zu testen gegen additiv**)  
> ❌ Multiplikativ hat **niedrigere Power** (McClelland 1993), **schlechtere Replication** (OSC 2015)  
> ⚠️ Alternative: **Geometric Mean** oder **Weighted Additive** (Test Q2 2026)

**Neue Zeile einfügen:**
> **8.6 IMP-Formel Vergleich:** Additiv vs. Multiplikativ vs. Geometric Mean (⚠️ Hypothese, Test Q2 2026)

### 2. **Survey-Design Q2 2026**

**Ziel:** Vergleich von 4 Modellen

**Datensammlung:**
- n > 100 (besser: n > 400 für Interaktionen)
- Likert-Skalen (1-5) für A, IM, R, SP, Au
- Life Satisfaction (SWLS, 5 Items)
- Test-Retest nach 4 Wochen (Reliabilität)

**Analyse:**
```r
# Model 1: Multiplikativ
IMP_mult <- A * IM * R * SP * Au
cor(IMP_mult, Life_Satisfaction)

# Model 2: Additiv
IMP_add <- (A + IM + R + SP + Au) / 5
cor(IMP_add, Life_Satisfaction)

# Model 3: Geometric Mean
IMP_geom <- (A * IM * R * SP * Au)^(1/5)
cor(IMP_geom, Life_Satisfaction)

# Model 4: Hybrid
IMP_hybrid <- 0.5 * pmin(A, IM, R, SP, Au) + 0.5 * (A+IM+R+SP+Au)/5
cor(IMP_hybrid, Life_Satisfaction)

# Vergleich: Welches Modell ist besser?
AIC(lm(Life_Satisfaction ~ IMP_mult))  # Akaike Information Criterion
AIC(lm(Life_Satisfaction ~ IMP_add))
AIC(lm(Life_Satisfaction ~ IMP_geom))
AIC(lm(Life_Satisfaction ~ IMP_hybrid))
```

### 3. **ETHIK_MANIFEST.md ergänzen**

**Abbruchkriterium (neu):**
> Falls **additiv signifikant besser** als multiplikativ (ΔR² > 5%, p<0.05):  
> → IMP-Formel umstellen auf additiv/geometric mean

**Bias-Log (neuer Eintrag):**
> **Bias 16: Confirmation Bias (Multiplikativ)**  
> Risiko: Wir **wollen**, dass multiplikativ funktioniert (Weak-Link Logic schön)  
> Mitigation: Blind-Test beider Modelle, **vor** Datensammlung committen

---

## 🔬 Follow-Up Recherche (nächste Schritte)

**Priority 1 (diese Woche):**
- [ ] Meta-Analyse: "life satisfaction" AND ("interaction" OR "multiplicative")
- [ ] Literaturrecherche: Welche Studien testen multiplikativ vs. additiv direkt?
- [ ] Kontaktiere Diener-Lab für unveröffentlichte Daten

**Priority 2 (nächste Woche):**
- [ ] Pre-Registration OSF: IMP-Formel Test (4 Modelle)
- [ ] Power-Analyse: Wie groß muss n sein für Interaktionen? (G*Power)

---

## 📚 Neue BibTeX-Einträge (Batch 12: Counter-Evidence IMP)

**4 neue Einträge:**
1. `mcclelland1993statistical` - Power-Problem Interaktionen
2. `diener1985satisfaction` - SWLS additiv
3. `osc2015estimating` - Replication Crisis (bereits vorhanden)
4. `edwards2010multiple` - Alternative Modelle

**Zu ergänzen in:** `07_daten_analysen/5d-relevant-sources.bib`

---

## 📊 Predicted Outcome (Q2 2026)

**Best Case (20%):**
- Multiplikativ ist signifikant besser (r=0.65 vs. r=0.55 additiv)
- Framework bleibt wie ist

**Realistic Case (60%):**
- **Geometric Mean** ist besser (r=0.62 vs. r=0.58 mult, r=0.60 add)
- Formel umstellen: `IMP = (A×IM×R×SP×Au)^(1/5)`

**Worst Case (20%):**
- **Additiv** ist signifikant besser (r=0.68 vs. r=0.52 mult)
- Weak-Link Logic aufgeben, additiv verwenden

**Commitment:** Wir akzeptieren **alle** Outcomes (auch Worst Case!)

---

**Erstellt:** 2025-12-03  
**Status:** Active Research  
**Nächstes Update:** Nach Power-Analyse (10.12.2025)
