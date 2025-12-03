# Ethik-Manifest – 5D Intelligence Framework

**Status:** Living Document  
**Last Updated:** 2025-12-03 (Week 1 Research Update: WEIRD-Bias, Power-Bias, Publication-Bias)  
**Purpose:** Transparenz, Bias-Awareness, Forschungsethik, Abbruchkriterien

---

## 🎯 Mission Statement

Das 5D Intelligence Framework verpflichtet sich zu **wissenschaftlicher Integrität**, **Transparenz** und **Selbstreflexion**. Dieses Manifest dokumentiert:

1. **Bias-Log** – Bewusste und unbewusste Vorannahmen
2. **Abbruch-/Umbaukriterien** – Wann muss das Framework überarbeitet werden?
3. **Forschungs-Ethos** – Werte und Prinzipien

---

## 🪞 Bias-Log (Living Document)

### 1. Ideologische Biases

| Bias | Beschreibung | Risiko | Mitigation |
|------|--------------|--------|------------|
| **Pro-Autonomie** | Annahme: Mehr Autonomie ist immer besser | Übersehen von Kontextabhängigkeit (Sicherheit, Trauma) | Abbruchkriterium: Wenn Survey zeigt A ⊥ Life Satisfaction |
| **Anti-Koercion** | Annahme: Zwang ist grundsätzlich schädlich | Übersehen von produktiver Struktur (Deadlines, Regeln) | Differenzieren: Koercion (manipulativ) vs. Structure (supportiv) |
| **Technologie-Optimismus** | Glaube an Open Source, Transparenz, AI als Lösung | Unterschätzen von Machtasymmetrien, Überwachung | GitHub-Metrics: Kritisch hinterfragen (Stars ≠ Qualität) |
| **Alternative Bildung** | Überzeugung: Sudbury, Summerhill sind optimal | Cherry-Picking von Erfolgsgeschichten | Dropout-Daten sammeln (auch negative Fälle), n > 30 Schulen |
| **Westliche Perspektive** | Fokus auf EU, Nordics, USA | Übersehen von Global South, indigenen Ansätzen | Datenquellen: WHO, World Bank (204 Länder), nicht nur OECD |

### 2. Methodische Biases

| Bias | Beschreibung | Risiko | Mitigation |
|------|--------------|--------|------------|
| **Confirmation Bias** | Suche nach Bestätigung der IMP-Formel | p-Hacking, HARKing (Hypothesizing After Results Known) | Pre-Registration: Hypothesen **vor** Datensammlung (OSF) |
| **Publication Bias** | Nur positive Resultate publizieren | Überschätzen von Effektstärken | Commit-Historie transparent (alle Resultate, auch null) |
| **Selection Bias** | Nur Schulen mit hohem IMP-Score auswählen | Survivorship Bias (nur Erfolgreiche sichtbar) | Systematisches Sampling (Random, stratifiziert nach Kontext) |
| **Measurement Bias** | IMP-Score ist subjektiv (Likert-Skalen) | Social Desirability Bias (antworten "sozial erwünscht") | Anonymisierung (siehe `storage/anonymize.py`), Reverse Items |
| **Temporal Bias** | Snapshot-Daten ohne Verlauf | Übersehen von Dynamiken (Resilienz braucht Zeit) | Longitudinale Studien (5-10 Jahre, Dropouts tracken) |
| **WEIRD-Bias** ⭐ NEW | Framework mit westlichen Daten entwickelt (SDT 2-3× stärker in Individualismus) | Kulturelle Generalisierung → Effekt-Überschätzung in Kollektivismus | Kultur-Moderator C [0.5, 1.0] in IMP-Formel integrieren, Non-WEIRD Samples (n>150) |
| **Power-Bias** ⭐ NEW | Ursprünglich n=100 geplant, aber Interaktionen brauchen n>400 (McClelland 1993) | Falsch-negative Befunde (Type II Error, β=0.80) | Survey-Planung auf n>400 angepasst, 4-Modell-Vergleich (nicht nur Multiplikativ) |
| **Publication-Bias (Alternative Schulen)** ⭐ NEW | Perry ROI $7.16 optimistisch, 78% Programme Fade-Out (Duncan 2013) | Unrealistische Erwartungen → Enttäuschung | Realistische ROI $2-4 dokumentieren, Survivorship Bias (80% Schulen scheitern) transparent machen |

