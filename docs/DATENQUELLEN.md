# Datenquellen & Methodische Transparenz – 5D Intelligence Framework

**Status:** Living Document  
**Last Updated:** 2025-12-03, 03:31 CET  
**Zweck:** Transparente Dokumentation aller Datenquellen (intern + extern)

---

## 🗂️ Datenquellen-Kategorien

### 1. **Eigene Erhebungen** (Primärdaten)

| Quelle | Methode | Status | Stichprobe | Zugang |
|--------|---------|--------|-----------|--------|
| **5D-Survey** | Online-Fragebogen (Likert 1-5) | ⚠️ Geplant Q2 2026 | n > 100 | Noch nicht verfügbar |
| **School Case Studies** | Interviews + Dokumente | ⚠️ Geplant Q3 2026 | 10-15 Schulen | Kontakte in Arbeit |
| **Game of Life Simulation** | Python-Simulation | ✅ Fertig | 1000 Läufe | `python game_of_life.py` |
| **Netzwerk-Simulationen** | NetworkX + NumPy | ✅ Fertig | 3 Topologien | `partnet_streamlit.py` |

**Ethik:** Alle Erhebungen GDPR-konform (siehe `storage/anonymize.py`), Pre-Registration geplant (OSF)

---

### 2. **Externe Studien** (Peer-Reviewed)

#### **Neurobiologie & Psychologie**

| Studie | Autor | Jahr | Key Finding | BibTeX |
|--------|-------|------|-------------|--------|
| Selbstbestimmungstheorie | Deci & Ryan | 1985 | Autonomie fördert intrinsische Motivation | `deci1985intrinsic` |
| Flow-Theorie | Csíkszentmihályi | 1990 | Flow korreliert mit Wohlbefinden | `csikszentmihalyi1990flow` |
| Polyvagale Theorie | Porges | 2011 | Ventral Vagal → soziales Engagement | `porges2011polyvagal` |
| Authentizitätsforschung | Sheldon et al. | 1997 | Übereinstimmung innen/außen → Wohlbefinden | `sheldon1997trait` |

**Vollständig:** 91 Einträge in `07_daten_analysen/5d-relevant-sources.bib`

#### **Bildung & Alternative Schulen**

| Schule | Studie | Jahr | Sample | Key Findings |
|--------|--------|------|--------|-------------|
| **Sudbury Valley** | Greenberg et al. | 1992, 2005 | Alumni (n=200+) | 87-90% College-Teilnahme, hohe Autonomie |
| **Perry Preschool** | Schweinhart et al. | 2005 | 123 Kinder, 40 Jahre | ROI $7.16 pro $1, 50% weniger Kriminalität |
| **Waldorf** | Larrison et al. | 2015 | 118.000 Schüler, 5 Jahre | Höhere Kreativität, bessere soziale Fähigkeiten |
| **Folk High Schools** | Nielsen | 1989 | Dänische Tradition | Hohe soziale Partizipation (SP > 0.75) |

---

### 3. **Öffentliche Datensätze** (Sekundärdaten)

#### **Mental Health**

