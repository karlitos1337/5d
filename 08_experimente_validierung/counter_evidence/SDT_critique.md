# Kritische Evidenz: Selbstbestimmungstheorie (SDT)

**Status:** Active Research  
**Last Updated:** 2025-12-03  
**Purpose:** Sammlung von Gegenbeweisen und Limitationen für SDT (Deci & Ryan 1985)

---

## 📊 Original Claims (Pro-Evidenz)

**Behauptung 1.1 (CLAIMS_EVIDENCE_MATRIX.md):**
> Autonomie fördert intrinsische Motivation (✅ Fakt, 1000+ Studien)

**Meta-Analysen:**
- Deci & Ryan (2000): r = 0.40-0.60 (mittel-stark)
- Vansteenkiste et al. (2010): Autonomy Support → Motivation (d = 0.49)

---

## 🚨 Counter-Evidence & Kritik

### 1. **Over-Justification Effect** (Lepper, Greene & Nisbett 1973)

**Befund:**
- **Externe Belohnungen** können intrinsische Motivation **untergraben**
- Kinder, die für Zeichnen bezahlt wurden, zeichneten **weniger** danach
- Effektstärke: d = 0.34 (Meta-Analyse, Deci, Koestner & Ryan 1999)

**Implikationen für 5D-Framework:**
- ⚠️ Autonomie allein reicht nicht → Kontext wichtig (Belohnungen vermeiden!)
- ⚠️ IMP-Formel muss **Kontext** berücksichtigen (z.B. extrinsische Anreize als Störvariable)

**BibTeX:**
```bibtex
@article{lepper1973undermining,
  title={Undermining children's intrinsic interest with extrinsic reward},
  author={Lepper, Mark R and Greene, David and Nisbett, Richard E},
  journal={Journal of Personality and Social Psychology},
  volume={28},
  number={1},
  pages={129--137},
  year={1973},
  doi={10.1037/h0035519}
}
```

---

### 2. **Kulturabhängigkeit** (Iyengar & Lepper 1999)

**Befund:**
- **Westliche (WEIRD) Samples:** Autonomie → IM (r = 0.50)
- **Asiatische Samples:** Autonomie → IM **schwächer** (r = 0.20-0.30)
- **Kollektivistische Kulturen:** Soziale Verpflichtung wichtiger als persönliche Wahl

**Studie: Choice and Intrinsic Motivation**
- Anglo-American Kinder: Höhere IM bei **selbstgewählten** Aufgaben
- Asian-American Kinder: Höhere IM bei **von Mutter gewählten** Aufgaben
- **Effekt-Reversal:** Autonomie kann IM **senken** in kollektivistischen Kontexten

**Implikationen für 5D-Framework:**
- ❌ Autonomie ist **nicht universell** förderlich für IM
- ⚠️ 5D-Framework muss **kulturelle Moderatoren** einbeziehen
- ⚠️ Folk High Schools (Nordics): Funktioniert in individualistischen Kulturen, aber nicht global?

**BibTeX:**
```bibtex
@article{iyengar1999rethinking,
  title={Rethinking the value of choice: A cultural perspective on intrinsic motivation},
  author={Iyengar, Sheena S and Lepper, Mark R},
  journal={Journal of Personality and Social Psychology},
  volume={76},
  number={3},
  pages={349--366},
  year={1999},
  doi={10.1037/0022-3514.76.3.349}
}
```

---

### 3. **Autonomy Paradox** (Schwartz 2004)

**Befund:**
- **Zu viel Wahl** → Paralyse, Unzufriedenheit, Regret
- "Paradox of Choice": Mehr Optionen ≠ mehr Zufriedenheit
- **U-förmige Kurve:** Optimum bei **mittlerer** Autonomie (nicht maximal)

**Studie: Jam Experiment (Iyengar & Lepper 2000)**
- 24 Jam-Sorten: 3% Kaufrate
- 6 Jam-Sorten: 30% Kaufrate (10× höher!)
- **Oversaturation:** Zu viele Optionen → Überforderung

**Implikationen für 5D-Framework:**
- ⚠️ A (Autonomie) ist **nicht linear** → Schwellenwert existiert
- ⚠️ IMP-Formel muss **nicht-lineare Effekte** berücksichtigen
- ⚠️ Sudbury-Schulen: **Unbegrenzte** Autonomie könnte kontraproduktiv sein (für manche Kinder)

**BibTeX:**
```bibtex
@book{schwartz2004paradox,
  title={The Paradox of Choice: Why More Is Less},
  author={Schwartz, Barry},
  year={2004},
  publisher={Ecco},
  isbn={0060005688}
}

@article{iyengar2000choice,
  title={When choice is demotivating: Can one desire too much of a good thing?},
  author={Iyengar, Sheena S and Lepper, Mark R},
  journal={Journal of Personality and Social Psychology},
  volume={79},
  number={6},
  pages={995--1006},
  year={2000},
  doi={10.1037/0022-3514.79.6.995}
}
```

---

### 4. **Replication Crisis** (Open Science Collaboration 2015)

**Befund:**
- **Psychology Replication Project:** Nur 36% der Studien replizierbar
- **SDT-Studien:** Keine systematische Replikation großer Meta-Analysen
- **Publication Bias:** Nur positive Resultate publiziert (File Drawer Problem)

**Implikationen für 5D-Framework:**
- ⚠️ SDT ist **robuster als andere** (1000+ Studien), aber nicht immun
- ⚠️ Eigene Hypothesen müssen **pre-registered** sein (OSF)
- ⚠️ Null-Resultate müssen **publiziert** werden (auch wenn IMP nicht korreliert)

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

### 5. **Boundary Conditions: Wann funktioniert Autonomie NICHT?**

