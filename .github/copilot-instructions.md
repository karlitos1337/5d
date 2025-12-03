# 5D Intelligence Framework – AI Coding Agent Instructions

**Version:** 3.0 (Scientific Documentation Update)  
**Last Updated:** 2025-12-03, 03:31 CET  
**Goal:** Help AI agents be immediately productive AND scientifically rigorous

---

## 🔬 SCIENTIFIC RIGOR REQUIREMENTS (NEW)

**ALL** code changes, new features, or documentation must address:

### 1. **Scientific Basis** → Info-Box mit Zitation
**Example:**
```python
# In pages/1_📊_IMP_Analysis.py
st.markdown("""
<div class="info-box">
  <h4>Was ist der IMP-Faktor?</h4>
  <p>Der IMP-Faktor basiert auf <strong>Selbstbestimmungstheorie (Deci & Ryan 1985)</strong>...</p>
  <button onclick="showSource('deci1985intrinsic')">

 Quellen</button>
</div>
""", unsafe_allow_html=True)
```

### 2. **Validation Status** → Badge: "Own Research" vs "Peer-Reviewed"
**Example:**
```html
<p>
  Autonomie fördert intrinsische Motivation 
  <span class="evidence-badge evidence-fact">✅ Fakt</span>
</p>
<p>
  IMP-Formel (multiplikativ) 
  <span class="evidence-badge evidence-hypothesis">⚠️ Hypothese</span>
</p>
```

### 3. **Data Source** → Link + Download-Button
**Example:**
```html
<a href="https://databank.worldbank.org/source/education-statistics" target="_blank">
  🌐 World Bank EdStats
</a>
<button onclick="downloadCSV('dropout_data.csv')">📍 CSV herunterladen</button>
```

### 4. **User Questions** → FAQ erweitern proaktiv
**Before implementing** new feature, ask:
- "Könnte User fragen: 'Woher stammen diese Daten?'"
- "Sollte ich FAQ.md mit Antwort erweitern?"

### 5. **UI Clarity** → 50-UI-Tips (UX guidelines)
**Check:**
- ✅ Labels IMMER sichtbar, nicht nur Placeholder
- ✅ Validation-Feedback direkt an Eingabestelle
- ✅ Keine komplexen Formulare in Modals

---

## 📚 ESSENTIAL FILES (UPDATED)

| File | Purpose | Status |
|------|---------|--------|
| **VISION.md** | Zentrale Definition 5D-Framework | ✅ Fertig (2025-12-03) |
| **docs/FAQ.md** | 15 häufige Fragen | ✅ Fertig (2025-12-03) |
| **docs/DATENQUELLEN.md** | Transparenz Google Drive + Externe Quellen | ✅ Fertig (2025-12-03) |
| **docs/BEWERTUNGSMATRIX_5D.md** | Wissenschaftliches Scoring (adaptiert von NFU Rubric) | ⚠️ TODO |
| **docs/CLAIMS_EVIDENCE_MATRIX.md** | 40 Behauptungen, Evidenzlabels | ✅ Fertig |
| **ETHIK_MANIFEST.md** | 13 Biases, Abbruchkriterien | ✅ Fertig |
| **LITERATUR_INDEX.md** | 91 BibTeX-Einträge | ✅ Fertig |
| **models/schemas.py** | Pydantic validation für alle JSON | ✅ Fertig |
| **config/default.yaml** | Alle konfigurierbaren Parameter | ✅ Fertig |

---

## 🎯 SCORING-SYSTEM (NEW)

**Projekt wird bewertet nach Nuclear NFU Policy Memo Rubric (adaptiert):**

| Kategorie | Gewichtung | Aktuell | Ziel |
|-----------|------------|---------|------|
| Framework Position (VISION.md) | 20% | 18/20 (90%) | 18/20 (90%) ✅ |
| Analysis (Evidenz, FAQ) | 35% | 28/35 (80%) | 30/35 (86%) |
| Writing Quality (Doku) | 20% | 18/20 (90%) | 18/20 (90%) ✅ |
| Sources (BibTeX) | 15% | 15/15 (100%) | 15/15 (100%) ✅ |
| Formatting (Repo) | 10% | 10/10 (100%) | 10/10 (100%) ✅ |
| **GESAMT** | **100%** | **89/100 (89%, B+)** | **91/100 (91%, A-)** |

**Siehe:** `docs/BEWERTUNGSMATRIX_5D.md` (vollständige Matrix, TODO)

---

## 📚 EVIDENZ-LABEL-SYSTEM (NEW)

**Alle Behauptungen müssen gelabelt sein:**

