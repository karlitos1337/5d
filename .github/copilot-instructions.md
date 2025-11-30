## 5d – AI Coding Agent Instructions

**Goal**: Enable AI agents to be immediately productive without breaking data flows or interfaces. Reference concrete files and existing patterns.

**Critical Constraint**: NO PrivateGPT/PGPT or RAG/LLM server setups in this repo. Focus on core 5D pipeline and Streamlit frontends.

### Architecture Overview

**Data Pipeline** (sequential ETL):
```
manifest/ → 5d_extractor.py → 5d_solutions.json (Pydantic-validated)
           ↓
         5d_research_scraper.py → 5d_research_data.json (arXiv/PubMed)
           ↓
         5d_github_api.py → 5d_github_data.json (GitHub trending)
           ↓
         5d_dashboard.py (Streamlit, port 8501)
```

**Key Components**:
- **Extractor** (`5d_extractor.py`): Parses `manifest/` recursively for projects/ROI/IMP dimensions. Config-driven via `config/default.yaml`. Supports PDF (PyPDF2, max 50 pages).
- **Research Scraper** (`5d_research_scraper.py`): Fetches papers from arXiv (Atom/XML) + PubMed (E-Utilities). Rate-limited (10s timeout, 1s sleep between requests).
- **GitHub Explorer** (`5d_github_api.py`): Searches education repos. Optional `GITHUB_TOKEN` env var for higher rate limits.
- **Dashboard** (`5d_dashboard.py`): Main UI with IMP scores, project ROI, research/GitHub trends. Uses `@st.cache_data` for I/O.
- **Simulations**: `autopoietic_streamlit.py`, `zwi_streamlit.py`, `gol_streamlit.py`, `partnet_streamlit.py` save runs to `simulations/*.json`.
- **Discord Bot** (`5d_discord_bot.py`): Commands `!5d`, `!imp`, `!project`, `!research`, `!github`. Requires `DISCORD_TOKEN` env var.

**Data Artifacts** (all JSON):
- `5d_solutions.json`: Core output (Pydantic-validated via `models/schemas.py`)
- `5d_research_data.json`, `5d_github_data.json`: External data feeds
- `solutions_external.json`, `5d_solutions_merged.json`: From `merge_external_solutions.py` (submodule data)
- `5d_solutions_adjusted.json`: Optional resonance mappings (`apply_resonance_mapping.py`)
- All consumers (dashboard/bot) gracefully handle missing files

### Developer Workflows

**Environment**: Python 3.10+, Ubuntu 24.04.3 LTS (dev container)

**Setup**:
```bash
pip install -r requirements_extended.txt
export GITHUB_TOKEN=ghp_...  # Optional: higher rate limits
export DISCORD_TOKEN=...     # Required for bot
```

**Complete Pipeline** (orchestrated):
```bash
chmod +x RUN_ALL.sh && ./RUN_ALL.sh
# Runs: extractor → research → github → dashboard startup
```

**Individual Steps**:
```bash
python 5d_extractor.py                     # manifest/ → 5d_solutions.json
python 5d_research_scraper.py              # arXiv/PubMed → 5d_research_data.json  
python 5d_github_api.py                    # GitHub → 5d_github_data.json
streamlit run 5d_dashboard.py              # Dashboard (http://localhost:8501)
streamlit run autopoietic_streamlit.py     # Simulation apps
python 5d_discord_bot.py                   # Discord bot
```

**Testing**:
```bash
pytest tests/                    # Full suite
pytest tests/test_extractor.py -v  # Specific test
```

**Debugging Dashboard Issues**:
```bash
# Health check
curl -s http://localhost:8501/_stcore/health  # Should return "ok"

# Restart if stuck
pkill -f streamlit || true
streamlit run 5d_dashboard.py --server.port 8501 --server.headless true

# Verify data files
ls -lh 5d_*.json  # All should be >10KB (github >20KB)

# Fallback: static view
open 5d_static_view.html
```

### Critical Conventions & Patterns

**Schema Compatibility** (preserve interfaces):
- JSON output files (`5d_*.json`) are consumed by dashboard/bot - keep structure stable
- Add new fields additively, never rename existing keys without updating all consumers
- Use Pydantic validators (`models/schemas.py`) for type safety and normalization
- Example: `DimensionScore` auto-converts 'HIGH'→0.75, normalizes >1.0 scores to [0,1]

**Network Operations** (robustness pattern):
- Always use timeouts (10s standard)
- Return empty lists on failure, never crash
- Rate limiting: `time.sleep(1)` between API calls (arXiv/PubMed)
- Example: `5d_research_scraper.py` line 28 - maintains 1s sleep, 10s timeout

**Streamlit Best Practices**:
- Non-blocking: All I/O in `@st.cache_data` decorated `load_data()` functions
- Graceful degradation: Missing files show warnings, not errors
- Example: `5d_dashboard.py` lines 26-44 - loads 3 JSON files with try/except fallbacks