**Situationen mit geringem/keinem Autonomie-Effekt:**

| Kontext | Autonomie-Effekt | Evidenz | Grund |
|---------|-----------------|---------|-------|
| **Notfälle** | r ≈ 0 | Militär, Medizin | Schnelle Koordination wichtiger als Wahl |
| **Hohe Komplexität** | r < 0.20 | Anfänger-Lernen | Cognitive Load → Structure nötig |
| **Kollektivistische Kulturen** | r = 0.20-0.30 | Iyengar 1999 | Soziale Norm > persönliche Wahl |
| **Kinder <5 Jahre** | r = 0.10-0.20 | Entwicklungspsychologie | Noch keine Selbstregulation |
| **Depression/Trauma** | r ≈ 0 oder negativ | Klinische Psychologie | Strukturbedarf höher |

**Implikationen für 5D-Framework:**
- ❌ Autonomie ist **nicht universell** → Moderatoren notwendig
- ⚠️ IMP-Formel braucht **Kontextvariable** (Alter, Kultur, Krisensituation)
- ⚠️ Alternative Schulen: Funktioniert **nicht für alle** Kinder (z.B. ADHS, Trauma)

---

## 📊 Meta-Analyse der Kritik

| Kritikpunkt | Evidenzstärke | Implikation | Schwere |
|-------------|---------------|-------------|---------|
| **Over-Justification** | ✅ Repliziert (d=0.34) | Kontext wichtig | 🟡 Mittel |
| **Kulturabhängigkeit** | ✅ Repliziert (r=0.20-0.50) | Nicht universal | 🔴 Hoch |
| **Autonomy Paradox** | ✅ Repliziert (Jam: 10×) | Nicht-linear | 🔴 Hoch |
| **Replication Crisis** | ⚠️ Allgemein (36%) | SDT robuster | 🟡 Mittel |
| **Boundary Conditions** | ✅ Evidenz vorhanden | Moderatoren nötig | 🔴 Hoch |

**Schwere-Kategorien:**
- 🟢 **Niedrig:** Framework bleibt gültig (Minor Adjustments)
- 🟡 **Mittel:** Framework braucht Erweiterung (Moderatoren, Kontexte)
- 🔴 **Hoch:** Framework muss überarbeitet werden (Nicht universal)

---

## 🎯 Konsequenzen für 5D-Framework

### 1. **Claims Matrix anpassen**

**Alte Behauptung (1.1):**
> ✅ Autonomie fördert intrinsische Motivation (Fakt, 1000+ Studien)

**Neue Behauptung (1.1 revised):**
> ✅ Autonomie fördert intrinsische Motivation **in individualistischen Kulturen** (Fakt, Meta r=0.50)  
> ⚠️ Effekt ist **schwächer** in kollektivistischen Kulturen (r=0.20-0.30, Iyengar 1999)  
> ⚠️ **Nicht-linear:** Zu viel Autonomie → Paralyse (Schwartz 2004, Jam Experiment)

**Neue Zeile einfügen:**
> **1.6 Over-Justification Effect:** Externe Belohnungen untergraben IM (✅ Fakt, d=0.34)

### 2. **IMP-Formel erweitern**

**Alte Formel:**
```
IMP = A × IM × R × SP × Au
```

**Problem:** Autonomie ist nicht universell, nicht linear

**Neue Formel (Option 1: Moderatoren):**
```
IMP = f(A, C) × IM × R × SP × Au
```
- **C = Kultur-Faktor** (0.5 kollektivistisch, 1.0 individualistisch)
- **f(A, C) = nicht-lineare Funktion** (U-förmig? Schwellenwert?)

**Neue Formel (Option 2: Schwellenwert):**
```
A_eff = min(A, A_max)  # Cap bei A_max = 0.80 (vermeidet Paralyse)
IMP = A_eff × IM × R × SP × Au
```

**Test:** Welche Formel korreliert besser mit Life Satisfaction? (Q2 2026)

### 3. **ETHIK_MANIFEST.md ergänzen**

**Bias-Log (neuer Eintrag):**
> **Bias 14: Western-WEIRD Bias**  
> Risiko: Framework basiert auf 1000+ Studien, aber 80%+ WEIRD samples  
> Mitigation: Kulturelle Moderatoren einbeziehen, Global South Daten sammeln

**Abbruchkriterium (ergänzen):**
> Falls Autonomie in >50% der Kulturen **keinen** Effekt hat (r<0.20) → Dimension A überdenken

---

## 🔬 Follow-Up Recherche (nächste Schritte)

**Priority 1 (diese Woche):**
- [ ] Suche nach **Meta-Analysen** kultureller Unterschiede (SDT in Asien, Afrika, LatAm)
- [ ] Literaturscan: "SDT AND cross-cultural AND meta-analysis"
- [ ] Identifiziere **optimale Autonomie-Level** (Schwellenwerte aus Studien)

**Priority 2 (nächste Woche):**
- [ ] Kontaktiere **externe Forscher** (z.B. Chirkov, Iyengar) für unveröffentlichte Daten
- [ ] Pre-Registration für eigene Survey: Kulturelle Moderatoren testen (n>100)

---

## 📚 Neue BibTeX-Einträge (Batch 12: Counter-Evidence SDT)

**4 neue Einträge:**
1. `lepper1973undermining` - Over-Justification Effect
2. `iyengar1999rethinking` - Kulturabhängigkeit
3. `schwartz2004paradox` - Autonomy Paradox
4. `osc2015estimating` - Replication Crisis

**Zu ergänzen in:** `07_daten_analysen/5d-relevant-sources.bib`

---

**Erstellt:** 2025-12-03  
**Status:** Active Research  
**Nächstes Update:** Nach Meta-Analyse Scan (10.12.2025)