| Label | Bedeutung | Kriterien | Beispiel |
|-------|-----------|-----------|----------|
| ✅ **Fakt** | Peer-reviewed, repliziert | Mind. 3 unabhängige Studien | SDT: Autonomie → intrinsische Motivation |
| ⚠️ **Hypothese** | Plausibel, testbar, nicht validiert | Theoretisch fundiert, falsifizierbar | IMP-Formel (multiplikativ) |
| 🔮 **Spekulation** | Explorativ, spekulativ | Konzeptuell, keine Empirie (yet) | 5D als spatio-temporales Netzwerkmodell |

**Usage:**
```python
# In code:
def calculate_imp(A, IM, R, SP, Au):
    """
    IMP = A × IM × R × SP × Au (multiplikativ)
    
    Scientific Basis: 
    - ✅ Autonomy → IM (Deci & Ryan 1985, 1000+ studies)
    - ⚠️ Multiplicative formula (testable Q2 2026, n>100)
    
    BibTeX: deci1985intrinsic
    """
    return A * IM * R * SP * Au
```

---

## 🚨 ABBRUCHKRITERIEN (NEW)

**Framework muss angepasst werden, wenn:**

| Kriterium | Schwelle | Konsequenz |
|-----------|----------|------------|
| IMP korreliert NICHT mit Life Satisfaction | r < 0.30 (n > 100) | Formel überarbeiten |
| Faktorenanalyse: A, IM, R, SP, Au sind NICHT distinkt | α < 0.60, PCA < 5 | Dimensionen reduzieren |
| Alternative Schulen haben KEINE höheren IMP-Scores | t-Test p > 0.05 (n > 30) | Hypothese falsifiziert |
| Peer-Review: Fundamentale Kritik | 3+ Rejections | Neukonzeption |

**Siehe:** `ETHIK_MANIFEST.md` (15+ Kriterien)

---

## 🛠️ DEVELOPER WORKFLOWS (UPDATED)

### Quick Start (mit wissenschaftlicher Validierung)
```bash
# 1. Alles installieren
pip install -r requirements_extended.txt

# 2. Pipeline + Tests laufen lassen
./start.sh  # Startet Extractor, Scraper, GitHub API, Dashboard, Map
pytest tests/ -v  # 161+ wissenschaftliche Tests (100% passing)

# 3. Wissenschaftliche Dokumentation prüfen
cat VISION.md  # ✅ Fertig (2025-12-03)
cat docs/FAQ.md  # ✅ Fertig (2025-12-03)
cat docs/CLAIMS_EVIDENCE_MATRIX.md  # ✅ 40 Behauptungen dokumentiert
cat docs/BEWERTUNGSMATRIX_5D.md  # ⚠️ TODO
```

### Neue Feature entwickeln (mit wissenschaftlicher Basis)
```python
# 1. BibTeX-Eintrag prüfen/erstellen
# In 07_daten_analysen/5d-relevant-sources.bib:
@article{deci1985intrinsic,
  author = {Deci, Edward L and Ryan, Richard M},
  title = {Intrinsic Motivation and Self-Determination in Human Behavior},
  year = {1985},
  journal = {Springer Science \& Business Media}
}

# 2. Evidenzlabel definieren
EVIDENCE_LEVEL = "FACT"  # or "HYPOTHESIS" or "SPECULATION"

# 3. Info-Box im UI
st.markdown("""
<div class="info-box">
  <h4>Wissenschaftliche Basis</h4>
  <p>Basierend auf <strong>Deci & Ryan (1985)</strong>...</p>
  <span class="evidence-badge evidence-fact">✅ Fakt</span>
</div>
""", unsafe_allow_html=True)

# 4. Test schreiben
def test_new_feature():
    """
    Test mit wissenschaftlicher Referenz.
    
    Scientific Basis: Deci & Ryan 1985
    Expected: r > 0.60 (autonomy vs. IM)
    """
    result = calculate_something()
    assert result > 0.60

# 5. FAQ erweitern
# In docs/FAQ.md:
### Neue Frage: "Ist Feature X validiert?"
**Antwort:** ✅/⚠️/🔮 + Begründung + Quellen
```

---

## 📋 TODO PRIORITY (NEW)

**BEFORE** any other work:

1. ✅ **VISION.md erstellen** (2 Stunden) → +3 Punkte → Fertig 2025-12-03
2. ✅ **docs/FAQ.md erstellen** (1 Stunde) → +2 Punkte → Fertig 2025-12-03
3. ✅ **docs/DATENQUELLEN.md erstellen** (30 Min) → Transparenz → Fertig 2025-12-03
4. ⚠️ **docs/BEWERTUNGSMATRIX_5D.md** (1 Stunde) → Scoring-System
5. ⚠️ **docs/UI_INFO_BOXEN.html** (2 Stunden) → Evidenzlabels im UI

**Nach 1-5: Score = 91%+ (A-)** 🎯

---

## 🔗 QUICK LINKS (UPDATED)

