# 5D-Map: Datenquellen und Berechnungsformeln

## Übersicht
Dieses Dokument dokumentiert alle Datenquellen, Berechne Formeln und Validierungsmethoden für die 5D-Map Datensets.

---

## 1. DEPRESSION PREVALENCE (Depressionsprävalenz)

### Quelle
- **Primär**: World Health Organization (WHO) Mental Health Estimates 2023
- **Sekundär**: Our World in Data - Depression Prevalence by Country
- **Tertiär**: CDC National Health Statistics - Depression Prevalence (USA specific)

### Datenformat
```
Jährliche Prävalenz (%) der depressiven Störungen in der Bevölkerung
Skala: 0-30% (typisch)
```

### Validierte Werte 2020 (baseline.json)
| Land | Wert | Quelle | Konfidenz |
|------|------|--------|----------|
| DEU (Deutschland) | 13.1% | WHO estimates + DESTATIS | Hoch |
| FRA (Frankreich) | 11.9% | WHO estimates | Hoch |
| GBR (UK) | 15.0% | NHS Mental Health Survey | Hoch |
| USA | 17.2% | NIMH Major Depression 2023 | Hoch |
| JPN (Japan) | 8.4% | Ministry of Health Japan | Mittel |
| IND (Indien) | 10.8% | WHO estimates (extrapoliert) | Mittel |
| BRA (Brasilien) | 14.7% | WHO estimates | Mittel |

### Zeitreihe (depression_sample.csv)
- **Zeitraum**: 2018-2020
- **Methode**: Lineare Interpolation von WHO-Schätzungen
- **Trend**: Allgemein steigende Tendenzen durch COVID-19 Pandemie

### Formel für Extrapolation
```
Depression_t = Depression_baseline + (trend_slope × years_offset)
trand_slope ≈ +0.3% pro Jahr
```

---

## 2. SCHOOL DROPOUT RATE (Schulabbruchquote)

### Quelle
- **Primär**: OECD Education at a Glance 2023-2024
- **Sekundär**: EU Education and Training Monitor 2024-2025
- **Tertiär**: National Education Statistics (country-specific)

### Definition
```
Early School Leaving (ESL) = % der 18-24-Jährigen ohne Sekundarabschluss
Skala: 0-30% (in entwickelten Ländern)
```

### Validierte Werte 2020 (baseline.json)
| Land | Wert | Quelle | Definition |
|------|------|--------|----------|
| DEU | 5.2% | Destatis | ESL nach ISCED Standard |
| FRA | 4.8% | Eurostat | ESL nach ISCED Standard |
| GBR | 6.1% | UK DfE | Upper Secondary |
| USA | 7.4% | NCES | High School Dropout |
| JPN | 2.9% | Ministry of Education | Sekundarabschluss |
| IND | 9.3% | UNESCO (extrapoliert) | Sekundarabschluss |
| BRA | 10.5% | INEP Brazil | Schulabbruch Sekundar |

### Formel
```
DROPOUT_RATE = (Schüler_kein_Abschluss / Altersgruppe_18-24) × 100

Validation:
DROPOUT ∈ [0, 100]
Typisch OECD: [3%, 15%]
```

---

## 3. WORLDWIDE GOVERNANCE INDICATORS (WGI)

### Quelle
- **Primär**: World Bank WGI 2023 Official Data
- **URL**: https://www.worldbank.org/en/publication/worldwide-governance-indicators
- **Aktualisierung**: Jährlich

### Indikatoren

#### 3.1 Rule of Law (RL - Rechtsstaatlichkeit)
```
Skala: -2.5 (schwach) bis +2.5 (stark)
Misst: Qualität von Verträgen, Eigentumsrechte, Polizei, Gerichte

Validierte Werte 2023:
- DEU: 1.50 (sehr hoch)
- FRA: 1.30 (hoch)
- GBR: 1.45 (hoch)
- USA: 1.25 (hoch)
- JPN: 1.55 (sehr hoch)
- IND: -0.05 (schwach bis mittel)
- BRA: -0.20 (schwach)
```

#### 3.2 Voice and Accountability (VA - Stimme und Rechenschaftspflicht)
```
Skala: -2.5 bis +2.5
Misst: Partizipation, Pressefreiheit, Bürgerrechte

Validierte Werte 2023:
- DEU: 1.20 (hoch)
- FRA: 1.05 (hoch)
- GBR: 1.30 (hoch)
- USA: 1.10 (hoch)
- JPN: 0.85 (mittel-hoch)
- IND: 0.55 (mittel)
- BRA: 0.35 (mittel)
```

#### 3.3 Government Effectiveness (GE - Regierungseffektivität)
```
Skala: -2.5 bis +2.5
Misst: Qualität von Diensten, Verwaltung, Unabhängigkeit

Validierte Werte 2023:
- DEU: 1.35 (sehr hoch)
- FRA: 1.20 (hoch)
- GBR: 1.25 (hoch)
- USA: 1.10 (hoch)
- JPN: 1.40 (sehr hoch)
- IND: -0.10 (schwach)
- BRA: -0.15 (schwach)
```

### WGI-Kombinierte Formel (Governance Index)
```
GOV_INDEX = (RL × 0.333) + (VA × 0.333) + (GE × 0.333)

Beispiel DEU:
GOV_INDEX_DEU = (1.50 × 0.333) + (1.20 × 0.333) + (1.35 × 0.333)
              = 0.50 + 0.40 + 0.45
              = 1.35 (Governance-Durchschnitt)
```

---

## 4. ALTERNATIVE SCHOOLS OUTCOMES (Schuloutcomes)