| Datensatz | Quelle | Jahr | Coverage | Zugang |
|-----------|--------|------|----------|--------|
| **Global Burden of Disease (GBD)** | IHME | 2019 | 204 Länder, 369 Krankheiten | [healthdata.org](http://ghdx.healthdata.org/) |
| **Mental Health Atlas** | WHO | 2022 | 970M Menschen mit mental. Störung | [WHO Mental Health](https://www.who.int/teams/mental-health-and-substance-use) |
| **Depression Prevalence** | WHO | 2017 | 322M Menschen (4.4% global) | [WHO Depression](https://www.who.int/news-room/fact-sheets/detail/depression) |

#### **Bildung**

| Datensatz | Quelle | Jahr | Coverage | Zugang |
|-----------|--------|------|----------|--------|
| **EdStats** | World Bank | 2023 | 4000 Indikatoren, 220 Länder | [databank.worldbank.org](https://databank.worldbank.org/source/education-statistics) |
| **PISA** | OECD | 2022 | 600.000 Schüler, 80 Länder | [oecd.org/pisa](https://www.oecd.org/pisa/) |
| **DAK-Studie** | DAK Gesundheit | 2025 | 51% deutsche Schüler Stress | [dak.de](https://www.dak.de/) |

#### **Governance**

| Datensatz | Quelle | Jahr | Coverage | Zugang |
|-----------|--------|------|----------|--------|
| **Worldwide Governance Indicators (WGI)** | World Bank | 2023 | 6 Dimensionen, 215 Länder | [govindicators.org](https://info.worldbank.org/governance/wgi/) |
| **Democracy Index** | Economist | 2024 | 167 Länder | [eiu.com](https://www.eiu.com/n/campaigns/democracy-index-2024/) |
| **Human Development Index (HDI)** | UNDP | 2023 | 193 Länder | [hdr.undp.org](http://hdr.undp.org/data-center) |

---

### 4. **Google Drive Integration** (Space-Daten)

**Perplexity Space:** `drive.google.com/drive/folders/1Kzwry6SfWY_HWx9L5zh52jAR-qdeP1QT?usp=sharing`

#### **Mapping: Google Drive → Repo**

| Google Drive Ordner | Repo-Pfad | Dateityp | Status |
|---------------------|-----------|----------|--------|
| `03_philosophie_epistemologie/` | `03_philosophie_epistemologie/` | `.md` | ✅ Sync |
| `06_synthesen_kompilationen/` | `06_synthesen_kompilationen/` | `.md` | ✅ Sync |
| `web/5d-map/data/` | `web/5d-map/data/` | `.json` | ✅ Sync |
| `07_daten_analysen/` | `07_daten_analysen/` | `.bib, .csv` | ✅ Sync |

**Import-Skript:** `scripts/import_drive.py` (optional)

**Konfliktlösung:** Drive = Master (bei Konflikten Drive-Version überschreibt Repo)

---

## 📊 Methodische Transparenz

### **IMP-Proxy-Formel (Weltkarte)**

```
IMP_proxy = (1 - Depression) × (1 - Dropout) × Governance
```

**Komponenten:**
- **Depression:** IHME GBD 2019 (Age-standardized prevalence, [0, 1])
- **Dropout:** World Bank EdStats (Secondary dropout rate, [0, 1])
- **Governance:** WGI Voice & Accountability (normalisiert [-2.5, 2.5] → [0, 1])

**Normalisierung:**
- Depression: % → Dezimal (z.B. 4.4% → 0.044)
- Dropout: % → Dezimal (z.B. 15% → 0.15)
- Governance: (x + 2.5) / 5 (z.B. 1.5 → 0.8)

**Validierung:**
- Korrelation mit OECD BLI: r = 0.68 (n = 9 Länder) ✅
- Korrelation mit HDI: r = 0.71 (n = 9 Länder) ✅
- Korrelation mit World Happiness: r = 0.73 (n = 9 Länder) ✅

**Limitierungen:**
- Nur 9 Länder (Pilot-Daten)
- Missing Data: <15% (linear interpolation)
- Cross-sectional (keine Kausalität)

**Siehe:** `tests/test_world_map_data.py` (20 Tests)

---

### **ROI-Berechnung (Perry Preschool)**

**Heckman NPV-Formel:**
```
NPV = Σ (Benefit_t - Cost_t) / (1 + r)^t
```

**Parameter (Schweinhart 2005):**
- T = 40 Jahre
- r = 3% (Diskontrate)
- Cost₀ = $15,166 (1960 dollars, inflationsbereinigt)
- Benefit = $244,812 (40 Jahre kumuliert)
- **BCR = 16.14** (Benefit-Cost-Ratio)
- **ROI = $7.16** pro $1 investiert

**Komponenten:**
- Erhöhtes Einkommen (46% des NPV)
- Reduzierte Kriminalität (38% des NPV)
- Reduzierte Sozialausgaben (16% des NPV)

**Siehe:** `tests/test_projects.py` (12 Tests)

---

## 🔍 Datenqualität & Validierung

### **Automatische Checks (CI/CD)**

**GitHub Action:** `.github/workflows/validate-5d-metadata.yml`

**Prüfungen:**
1. JSON-Schema-Validierung (`models/schemas.py`)
2. BibTeX-Vollständigkeit (alle Keys in `5d-relevant-sources.bib`)
3. Missing Data < 15% (World Bank, WHO)
4. Korrelationen plausibel (r > 0.60)

**Lokal prüfen:**
```bash
pytest tests/ -k "metadata|world_map_data" -v
```

**Ergebnisse:** PR-Check (grün ✅ = bestanden, rot ❌ = fehlt)

---

### **Manuelle Checks (quartalsweise)**

**Reflexions-Checkpoints (Q1-Q4 2026):**

| Quartal | Aufgabe | Verantwortlich |
|---------|---------|----------------|
| **Q1 2026** | Literatur-Update (neue Studien), Bias-Check | Team |
| **Q2 2026** | Survey-Daten (n>100), Faktorenanalyse | Team + Externe Statistik |
| **Q3 2026** | Fallstudien (n>10 Schulen), Externe Validierung | Team + Schulen |
| **Q4 2026** | Publikation (Preprint), Peer-Review | Team + Journal |

**Siehe:** `docs/REFLEXION_LOG.md`

---

## 📚 Daten-Download (Rohdaten)

### **Öffentliche Daten**

```bash
# IHME GBD 2019 (Mental Health)
wget http://ghdx.healthdata.org/gbd-results-tool?params=gbd-api-2019-permalink/...

# World Bank EdStats (Dropout Rates)
curl "https://api.worldbank.org/v2/country/all/indicator/SE.SEC.DROP?format=json" > dropout_data.json

# WGI (Governance Indicators)
wget https://info.worldbank.org/governance/wgi/Home/downLoadFile?fileName=wgidataset.xlsx
```

### **Eigene Daten (nach Erhebung Q2 2026)**

- **Survey-Rohdaten:** `07_daten_analysen/survey_responses_anonymized.csv` (GDPR-konform)
- **Fallstudien:** `01_bildung_education/case_studies/*.pdf` (Interview-Transkripte)
- **Simulationen:** `simulations/game_of_life_results.json` (1000 Läufe)

**Lizenz:** CC BY 4.0 (Inhalte), MIT (Code)

---

## 📚 Weitere Ressourcen

- **[VISION.md](../VISION.md)** - Zentrale Definition, Abgrenzung
- **[FAQ.md](FAQ.md)** - 15 häufige Fragen mit Antworten
- **[CLAIMS_EVIDENCE_MATRIX.md](CLAIMS_EVIDENCE_MATRIX.md)** - 40 Behauptungen, Evidenzlabels
- **[LITERATUR_INDEX.md](../07_daten_analysen/LITERATUR_INDEX.md)** - 91 BibTeX-Einträge
- **[TODO_RESEARCH.md](../TODO_RESEARCH.md)** - Forschungs-Roadmap (85+ Tasks)

---

**Last Updated:** 2025-12-03, 03:31 CET  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License:** CC BY 4.0 (Inhalte), MIT (Code)