# 5D Intelligence Framework – AI Agent Instructions

**Version:** 4.0 (Streamlined Architecture Guide)  
**Last Updated:** 2025-12-03  
**Goal:** Help AI agents be immediately productive with scientific rigor

---

## 🏗️ Core Architecture

### Data Pipeline (Sequential Flow)
```
5d_extractor.py → 5d_research_scraper.py → 5d_github_api.py → JSON artifacts
                                                                     ↓
                               5d_dashboard.py (main) + pages/*.py (Streamlit multipage)
                                              ↓
                                     5d_discord_bot.py (optional)
```

**Critical:** JSON files (`5d_solutions.json`, `5d_research_data.json`, `5d_github_data.json`) are the stable contract between pipeline stages. Never rename core JSON keys without team discussion.

### Project Structure Patterns
- **manifest/** - Human-curated knowledge base (MD files)
- **formeln/** - Mathematical formulas (001-157)
- **models/schemas.py** - Pydantic validation for all JSON (required!)
- **config/default.yaml** - All configurable parameters (no hardcoding)
- **pages/*.py** - Streamlit multipage apps (emoji prefixes for ordering)
- **web/5d-map/** - Static Leaflet map with OWID/World Bank data integration

---

## 🔬 Scientific Rigor Requirements

**Every code change must include:**

1. **Evidence Label** - Tag claims as ✅ Fakt (peer-reviewed), ⚠️ Hypothese (testable), or �� Spekulation (exploratory)
2. **BibTeX Citation** - Reference `07_daten_analysen/5d-relevant-sources.bib` (134+ entries)
3. **Test Coverage** - Add test to `tests/` with scientific basis documented
4. **FAQ Update** - If users might ask "Where does this data come from?", update `docs/FAQ.md`

**Example:**
```python
def calculate_imp(A, IM, R, SP, Au):
    """
    IMP = A × IM × R × SP × Au (multiplicative)
    
    Scientific Basis:
    - ✅ Autonomy → IM (Deci & Ryan 1985, 1000+ studies)
    - ⚠️ Multiplicative formula (testable Q2 2026, n>100)
    
    BibTeX: deci1985intrinsic
    """
    return A * IM * R * SP * Au
```

---

## 🛠️ Developer Workflows

### Quick Start
```bash
# Install dependencies
pip install -r requirements_extended.txt

# Run full pipeline + tests
./start.sh  # Extractor → Scraper → GitHub API → Dashboard (port 8501) → Map (port 5500)
pytest tests/ -v  # 161+ tests (100% passing)

# Or use Make
make start      # Same as ./start.sh
make test       # Run pytest
make serve-map  # Serve web/5d-map on port 5500
```

### Adding a New Feature
1. **Check BibTeX** - Is there a scientific reference in `07_daten_analysen/5d-relevant-sources.bib`?
2. **Define Evidence Level** - ✅⚠️🔮 based on peer-review status
3. **Update Schema** - If adding new JSON keys, update `models/schemas.py` (Pydantic validation)
4. **Write Test** - Add to `tests/` with expected outcomes and scientific reference
5. **Update FAQ** - Anticipate user questions about data sources or methodology
6. **Add Info-Box** - In Streamlit UI, include citation and evidence badge

### Pydantic Validation Pattern
All JSON outputs must pass `models/schemas.py` validation:
```python
from models.schemas import Solutions, Project, DimensionScore

# Automatic normalization + deduplication
solutions = Solutions(
    projects=[Project(name="Bäckerei", investment="50.000", roi="95%")],
    dimension_scores=[DimensionScore(dimension="A", score=0.95, source="manifest.md")],
    plan={}
)
# score auto-normalizes to [0,1], names deduplicate
```

---

## �� 5D Framework Essentials

**The 5 Dimensions (IMP Formula):**
- **A** - Autonomie (self-determination)
- **IM** - Intrinsische Motivation (intrinsic interest)
- **R** - Resilienz (stress recovery capacity)
- **SP** - Soziale Partizipation (community engagement)
- **Au** - Authentizität (value-action alignment)

**Formula:** `IMP = A × IM × R × SP × Au` (multiplicative - if any dimension = 0, system collapses)

**Scientific Basis:**
- ✅ SDT (Self-Determination Theory): Deci & Ryan 1985 (1000+ studies)
- ✅ Polyvagal Theory: Porges 2011 (150+ studies)
- ⚠️ Multiplicative IMP: Own research (testable Q2 2026, n>100)

**Complexity Levels (1D-5D):**
- **1D** - Monocausal (X → Y)
- **2D** - Trade-offs (X vs Y)
- **3D** - Triangular models (SDT: Autonomy, Competence, Relatedness)
- **4D** - Time dynamics (longitudinal processes)
- **5D** - Network complexity (graph topology + emergence)

---

## 🗺️ Interactive Map Architecture

**Location:** `web/5d-map/` (static site, Leaflet + vanilla JS)

**Layers:**
- **Heatmap** - Depression (OWID) + Dropout (World Bank) → Intensity = avg(depression%, dropout%)/100
- **IMP Choropleth** - Proxy calculation using WGI (World Governance Indicators) as fallback:
  - `A = 1 - dropout/100`
  - `IM = 1 - depression/100`
  - `R = normalize(WGI Rule of Law)`
  - `SP = normalize(WGI Voice & Accountability)`
  - `Au = normalize(WGI Government Effectiveness)`
- **Schools** - Alternative education markers from `data/schools.json`
- **Time Travel** - Historical slider for yearly data

**Caching:** LocalStorage (1h TTL), automatic fallback to baseline if APIs fail

**Run locally:**
```bash
cd web/5d-map && python3 -m http.server 5500
```

---

## 📋 Key Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `VISION.md` | Central 5D definition, 1D-5D complexity levels | ✅ Complete |
| `TODO.md` | Infrastructure tasks (13/15, 87%) | �� In Progress |
| `TODO_RESEARCH.md` | Scientific validation roadmap (85+ tasks) | 🟡 In Progress |
| `docs/EXECUTIVE_SUMMARY_2025.md` | Complete overview (92% A-, 54.2% facts) | ✅ Complete |
| `docs/CLAIMS_EVIDENCE_MATRIX.md` | 48 claims with evidence labels | ✅ Complete |
| `docs/BEWERTUNGSMATRIX_5D.md` | Scoring system (Nuclear NFU rubric adapted) | ✅ Complete |
| `ETHIK_MANIFEST.md` | 13 biases, abort criteria | ✅ Complete |
| `07_daten_analysen/LITERATUR_INDEX.md` | 134 BibTeX entries | ✅ Complete |
| `models/schemas.py` | Pydantic validation (required) | ✅ Complete |
| `config/default.yaml` | All configurable parameters | ✅ Complete |

---

## ❌ Critical Don'ts

- ❌ **Rename JSON keys** without team approval (breaks pipeline contract)
- ❌ **Hardcode values** - use `config/default.yaml` instead
- ❌ **Add claims without evidence labels** (✅⚠️🔮 required)
- ❌ **Skip tests** when changing schemas or formulas
- ❌ **Ignore FAQ updates** - anticipate user questions proactively

---

## 🎯 Success Metrics

**AI Agent is successful when:**
1. All changes have scientific references (BibTeX citations)
2. All claims have evidence labels (✅ Fakt 54.2%, ⚠️ Hypothese 35.4%, 🔮 Spekulation 10.4%)
3. Tests pass (161+ tests, 100% passing)
4. FAQ is updated proactively
5. Project score increases (current: 92% A-)

**Check progress:**
```bash
cat docs/BEWERTUNGSMATRIX_5D.md | grep "GESAMT"  # Current: 92/100 (A-)
pytest tests/ -v | grep "passed"  # Should show 161+ passed
```

---

## 🔗 Quick Navigation

- **Pipeline Start:** `./start.sh` or `make start`
- **Tests:** `pytest tests/ -v` or `make test`
- **Map Preview:** `make serve-map` → http://localhost:5500
- **Dashboard:** http://localhost:8501 (auto-launched by start.sh)
- **Scientific Docs:** `VISION.md`, `docs/EXECUTIVE_SUMMARY_2025.md`, `docs/FAQ.md`
- **Research Roadmap:** `TODO_RESEARCH.md`, `08-experimente-validierung/experiments/research_agenda.md`

---

**Version:** 4.0  
**Environment:** Ubuntu 24.04.3 LTS, Python 3.10+, Dev Container  
**Major Milestones:** 10/10 dashboard pages ✅, 161 tests passing ✅, 92% A- score ✅