- **[TODO.md](../TODO.md)** - Infrastruktur (13/15, 87%)
- **[TODO_MULTIPAGE.md](../TODO_MULTIPAGE.md)** - Dashboard (10/10 Pages, 100%)
- **[TODO_RESEARCH.md](../TODO_RESEARCH.md)** - Forschung (85+ Tasks)
- **[VISION.md](../VISION.md)** - Zentrale Definition (✅ Fertig)
- **[docs/FAQ.md](../docs/FAQ.md)** - 15 häufige Fragen (✅ Fertig)
- **[docs/DATENQUELLEN.md](../docs/DATENQUELLEN.md)** - Transparenz (✅ Fertig)
- **[docs/BEWERTUNGSMATRIX_5D.md](../docs/BEWERTUNGSMATRIX_5D.md)** - Scoring (⚠️ TODO)
- **[docs/CLAIMS_EVIDENCE_MATRIX.md](../docs/CLAIMS_EVIDENCE_MATRIX.md)** - 40 Behauptungen
- **[ETHIK_MANIFEST.md](../ETHIK_MANIFEST.md)** - Bias-Log, Abbruchkriterien

---

## ❌ WHAT NOT TO DO (UPDATED)

❌ **Add claims without evidence labels** (must be ✅⚠️🔮)  
❌ **Create features without scientific basis** (needs BibTeX + Info-Box)  
❌ **Skip FAQ updates** (proaktiv User-Fragen antizipieren)  
❌ **Ignore BEWERTUNGSMATRIX_5D.md** (alle Änderungen beeinflussen Score)  
❌ **Hardcode values** that should be in `config/default.yaml`  
❌ **Rename public JSON keys** without team discussion  
❌ **Skip tests** when changing data schemas  

---

## 🎯 SUCCESS METRICS (NEW)

**AI Agent is successful wenn:**

1. ✅ Alle Änderungen haben wissenschaftliche Basis (BibTeX-Zitate)
2. ✅ Alle Behauptungen haben Evidenzlabels (✅⚠️🔮)
3. ✅ UI hat Info-Boxen mit Quellen-Buttons
4. ✅ FAQ wird proaktiv erweitert
5. ✅ Tests decken wissenschaftliche Behauptungen ab (161+ Tests, 100% passing)
6. ✅ Score steigt (89% → 91%+, A-)

**Measure:**
```bash
# Score prüfen
cat docs/BEWERTUNGSMATRIX_5D.md | grep "GESAMT"
# Output: GESAMT: 89/100 (89%, B+) → Ziel: 91/100 (91%, A-)

# Evidenzverteilung prüfen
cat docs/CLAIMS_EVIDENCE_MATRIX.md | grep "Kategorie"
# Output: ✅ Fakt: 18 (45%), ⚠️ Hypothese: 16 (40%), 🔮 Spekulation: 6 (15%)

# Tests prüfen
pytest tests/ -v | grep "passed"
# Output: 161 passed (100%)
```

---

## 📊 Big Picture Architecture

### Core Pipeline (Sequential Data Flow)
```
5d_extractor.py → 5d_research_scraper.py → 5d_github_api.py → JSON artifacts
                                                                     ↓
                               5d_dashboard.py + specialized Streamlit apps
                                              ↓
                                     5d_discord_bot.py (optional)
```

**Key principle:** JSON files are the stable contract between pipeline stages. Never rename core JSON keys without team approval.

### Interactive Visualization
- **5D-Map** (`web/5d-map/`): Leaflet-based world map with live data visualization
  - Heatmaps (depression, dropout rates via OWID/World Bank APIs)
  - IMP-Score choropleth (multidimensional proxy calculation)
  - Alternative schools markers
  - Time-travel slider for historical data
  - Client-side caching (LocalStorage, 1h TTL)

### Scientific Foundations
- **5 Dimensions:** Autonomie (A), Intrinsische Motivation (IM), Resilienz (R), Soziale Partizipation (SP), Authentizität (Au)
- **IMP Formula:** `IMP = A × IM × R × SP × Au` (siehe `models/imp.py`)
- **Data sources:** Manifest files (`manifest/`) contain human-curated knowledge, formulas in `formeln/` (001-157)

---

**Version:** 3.0 (Scientific Documentation Update)  
**Last Updated:** 2025-12-03, 03:31 CET  
**Dev Container:** Ubuntu 24.04.3 LTS, Python 3.10+  
**Major Milestones:**
- Phase 1: All 10 dashboard pages complete (100%) ✅
- Phase 3: Mini-maps on all 7 geographic pages (100%) ✅
- Phase 4: App integration 4/4 complete (100%) ✅
- Phase 8: 161 scientific tests, 151/151 passing (100%) ✅
- **NEW:** Scientific Documentation Upgrade (VISION, FAQ, DATENQUELLEN) ✅
- **NEXT:** BEWERTUNGSMATRIX_5D, UI_INFO_BOXEN, Minimalexperimente ⚠️