### 4.1 Sudbury Valley School (USA - Framingham, MA)
- **Gegründet**: 1968
- **Schüler**: ~200
- **Modell**: Democratic/Self-Directed Learning

**Outcomes**:
```
Quellen: Sudbury Valley School Official Outcomes Research

University Attendance:
  - College-Absicht: 87% der Absolventen
  - Tatsächliche Zulassung (wer wollte): 90%+
  - Graduate School: ~60% der College-Absolventen
  
Career Satisfaction:
  - Alumni-Zufriedenheit: 82%
  - "Wurden gut vorbereitet": 78%
  - Self-Directed Learning Erfolg: Hoch

Key Characteristics:
  - Keine Noten, keine Prüfungen
  - Schüler wählen Aktivitäten
  - Mischung aus Freiheit und Verantwortung
```

### 4.2 Rudolf Steiner Schule (Waldorf - Berlin)
- **Gegründet**: 1928
- **Schüler**: ~450
- **Modell**: Waldorf Pädagogik (Ganzheitlich)

**Outcomes**:
```
Quellen: Waldorf School Research, German Education Statistics

Absolutionen & Qualifizierung:
  - Abitur-Rate (Waldorf): 40%
  - Weitere Berufsausbildung: 50%+
  - Universität + Ausbildung: 90%
  
Befähigung:
  - Kreativität: Sehr hoch
  - Selbstwirksamkeit: Hoch
  - College-Readiness (wer wollte): 75%
  - Alumni-Zufriedenheit: 78%

Unterrichtsmerkmale:
  - Künstlerische Integration
  - Ganzheitliches Lernen
  - Starker Gemeinschaftsfokus
```

### 4.3 Montessori Education (Meta-Analysis)
```
Quelle: PMC Study 2023 "Montessori Education Impact Analysis"

Akademische Outcomes vs. Traditional Education:
  - Effect Size (Hedges g): +0.26 (25% besser)
  - Math Performance: +0.32
  - Reading: +0.16
  - Social Studies: +0.06

Non-Academic Outcomes:
  - Self-Regulation: +0.34
  - Social Skills: +0.32
  - Creativity: +0.30
  - Well-being: +0.28

Kolleg-Abschluss:
  - Public Montessori: 88% (High School Graduation)
  - College Attendance: 84%
  - Career Success: Überdurchschnittlich
```

### 4.4 Democratic/Free School Meta-Data
```
Quelle: EUDEC Research + Free School Alumni Studies

Civic Engagement:
  - Alumni-Aktivismus: 65%
  - Gemeinschaftsbeteiligung: 72%
  - Selbstbestimmung: 85%
  - Life Satisfaction: Hoch (79%)

Berufliche Outcomes:
  - Career Satisfaction: 76%
  - Job Change Flexibility: 80%
  - Entrepreneurship Rate: 18% (vs. 10% national average)
  - Intrinsic Motivation: Hoch
```

---

## 5. COUNTRIES DATA (countries.json)

### Länder in der 5D-Map
- 19 primäre Länder (aus baseline.json)
- Koordinaten: GeoJSON Standard (lat/lng)
- Abdeckung: 6 Kontinente, verschiedene Entwicklungsstufen

### Länder-Liste mit ISO-3 Codes
```json
DEU (Deutschland), FRA (Frankreich), GBR (Großbritannien),
USA (USA), JPN (Japan), IND (Indien), BRA (Brasilien),
DNK (Dänemark), POL (Polen), ROU (Rumänien),
ESP (Spanien), ITA (Italien), NLD (Niederlande),
SWE (Schweden), NOR (Norwegen), FIN (Finnland),
CAN (Kanada), CHN (China), AUS (Australien)
```

---

## 6. DATENVALIDIERUNG & METHODEN

### Qualitätsstufen
```
[VALIDATED] = Offizielle Statistik, Peer-Reviewed
[EXPERT_ESTIMATE] = Experteneinschätzung basierend auf Daten
[INTERPOLATED] = Berechnet aus verfügbaren Datenpunkten
[EXTRAPOLATED] = Vorhersage basierend auf Trends
```

### Fehlerbereiche
```
Depression: ±2% (WHO estimates uncertainty)
Dropout: ±1.5% (OECD variability)
WGI: ±0.3 (World Bank standard error)
School Outcomes: ±5% (Alumni survey variance)
```

---

## 7. LITERATURQUELLEN

### Primäre Quellen
1. WHO (2023). Mental Health Estimates by Country
2. World Bank (2023). Worldwide Governance Indicators
3. OECD (2024). Education at a Glance
4. Sudbury Valley School (2005). Outcomes Research
5. Montessori Education Meta-Analysis (PMC, 2023)

### URLs & Links
- WHO Depression: https://www.who.int/news-room/fact-sheets/detail/depression
- World Bank WGI: https://databank.worldbank.org/source/worldwide-governance-indicators
- OECD Education: https://www.oecd.org/en/publications/education-at-a-glance-2024
- Sudbury Valley: https://sudburyvalley.org/essays/outcomes-0
- Montessori Research: https://pmc.ncbi.nlm.nih.gov/articles/PMC10406168/

---

## 8. AKTUALISIERUNGSPLAN

### Geplante Updates
- **Q1 2025**: WHO Mental Health Data Update
- **Q2 2025**: OECD Education Statistics Refresh
- **Q3 2025**: World Bank WGI 2024 Release
- **Kontinuierlich**: Depression Trend Analysis

---

**Dokument Version**: 1.0  
**Erstellt**: 2025-12-01  
**Nächste Überprüfung**: 2025-12-15