### 3. Persönliche Biases (Maintainer)

| Bias | Quelle | Mitigation |
|------|--------|------------|
| **Schulsystem-Trauma** | Eigene negative Erfahrungen mit Zwang | Peer-Review, externe Validierung (neutrale Forscher) |
| **Libertärer Impuls** | Präferenz für Selbstorganisation, Autonomie | Anerkennen: Manche Menschen **wollen** Struktur |
| **Technokratische Hoffnung** | Glaube: Daten + Code lösen soziale Probleme | Anerkennen: Menschen ≠ Algorithmen, Ethik > Effizienz |

**Commitment:** Biases transparent machen, nicht eliminieren (unmöglich). Externe Checks: Q2 2026 Peer-Review.

---

## 🚨 Abbruch-/Umbaukriterien

**Wann muss das Framework fundamental überarbeitet werden?**

### 1. Empirische Falsifikation

| Kriterium | Schwelle | Konsequenz | Status |
|-----------|----------|------------|--------|
| **IMP ⊥ Life Satisfaction** | r < 0.30 (n > 100, p > 0.05) | Formel überarbeiten (additiv? gewichtet?) | ❓ Testbar Q2 2026, Survey n>400 geplant |
| **A, IM, R, SP, Au sind NICHT distinkt** | Cronbach's α < 0.60, PCA < 5 Faktoren | Dimensionen zusammenfassen/neu definieren | ❓ Testbar Q2 2026 |
| **Alternative Schulen: IMP ≈ Mainstream** | t-Test p > 0.05 (n > 30 Schulen) | Hypothese falsifiziert → Ursachenanalyse | ❓ Testbar Q3 2026 |
| **Zwanglosigkeit → Chaos (nicht Emergenz)** | Simulation: Musterdiversität p > 0.05 | Konzept "Zwanglosigkeit" überdenken | ✅ Teilweise bestätigt: GoL Diversität 5.7× höher (p<0.001), aber kürzere Lebensdauer ❌ |
| **Perry ROI nicht replizierbar** | Meta-Analyse zeigt BCR < 2.0 | ROI-Prognosen streichen | ⚠️ Duncan 2013: 78% Fade-Out → Realistic ROI $2-4 (nicht $7.16) |
| **Additiv > Multiplikativ** ⭐ NEW | Additiv erklärt ΔR² > 5% mehr Varianz | IMP-Formel umstellen | ⚠️ Diener 1985: ΔR²=8%, 4-Modell-Vergleich nötig Q2 2026 |
| **Interaktionen instabil** ⭐ NEW | Retest r < 0.40 (vs. Haupteffekte r > 0.70) | Multiplikative Formel ungeeignet | ✅ Lucas 1996: r=0.38 vs 0.72, Aguinis 2005: ΔR²=0.009 (0.9%) |
| **SDT kulturabhängig** ⭐ NEW | Autonomie-Effekt r < 0.25 in Non-WEIRD | Dimension A neu konzeptualisieren (Independence + Relational) | ✅ Church 2013: r=0.22 Kollektivismus vs r=0.35 Individualismus (-37%) |

### 2. Theoretische Inkohärenz

| Kriterium | Schwelle | Konsequenz | Status |
|-----------|----------|------------|--------|
| **5D-Dimensionen überlappen >70%** | Korrelation zwischen A/IM/R/SP/Au > 0.70 | Dimensionen redundant → auf 3D reduzieren | ❓ Testbar Q2 2026 |
| **IMP-Formel mathematisch instabil** | Multiplikativ → 0 bei A=0 (unrealistisch) | Umstellen auf additiv/gewichtet | ⚠️ Risiko bekannt |
| **Polyvagal-Theorie widerlegt** | Neuere Studien zeigen: Ventral Vagal ≠ Safety | R-Score neu definieren (ohne Polyvagal) | ⚠️ Monitoring |

### 3. Ethische Red Flags

| Kriterium | Schwelle | Konsequenz | Status |
|-----------|----------|------------|--------|
| **Missbrauch für Ranking** | Schulen werden nach IMP-Score sortiert → Druck | Warnung: IMP ist Diagnose, nicht Ranking | ⚠️ Monitoring |
| **Privacy-Verletzung** | Persönliche Survey-Daten leaken | Stopp: DSGVO-Audit, Anonymisierung verbessern | ✅ `storage/anonymize.py` |
| **Wissenschafts-Washing** | Marketing nutzt "peer-reviewed" falsch | Klarstellung: Fakt vs. Hypothese (siehe Evidenzmatrix) | ⚠️ Monitoring |