**Configuration Management**:
- All paths/settings via `config/default.yaml` (not hardcoded)
- Load with `config/loader.py` - optional config_path override
- Keywords, patterns, file types all configurable

### Implementation Patterns

**Extractor** (`5d_extractor.py`):
- Scans `manifest/` recursively (configurable via `config/default.yaml`)
- Regex patterns for projects/ROI/pilots defined in config
- IMP keywords: `{A, IM, R, SP, Au}` from config
- Pydantic validation: `DimensionScore`, `Project`, `Solutions` in `models/schemas.py`
- Fuzzy matching for project names (e.g., "Bäckereii" → "Bäckerei")
- PDF support via PyPDF2 (max 50 pages from config)

**Research Scraper** (`5d_research_scraper.py`):
- arXiv: Atom/XML parsing via BeautifulSoup
- PubMed: E-Utilities JSON API
- Rate limits: 10s timeout, 1s sleep between requests (PRESERVE THIS!)
- Keywords in `self.keywords` - add new topics there

**GitHub Explorer** (`5d_github_api.py`):
- Search queries defined in `search_queries` list
- Optional `GITHUB_TOKEN` in headers for higher rate limits
- Returns repository data + trending topics

**IMP Calculation** (`models/imp.py`):
- Formula: `raw_multiplicative = A × IM × R × SP × Au`
- Weights: `A:1.1, IM:1.05, R:1.0, SP:0.95, Au:1.0` (keep consistent!)
- Dashboard uses transparent multiplicative formula
- Returns: `raw_multiplicative`, `weighted_additive`, `normalized`

**Streamlit Apps**:
- Dashboard: `@st.cache_data` for all I/O operations
- Simulations: Save runs to `simulations/*.json` with timestamps
- All apps handle missing JSON files gracefully (try/except + warnings)

### External Integration

**Submodules** (optional):
- `external/system-genesis`: Universal system genesis formulas
- `external/resonance-formulas`: Resonance/intelligence formulas

**Merge Strategy**:
```bash
python merge_external_solutions.py
# Creates: solutions_external.json + 5d_solutions_merged.json
```

**Rules**:
- External fields use prefixes: `ext_genesis_*`, `ext_resonanz_*`
- Never overwrite core `manifest/` or `formeln/` structures
- Keep submodules updated: `git submodule update --remote --merge`
- Use `mapping_resonance_imp.md` for resonance→IMP mappings
- No direct mixing of resonance/genesis formulas into core IMP scores

### Success Criteria

**File Validation**:
```bash
# Check sizes
ls -lh 5d_*.json  # solutions >10KB, research >10KB, github >20KB

# Validate JSON structure
python -c "import json; json.load(open('5d_solutions.json'))"

# Dashboard health
curl -s http://localhost:8501/_stcore/health  # Returns "ok"
```

**Acceptance Tests**:
- Dashboard loads at http://localhost:8501 showing IMP/ROI/Projects
- All JSON files have valid Pydantic schemas
- No references to "PrivateGPT", "PGPT" or RAG infrastructure
- Tests pass: `pytest tests/`

### Quick Troubleshooting

**Empty Data**:
```bash
# Re-run pipeline
python 5d_extractor.py && python 5d_research_scraper.py && python 5d_github_api.py
```

**Dashboard Not Loading**:
```bash
# Force restart
pkill -f streamlit || true
streamlit run 5d_dashboard.py --server.port 8501 --server.headless true
```

**Common Issues**:
- Score >1.0: Auto-normalized in `models/schemas.py`
- Rate limits: Set `GITHUB_TOKEN` env var
- Bot fails: Set `DISCORD_TOKEN` and ensure JSON files exist
- Low disk: `rm -rf ~/.cache/pip ~/.cache/huggingface 2>/dev/null || true`

### Safe Changes (Guardrails)

**DO**:
- Add new JSON fields additively
- Use config files for all settings
- Return empty lists on network failures
- Cache I/O operations in Streamlit
- Keep rate limiting patterns

**DON'T**:
- Rename existing JSON keys without updating all consumers
- Change output filenames without updating dashboard/bot
- Remove timeouts from network calls
- Block Streamlit render path with I/O
- Mix external formulas directly into core IMP scores

### Language & Labels

**User-Facing Text**: German
- JSON keys: `"Projekte"`, `"ROI"`, `"Pilots"` (don't rename!)
- Dashboard labels in German
- Coordinate changes across dashboard/bot

**Expected JSON Structures**:
```json
// 5d_solutions.json
{"projects": [{"name": "Bäckerei", "roi": 3.0}], "dimension_scores": [...]}

// 5d_research_data.json
{"self-directed learning": {"arxiv": [...], "pubmed": [...]}}

// 5d_github_data.json  
{"repositories": {"democratic education": [...]}, "trending": {...}}
```
