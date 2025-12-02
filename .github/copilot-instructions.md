# 5D Intelligence Framework – AI Coding Agent Instructions

**Goal:** Help AI agents be immediately productive without breaking data contracts, pipelines, or scientific rigor.

## Big Picture Architecture

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
- **5 Dimensions:** Autonomy (A), Intrinsic Motivation (IM), Resilience (R), Social Participation (SP), Authenticity (Au)
- **IMP Formula:** `IMP = A × IM × R × SP × Au` (see `models/imp.py`)
- **Data sources:** Manifest files (`manifest/`) contain human-curated knowledge, formulas in `formeln/` (001-157)

## Essential Files to Read First

| File | Purpose |
|------|---------|
| `config/default.yaml` | All configurable parameters (manifest paths, keywords, defaults) |
| `models/schemas.py` | Pydantic validation for all JSON outputs – **change here first** |
| `models/imp.py` | IMP calculation formulas (multiplicative & weighted) |
| `storage/anonymize.py` | Data privacy patterns (GDPR compliance for surveys) |
| `web/5d-map/README.md` | Map architecture, formulas, caching strategy |

## Developer Workflows

### Quick Start
```bash
pip install -r requirements_extended.txt
./start.sh  # or: make start
```

### Individual Pipeline Steps
```bash
python 5d_extractor.py          # → 5d_solutions.json
python 5d_research_scraper.py   # → 5d_research_data.json
python 5d_github_api.py         # → 5d_github_data.json
streamlit run 5d_dashboard.py   # → http://localhost:8501
```

### Run 5D-Map Locally
```bash
cd web/5d-map
python3 -m http.server 5500  # → http://localhost:5500
# Optional CORS proxy for OWID:
python3 owid_proxy.py 5510
```

### Testing
```bash
pytest tests/                    # All tests
pytest tests/test_extractor.py -v  # Specific module with verbose output
make test                        # Quick run via Makefile
```

### Environment Variables
- `GITHUB_TOKEN` – Higher rate limits for GitHub API (optional)
- `DISCORD_TOKEN` – Required only for Discord bot (`5d_discord_bot.py`)

## Critical Data Contracts

### JSON Filenames (NEVER rename without approval)
- `5d_solutions.json` – Extracted 5D dimension scores from manifest
- `5d_research_data.json` – Scraped academic papers
- `5d_github_data.json` – GitHub repo metadata

### Schema Evolution Pattern
1. Update `models/schemas.py` (Pydantic models)
2. Adjust producer scripts (`5d_extractor.py`, etc.)
3. Update consumer scripts (`5d_dashboard.py`, etc.)
4. Add tests in `tests/` to verify backward compatibility

**Example (Score Normalization):**
```python
# models/schemas.py
class DimensionScore(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    
    @field_validator('score', mode='before')
    def parse_score(cls, v):
        # Handles: 'HIGH' → 0.75, '3.5' → 0.7, percentages, etc.
        # Always clamps to [0, 1]
```

## Project-Specific Conventions

### Streamlit Performance
```python
@st.cache_data  # ALWAYS use for expensive file loads
def load_json(filepath):
    return json.load(open(filepath))
```

### API Rate Limiting
```python
# Research scrapers
time.sleep(1)  # Between requests to arXiv/OWID/World Bank
```

### Configuration over Hardcoding
```python
# ❌ Bad
manifest_dir = "manifest"

# ✅ Good
from config.loader import load_config
config = load_config()
manifest_dir = config['extractor']['manifest_dir']
```

### IMP Calculation (Verifiable)
```python
from models.imp import calculate_imp_verified

result = calculate_imp_verified({
    'A': 0.75, 'IM': 0.70, 'R': 0.65, 'SP': 0.75, 'Au': 0.70
})
# Returns: {'raw_multiplicative': 0.179, 'normalized': 0.179, ...}
```

## Scientific Rigor Requirements

When adding new features/functions, **ALWAYS** address:

1. **Scientific Basis** → Create info-box with citation
2. **Validation Status** → Badge: "Own Research" vs "Peer-Reviewed"
3. **Data Source** → Link + download button
4. **User Questions** → Extend FAQ proactively
5. **UI Clarity** → Check against 50-UI-Tips (UX guidelines)

**Example Pattern:**
```python
# surveys/dimension_1_neurobiology.py
NEUROBIOLOGY_QUESTIONS = [
    {
        "id": "neuro_flow_frequency",
        "question": "Wie häufig erleben Sie Flow-Zustände?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Csikszentmihalyi, M. (1990). Flow: The Psychology of Optimal Experience.",
        "bibtex_key": "csikszentmihalyi1990flow"  # Must exist in 07_daten_analysen/5d-relevant-sources.bib
    }
]
```

## Testing Strategy

### Pre-Commit Hook
- Automatically runs: syntax checks + core tests
- Failing core tests **block commits**
- Manual trigger: `pytest tests/`

### Test Categories
- `test_extractor.py` – Manifest parsing, Pydantic validation
- `test_anonymization.py` – GDPR compliance for survey data
- `test_surveys.py` – Likert validation, completeness checks
- `test_formulas_scoring.py` – IMP calculation accuracy

### Writing New Tests
```python
def test_new_feature():
    # Arrange
    input_data = {...}
    
    # Act
    result = process_data(input_data)
    
    # Assert
    assert result['normalized_score'] >= 0.0
    assert result['normalized_score'] <= 1.0
```

## What NOT to Do

❌ **Rename public JSON keys** without team discussion  
❌ **Introduce RAG/LLM external infrastructure** (PrivateGPT/Ollama)  
❌ **Store personal data** outside `storage/anonymize.py` patterns  
❌ **Hardcode values** that should be in `config/default.yaml`  
❌ **Skip tests** when changing data schemas  
❌ **Make blocking network calls** in Streamlit render paths  

## Quick Reference Commands

```bash
# Development
./start.sh              # Full pipeline + dashboard
make serve-map          # Just the 5D-Map
streamlit run 5d_dashboard.py --server.port 8502  # Custom port

# Testing
pytest tests/ -v        # Verbose
pytest -k "test_extractor"  # Specific pattern

# Deployment
git push                # Triggers GitHub Actions for 5D-Map
# Manual: Settings → Pages → Source: GitHub Actions
```

## File Structure Overview

```
5d/
├── manifest/               # Human-curated knowledge (01-08, 99)
├── formeln/                # Scientific formulas (001-157)
├── config/                 # default.yaml + loader.py
├── models/                 # schemas.py (Pydantic), imp.py
├── analysis/               # calculate_5d_scores.py, cluster_responses.py
├── surveys/                # Survey questions with citations
├── storage/                # anonymize.py (GDPR patterns)
├── web/5d-map/             # Interactive Leaflet map
├── tests/                  # Pytest suite
├── 5d_extractor.py         # Stage 1: Manifest → JSON
├── 5d_research_scraper.py  # Stage 2: Research APIs → JSON
├── 5d_github_api.py        # Stage 3: GitHub metadata → JSON
├── 5d_dashboard.py         # Main Streamlit UI
└── RUN_ALL.sh              # Orchestration script
```

---

**Version:** 2.0  
**Last Updated:** December 2, 2025  
**Dev Container:** Ubuntu 24.04.3 LTS, Python 3.10+