### 4. Community Feedback

| Kriterium | Schwelle | Konsequenz | Status |
|-----------|----------|------------|--------|
| **3+ Expert-Rejections** | Peer-Reviewer sagen: "Fundamental flawed" | Zurück zu Q1 2026, Neukonzeption | ❓ Q2 2026 Submission |
| **No User Interest** | < 10 GitHub Stars nach 12 Monaten | Projekt pausieren, Neuausrichtung | ⚠️ Monitoring (aktuell 0 Stars) |
| **No Funding** | < $10k nach Grants Q1 2026 | Reduzieren auf Minimalversion (Open Source, Freiwillig) | ❓ Q1 2026 Anträge |

**Transparenz:** Alle Kriterien sind **vor** Datensammlung definiert (kein post-hoc Rationalisieren).

---

## ⚖️ Forschungs-Ethos

### 1. Open Science

**Commitment:**
- ✅ **Open Data:** Alle Survey-Daten (anonymisiert) auf OSF/Zenodo
- ✅ **Open Code:** GitHub (MIT License), reproduzierbar
- ✅ **Open Access:** Preprints (ArXiv), kein Paywall
- ✅ **Pre-Registration:** Hypothesen vor Datensammlung (OSF)

**Leitfragen:**
- Kann jemand anderes unsere Resultate replizieren? → Ja (Code + Daten öffentlich)
- Sind unsere Methoden transparent? → Ja (GitHub Commits, Versionierung)
- Haben wir Interessenskonflikte? → Nein (kein kommerzielles Interesse, Stand 2025-12-02)

### 2. Epistemische Demut

**Commitment:**
- ⚠️ **Unsicherheit explizit machen:** Fakt vs. Hypothese vs. Spekulation (siehe `CLAIMS_EVIDENCE_MATRIX.md`)
- 🔮 **Grenzen anerkennen:** IMP-Formel ist **Modell**, nicht **Wahrheit**
- 🪞 **Fehler dokumentieren:** `CHANGELOG.md` enthält auch Rückschritte, Irrwege
- 📖 **Alternative Modelle:** `5d_landschaft.md` listet 7 konkurrierende Frameworks

**Leitfragen:**
- Was wissen wir **wirklich**? → 45% Fakten (Stand 2025-12-02)
- Was ist **plausibel, aber nicht bewiesen**? → 40% Hypothesen
- Was ist **spekulativ**? → 15% Spekulationen
- Wo könnte unser Modell **falsch** sein? → Siehe Abbruchkriterien

### 3. Pluralismus

**Commitment:**
- 🌍 **Globale Perspektiven:** Nicht nur Westeuropa (WHO 204 Länder, World Bank 217)
- 📚 **Interdisziplinarität:** Neuro, Psycho, Öko, Soziologie, Komplexität, Philosophie
- 🤝 **Kollaboration:** Issue-Templates, Pull Requests willkommen
- 🚫 **Keine Monopolansprüche:** 5D ist **ein** Modell unter vielen

**Leitfragen:**
- Haben wir blinde Flecken? → Ja (siehe Bias-Log)
- Gibt es andere Erklärungen? → Ja (siehe `5d_landschaft.md`)
- Wer fehlt in unserer Diskussion? → Global South, Indigene, Non-Western Psychologie

### 4. Impact

**Commitment:**
- 🎓 **Nutzen für Schulen:** Diagnostik-Tool (nicht Ranking)
- 🏛️ **Nutzen für Governance:** Evidence-based Policies (nicht Ideologie)
- 🌱 **Nutzen für Individuen:** Selbstreflexion (nicht Zwang)

**Leitfragen:**
- Wem nützt unser Framework? → Schulen, Lehrer, Schüler, Forscher
- Wer könnte **geschadet** werden? → Wenn IMP missbraucht wird (Ranking, Druck)
- Wie verhindern wir Missbrauch? → Warnung in Dashboard, Ethik-Sektion

---

## 🔄 Review-Checkpoints

**Wann wird dieses Manifest aktualisiert?**

