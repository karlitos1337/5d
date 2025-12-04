# 🔬 5D-Framework: Validierung & Simulation

## Übersicht

Dieser Ordner enthält alle Tools zur **empirischen Validierung** des 5D-Intelligence-Frameworks.

**Erstellt**: 04./05.12.2025  
**Status**: ✅ Prototyp fertig | 🔄 Datensammlung ausstehend

---

## 📁 Dateien

### 1. `imp_validation_study.py`
**Zweck**: Hauptskript für IMP-Validierungsstudie  
**Features**:
- ✅ Fragebogen-Generator (25 Fragen, 5D × 5 Items)
- ✅ Cronbach's Alpha Reliabilitätsberechnung
- ✅ IMP-Score Berechnung (multiplikativ & additiv)
- ✅ Statistische Analysen & Visualisierungen
- ✅ CSV-Export für Probandendaten

**Usage**:
```python
python imp_validation_study.py
```

**Output**:
- `questionnaire_TIMESTAMP.json` - Fragebogen
- `example_responses_TIMESTAMP.csv` - Beispieldaten  
- `validation_results_TIMESTAMP.png` - Visualisierungen
- `validation_report_TIMESTAMP.json` - Analysebericht

---

### 2. `model_comparison_simulation.py`
**Zweck**: Vergleich multiplikatives vs. additives Modell  
**Features**:
- ✅ 1000 Monte-Carlo-Simulationen
- ✅ Zero-Impact-Analyse (Null-Wert-Problem)
- ✅ Sensitivitätsanalyse 
- ✅ 6 Visualisierungen (inkl. 3D-Plot)
- ✅ Statistische Vergleiche

**Usage**:
```python
python model_comparison_simulation.py
```

**Output**:
- `model_comparison_results.png` - 6-Panel-Visualisierung
- `model_comparison_data.csv` - Simulationsdaten

**Key Findings**:
- 🏆 Multiplikatives Modell zeigt Interdependenz
- ⚠️ Null-Werte führen zu komplettem IMP-Kollaps
- 📊 Sensitivität gegenüber schwachen Dimensionen

---

## 🚀 Schnellstart

### Voraussetzungen
```bash
pip install pandas numpy scipy matplotlib seaborn
```

### 1. Validierungsstudie durchführen
```bash
cd validation/
python imp_validation_study.py
```

### 2. Modellvergleich ausführen
```bash
python model_comparison_simulation.py
```

---

## 📊 Ergebnisse

### Cronbach's Alpha (Reliabilität)
Zielwert für jede Dimension:
- ✅ **Exzellent**: α ≥ 0.9
- ✅ **Gut**: α ≥ 0.8  
- ⚠️ **Akzeptabel**: α ≥ 0.7
- ❌ **Fragwürdig**: α < 0.7

### IMP-Score Interpretation
Multiplikatives Modell (0-100%):
- **80-100%**: Exzellentes Potential
- **60-80%**: Gutes Potential
- **40-60%**: Durchschnittlich
- **20-40%**: Entwicklungsbedürftig
- **0-20%**: Kritische Schwachstellen

---

## 🔬 Methodologie

### Dimensionen (je 5 Items)
1. **Autonomie (A)**: Selbstbestimmung, freie Entscheidungen
2. **Intrinsische Motivation (IM)**: Flow, innerer Antrieb
3. **Resilienz (R)**: Anpassungsfähigkeit, Stressbewältigung
4. **Soziale Partizipation (SP)**: Gemeinschaft, Engagement
5. **Authentizität (Au)**: Echtheit, Wertekongruenz

### IMP-Formel
```python
# Multiplikativ (empfohlen)
IMP = (A/7) * (IM/7) * (R/7) * (SP/7) * (Au/7) * 100

# Additiv (Vergleich)
IMP = (A + IM + R + SP + Au) / 5
```

**Rationale für Multiplikation**:
- 🔗 Zeigt Interdependenz zwischen Dimensionen
- 🎯 Eine schwache Dimension limitiert Gesamtpotential
- 🌐 Spiegelt komplexe Systemdynamik wider

---

## 📄 Nächste Schritte

### SOFORT (0-1 Monat)
- [ ] Echte Probanden rekrutieren (Ziel: 30+)
- [ ] Online-Fragebogen erstellen (Google Forms/LimeSurvey)
- [ ] Datensammlung starten
- [ ] Erste Pilotanalyse durchführen

### KURZFRISTIG (1-3 Monate)
- [ ] Reliabilität mit echten Daten prüfen
- [ ] Items bei Bedarf überarbeiten
- [ ] Erweiterte Simulationen (Bayesian)
- [ ] Preprint-Paper schreiben

### MITTELFRISTIG (3-6 Monate)
- [ ] Peer-Review-Publikation einreichen
- [ ] Größere Stichprobe (100+ Probanden)
- [ ] Cross-Validation mit externen Daten
- [ ] Open-Science-Toolkit veröffentlichen

---

## 📚 Literatur & Grundlagen

**Psychometrie**:
- Cronbach, L. J. (1951). Coefficient alpha and the internal structure of tests.
- Nunnally, J. C. (1978). Psychometric theory (2nd ed.).

**5D-Dimensionen**:
- Csikszentmihalyi, M. (1990). Flow: The Psychology of Optimal Experience
- Deci, E. L., & Ryan, R. M. (2000). Self-Determination Theory
- Masten, A. S. (2001). Ordinary magic: Resilience processes

**Modellvergleiche**:
- Luhmann, N. (1984). Soziale Systeme
- Maturana, H., & Varela, F. (1980). Autopoiesis and Cognition

---

## ❗ Wichtige Hinweise

### Null-Wert-Problem
⚠️ **KRITISCH**: Im multiplikativen Modell führt eine Dimension mit Wert 0 zu IMP = 0!

**Lösung**: 
- Verwende **Mindestwert 1** (nicht 0) auf Likert-Skala
- Oder: Transformiere 0 → 0.1 für Berechnungen

### Interpretation
- IMP ist **KEIN fixer Persönlichkeitswert**
- IMP zeigt **aktuelles Entwicklungspotential**
- Dynamisch veränderbar durch Training/Intervention

---

## 👥 Kontakt & Contribution

**Autor**: karlitos1337  
**Projekt**: 5D-Intelligence-Framework  
**Lizenz**: Open Source (MIT)  
**Issues**: [GitHub Issues](https://github.com/karlitos1337/5d/issues)

**Contributions Welcome!**
- 🐛 Bug Reports
- 💡 Feature Requests  
- 📈 Datenvalidierung
- 📝 Dokumentation

---

## 🎯 Ziel dieser Validierung

Nachweis, dass das 5D-Framework:
1. **Reliabel** ist (Cronbach's α > 0.8)
2. **Validität** besitzt (Konstruktvalidität)
3. **Praktisch anwendbar** ist (einfache Erhebung)
4. **Theoretisch fundiert** ist (interdisziplinär)

→ **Ziel**: Publikationsreife für Preprint erreichen!

---

*Letzte Aktualisierung: 05.12.2025, 00:00 CET*  
*Version: 1.0.0 (Prototyp)*