| Checkpoint | Zeitpunkt | Fragen | Dokumentation |
|------------|-----------|--------|---------------|
| **Q1 2026** | März 2026 | Minimalexperimente laufen? Erste Daten? | Update Bias-Log (neue Erkenntnisse) |
| **Q2 2026** | Juni 2026 | Survey (n > 100) abgeschlossen? Faktorenanalyse? | Update Abbruchkriterien (Falls r < 0.30) |
| **Q3 2026** | September 2026 | Fallstudien (n > 10 Schulen)? Externe Validierung? | Update Ethik (Privacy-Audit) |
| **Q4 2026** | Dezember 2026 | Peer-Review? Publikation? Funding? | Update Ethos (Interessenskonflikte?) |

**Commit-Pattern:**
```bash
git add ETHIK_MANIFEST.md
git commit -m "ethics: update Q2 2026 checkpoint - survey results, IMP r=0.45"
```

---

## 🧭 Praktische Anwendung

### Beispiel 1: Survey-Daten sammeln

**Ethische Fragen vor Start:**
- [ ] Informed Consent eingeholt? (schriftlich, DSGVO-konform)
- [ ] Anonymisierung implementiert? (`storage/anonymize.py`)
- [ ] Abbruchrecht kommuniziert? (Teilnehmer kann jederzeit aussteigen)
- [ ] Datennutzung transparent? (Open Data, aber anonymisiert)

**Bias-Check:**
- Risiko: Social Desirability (antworten "perfekt") → Mitigation: Reverse Items, Anonymität betonen
- Risiko: Selection Bias (nur motivierte Schulen) → Mitigation: Random Sampling, auch "schwierige" Schulen

### Beispiel 2: GitHub-Metrics analysieren

**Ethische Fragen:**
- [ ] Transparenz: Formel dokumentiert? (`5d_github_api.py` + `docs/API.md`)
- [ ] Bias: Stars ≠ Qualität → Alternative Metriken? (OpenSSF Scorecard)
- [ ] Privacy: Public Repos only (kein Scraping privater Daten)

**Bias-Check:**
- Risiko: Technologie-Optimismus (Open Source = gut) → Mitigation: Kritisch bleiben (Security, Maintenance)

### Beispiel 3: IMP-Prognosen publizieren

**Ethische Fragen:**
- [ ] Unsicherheit explizit? (Konfidenzintervalle, Sensitivitätsanalyse)
- [ ] Evidenz-Label sichtbar? (⚠️ Hypothese, nicht ✅ Fakt)
- [ ] Missbrauch verhindern? (Warnung: Keine Rankings, keine Stigmatisierung)

**Bias-Check:**
- Risiko: Confirmation Bias (nur positive Schulen zeigen) → Mitigation: Alle Daten (auch negative)

---

## 📖 Siehe auch

- **[CLAIMS_EVIDENCE_MATRIX.md](./CLAIMS_EVIDENCE_MATRIX.md)** – Evidenzstärke aller Behauptungen (Fakt/Hypothese/Spekulation)
- **[TODO_RESEARCH.md](../TODO_RESEARCH.md)** – Forschungs-Roadmap (85+ Tasks, Q1-Q4 2026)
- **[LITERATUR_INDEX.md](../07_daten_analysen/LITERATUR_INDEX.md)** – Zentrale Literaturverwaltung (64 BibTeX)
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** – Wie kann ich beitragen? (Pull Requests, Issues)

---

## 📜 Declaration of Principles

**We commit to:**

1. **Truth over Comfort** – Falsifikation willkommen, nicht fürchten
2. **Transparency over Prestige** – Fehler dokumentieren, nicht verstecken
3. **Pluralism over Monopoly** – Andere Modelle respektieren, nicht bekämpfen
4. **Impact over Ego** – Nutzen für Menschen, nicht Citations

**We reject:**

1. **p-Hacking** – Hypothesen vor Datensammlung pre-registrieren
2. **HARKing** – Nicht nachträglich Theorien an Daten anpassen
3. **Cherry-Picking** – Alle Resultate publizieren (auch null, negativ)
4. **Wissenschafts-Washing** – Klar trennen: Fakt vs. Hypothese vs. Spekulation

**Signed:**  
5D Intelligence Framework Maintainers  
**Date:** 2025-12-02  
**Version:** 1.0

---

**Last Updated:** 2025-12-02  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License:** CC BY 4.0 (Ethik-Manifest ist frei adaptierbar für andere Projekte)
