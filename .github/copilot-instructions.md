# 5D Intelligence Framework – GitHub Copilot Instructions

**Goal**: Enable AI coding agents to be immediately productive with clear, project-specific guidance. Focus on real workflows, stable data contracts, and concrete examples from this repository.

**Critical Constraint**: NO PrivateGPT/PGPT or RAG/LLM server setups in this repo. Focus on core 5D pipeline and Streamlit frontends.

## Architecture Overview

### Data Pipeline (Sequential ETL)
```
manifest/ → 5d_extractor.py → 5d_solutions.json (Pydantic-validated)
           ↓
         5d_research_scraper.py → 5d_research_data.json (arXiv/PubMed)
           ↓
         5d_github_api.py → 5d_github_data.json (GitHub trending)
           ↓
         5d_dashboard.py (Streamlit, multipage app in pages/)
           ↓
         web/5d-map/ (Leaflet, static visualization)
```

**Artifact Contract**: `5d_solutions.json`, `5d_research_data.json`, `5d_github_data.json` are the interfaces between pipeline steps. **NEVER rename JSON keys without schema update + tests.**

### Key Components

- **`5d_extractor.py`**: Parses `manifest/` recursively for projects/ROI/IMP dimensions. Config-driven via `config/default.yaml`. Supports PDF (PyPDF2, max 50 pages).
- **`5d_research_scraper.py`**: Fetches papers from arXiv (Atom/XML) + PubMed (E-Utilities). Rate-limited (10s timeout, 1s sleep between requests).
- **`5d_github_api.py`**: Searches education repos. Optional `GITHUB_TOKEN` env var for higher rate limits.
- **`5d_dashboard.py`**: Main Streamlit UI with IMP scores, project ROI, research/GitHub trends. Uses `@st.cache_data` for I/O.
- **`pages/`**: Streamlit multipage app. External templates via `st.components.v1.html` possible (e.g., `web/templates/5d_forschungsplanung.html`).
- **`models/schemas.py`**: Pydantic validation for all artifacts. Schema changes → new tests in `tests/`, then update pipeline writers.
- **`config/default.yaml`**: All configurable values. No hardcodes in pipeline scripts.
- **`web/5d-map/`**: Static Leaflet map. Dashboard renders exclusively from JSON artifacts.
- **Simulations**: `autopoietic_streamlit.py`, `zwi_streamlit.py`, `gol_streamlit.py`, `partnet_streamlit.py` save runs to `simulations/*.json`.
- **Discord Bot** (`5d_discord_bot.py`): Commands `!5d`, `!imp`, `!project`, `!research`, `!github`. Requires `DISCORD_TOKEN` env var.

### Data Artifacts (All JSON)

- `5d_solutions.json`: Core output (Pydantic-validated via `models/schemas.py`)
- `5d_research_data.json`, `5d_github_data.json`: External data feeds
- `solutions_external.json`, `5d_solutions_merged.json`: From `merge_external_solutions.py` (submodule data)
- `5d_solutions_adjusted.json`: Optional resonance mappings (`apply_resonance_mapping.py`)
- All consumers (dashboard/bot) gracefully handle missing files

## Development Environment

**Environment**: Python 3.10+, Ubuntu 24.04.3 LTS (dev container available)

### Setup

```bash
# Install dependencies
pip install -r requirements_extended.txt

# Optional: Higher GitHub API rate limits
export GITHUB_TOKEN=ghp_...

# Required for Discord bot
export DISCORD_TOKEN=...
```

### Running the Pipeline

**Complete Pipeline** (orchestrated):
```bash
chmod +x start.sh && ./start.sh
# Runs: extractor → research → github → dashboard startup
```

Or with Make:
```bash
make start
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

**Map Server**:
```bash
cd web/5d-map && python3 -m http.server 5500
# Or: make serve-map
# Access at http://localhost:5500
```

### Testing

```bash
# Full test suite
pytest tests/ -v
# Or: make test

# Specific test module
pytest tests/test_extractor.py -v

# With coverage
make coverage
```

## Project Rules (Mandatory)

### Evidence Labels
In content changes, use evidence labels:
- ✅ **Fact**: Peer-reviewed, validated research
- ⚠️ **Hypothesis**: Proposed theory, needs validation
- 🔮 **Speculation**: Conceptual, not yet tested

Source citations preferably from `07_daten_analysen/5d-relevant-sources.bib`

### Schema-First Development
1. **New JSON field**: Define in `models/schemas.py` first
2. **Write tests**: Add to `tests/test_*_schema.py`
3. **Run tests**: `pytest tests/`
4. **Update writers**: Modify pipeline scripts (`5d_extractor.py`, `5d_github_api.py`, etc.)
5. **PR description**: Document affected JSON keys and pipeline stages

### Data Provenance
Changes with data source impact require update of `docs/FAQ.md`

## Code Standards & Conventions

### Python Style
- **Type hints required**: `from typing import ...`
- **Docstrings**: Google Style with scientific references
- **Pathlib over os.path**: `from pathlib import Path`
- **Dataclasses**: For structured data (`from dataclasses import dataclass`)
- **Format**: PEP 8, Black (line-length: 100), see `pyproject.toml`
- **Linting**: Ruff (E, F, I, B, UP rules)
- **No license headers**: Keep minimal, invasive changes

### Configuration over Hardcoding
```python
# ❌ Bad
manifest_dir = "manifest"

# ✅ Good
from config.loader import load_config
config = load_config()
manifest_dir = config['extractor']['manifest_dir']
```

### Streamlit Best Practices
```python
# ✅ Always cache expensive operations
@st.cache_data(ttl=300)
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
```

- **Non-blocking I/O**: All I/O in `@st.cache_data` decorated functions
- **Graceful degradation**: Missing files show warnings, not errors
- **No blocking ops** in render path

### Network Operations (Robustness Pattern)
- **Always use timeouts**: 10s standard
- **Return empty lists on failure**, never crash
- **Rate limiting**: `time.sleep(1)` between API calls (arXiv/PubMed)
- Example: `5d_research_scraper.py` maintains 1s sleep, 10s timeout

### Schema Compatibility (Preserve Interfaces)
- JSON output files are consumed by dashboard/bot - **keep structure stable**
- **Add new fields additively**, never rename existing keys without updating all consumers
- Use Pydantic validators (`models/schemas.py`) for type safety and normalization
- Example: `DimensionScore` auto-converts 'HIGH'→0.75, normalizes >1.0 scores to [0,1]

### Language Conventions
- **User-facing texts and JSON keys**: German (e.g., `"Projekte"`, `"ROI"`, `"Pilots"`)
- **Code/APIs**: English
- **Documentation**: German for domain docs, English for technical docs
- **Do NOT rename** without updating dashboard/bot consumers

## Common Workflows

### Adding a New JSON Field
1. Edit `models/schemas.py`
2. Add test in `tests/test_solutions_schema.py`
3. Run `pytest tests/`
4. Update writer in `5d_extractor.py`/`5d_github_api.py`
5. PR description: List affected JSON keys + pipeline stages

### Debugging the Map
```bash
cd web/5d-map && python3 -m http.server 5500
# Open http://localhost:5500 in browser
# Check web/5d-map/data/*.json and config/default.yaml
```

### Adding a New Dashboard Page
1. Create `pages/<order>_<emoji>_<Name>.py`
2. Set `st.set_page_config(...)`
3. Optional: Load template via `st.components.v1.html`
4. Add navigation link via `st.page_link(...)`

### Debugging Dashboard Issues
```bash
# Health check
curl -s http://localhost:8501/_stcore/health  # Should return "ok"

# Restart if stuck (use specific PID from ps aux | grep streamlit)
kill <STREAMLIT_PID>
streamlit run 5d_dashboard.py --server.port 8501 --server.headless true

# Verify data files
ls -lh 5d_*.json  # All should be >10KB (github >20KB)

# Fallback: static view
open 5d_static_view.html
```

## JSON Output Schemas

### `5d_solutions.json`
```json
{
  "solutions": {
    "Projekte": ["Bäckerei", "Garten"],
    "ROI": ["95", "485"],
    "Pilots": ["10"]
  },
  "plan": {"Phase1": "..."}
}
```

### `5d_research_data.json`
```json
{
  "self-directed learning": {
    "arxiv": [{"title": "...", "link": "..."}],
    "pubmed": [{"title": "...", "link": "..."}],
    "timestamp": "..."
  }
}
```

### `5d_github_data.json`
```json
{
  "repositories": {
    "democratic education": [{"name": "...", "stars": 123, "url": "..."}]
  },
  "trending": {"education": [{"name": "..."}]},
  "timestamp": "..."
}
```

## Implementation Details

### Extractor (`5d_extractor.py`)
- Scans `manifest/` recursively (via `config/default.yaml`: `recursive: true`, `file_types: ['*.md', '*.txt', '*.md']`)
- Regex for Projekte/ROI/Pilots; IMP keywords in `config/default.yaml` under `keywords: {A, IM, R, SP, Au}`
- Uses Pydantic schemas (`models/schemas.py`) for validation: `DimensionScore`, `Project`, `Solutions`
- Fuzzy matching for project names (e.g., "Bäckereii" → "Bäckerei" via `normalize_name()`)
- PDF support via PyPDF2 (`max_pages: 50` from config)

### Research Scraper (`5d_research_scraper.py`)
- arXiv (Atom/XML via BeautifulSoup) + PubMed (E-Utilities JSON)
- 10s timeout, `time.sleep(1)` rate limit - **MAINTAIN THIS!**
- Keywords in `self.keywords`. Add new topics there and use in `scrape_all()`

### GitHub Explorer (`5d_github_api.py`)
- `search_queries` define searches
- Optional `GITHUB_TOKEN` in header for rate limits
- `get_trending_topics()` stores additional data; dashboard primarily uses `repositories`

### IMP Calculation (`models/imp.py`)
- `calculate_imp_verified()` returns `raw_multiplicative` (A × IM × R × SP × Au), `weighted_additive`, `normalized`
- Weights: `A:1.1, IM:1.05, R:1.0, SP:0.95, Au:1.0` (documented + keep consistent)
- Dashboard uses transparent multiplicative formula

## Testing Philosophy

- **Property-based testing** (Hypothesis library) over example-based when appropriate
- Test emergent properties, not prescribed behaviors
- Maintain test coverage for schemas and core pipeline
- Example tests in `tests/test_extractor.py`, `tests/test_models_5d.py`

## Scientific Rigor

- Every non-trivial claim must cite peer-reviewed source
- Use `# Reference: [Author Year, DOI]` comments
- LaTeX-style math in comments when applicable
- BibTeX keys from `07_daten_analysen/5d-relevant-sources.bib`

### Core References
```python
CORE_REFERENCES = {
    "fine_grained_networks": "Kong et al. 2019, DOI:10.1093/cercor/bhy123",
    "gaia_hypothesis": "Lovelock & Margulis 1974, DOI:10.3402/tellusa.v26i1-2.9731",
    "intrinsic_motivation": "Deci et al. 1999, DOI:10.1037/0033-2909.125.6.627",
    "mycorrhizal_networks": "Simard 2021, ISBN:978-0525656098",
    "swarm_intelligence": "Seeley 2010, ISBN:978-0691149125",
    "active_inference": "Friston 2010, DOI:10.1016/j.neuroimage.2008.02.054"
}
```

## Anti-Patterns (Flag These!)

- ❌ Tesla/Quantum mysticism as technical foundation
- ❌ Vague metaphors without operationalization
- ❌ Hierarchical control structures (prefer event-driven, reactive)
- ❌ External reward/punishment logic (gamification anti-pattern)
- ❌ Breaking JSON schema compatibility
- ❌ Hardcoded configuration values
- ❌ Blocking I/O in Streamlit render path

## Preferred Patterns

- ✅ Decentralized architectures (publish-subscribe, actor model)
- ✅ Intrinsic feedback loops (self-assessment, reflection)
- ✅ Topological data analysis for pattern recognition
- ✅ Active Inference frameworks (Free Energy Principle)
- ✅ Config-driven behavior
- ✅ Schema-first development
- ✅ Graceful degradation

## Quick Reference

### Key Files and Directories
- `5d_extractor.py`, `5d_research_scraper.py`, `5d_github_api.py` - Pipeline writers/fetchers
- `models/schemas.py` - Data contract/validation
- `config/default.yaml` - Configuration
- `5d_dashboard.py`, `pages/` - Streamlit UI
- `web/5d-map/`, `web/templates/` - Static map/HTML templates
- `tests/` - Schema/workflow tests
- `docs/FAQ.md` - Frequently asked questions
- `CONTRIBUTING.md` - Contribution guidelines
- `manifest/` - Human-curated knowledge base
- `formeln/` - Scientific formulas (001-157)

### Success Checks (Acceptance Criteria)
- `5d_solutions.json` > 10KB
- `5d_research_data.json` > 10KB
- `5d_github_data.json` > 20KB
- Dashboard loads at `http://localhost:8501` and shows IMP/ROI/Projects
- No occurrences of "PrivateGPT", "PGPT" or `private-gpt-main` in repo

### Commands via Makefile
```bash
make start        # Run full pipeline + dashboard
make test         # Run test suite
make serve-map    # Serve static map
make coverage     # Run tests with coverage report
make clean        # Clean caches and artifacts
```

## External Repositories & Integration

**Related Repos**: 
- `universal-system-genesis-5d`
- `resonance-formula-5d-intelligence`

**Integration** (recommended as Git submodules under `external/`):
```bash
mkdir -p external
git submodule add https://github.com/karlitos1337/universal-system-genesis-5d.git external/system-genesis
git submodule add https://github.com/karlitos1337/resonance-formula-5d-intelligence.git external/resonance-formulas
```

**Consistency**: Changes only additive; don't overwrite existing `formeln/` and `manifest/` structures

**Merge Strategy**: New fields prefixed (`ext_resonanz_*`, `ext_genesis_*`) instead of replacing existing keys

**Automatic Merge**: Script `merge_external_solutions.py` creates `solutions_external.json` + `5d_solutions_merged.json`

## Core Philosophy (The 5 Dimensions)

### 1. Neurobiological (Autonomie - A)
**Core**: Fine-grained network dynamics (DMN/FPN coupling) predict adaptive intelligence  
**Reference**: Kong et al. 2019, DOI:10.1093/cercor/bhy123

### 2. Psychological (Intrinsische Motivation - IM)
**Core**: Autonomous agency via intrinsic motivation (Self-Determination Theory)  
**Reference**: Deci & Ryan 1999, DOI:10.1037/0033-2909.125.6.627

### 3. Philosophical (Resilienz - R)
**Core**: Operative autopoiesis – systems define boundaries through internal processes  
**Reference**: Maturana & Varela 1980

### 4. Economic/Governance (Sympoietische Partizipation - SP)
**Core**: Sympoietic cooperation – resource-efficient value creation through interdependence  
**Reference**: Ostrom 1990

### 5. Technological (Authentizität - Au)
**Core**: Active Inference, Topological Data Analysis, Swarm Intelligence  
**References**: Friston 2010, Seeley 2010, Carlsson 2009

## Key Mantras

- *"Natural systems have no bosses, no grades, no penalties – only resonance"*
- *"Don't optimize intelligence – remove coercion that suppresses it"*
- *"Would this code exist in a self-organizing natural system?"*

## The Principle of Non-Coercion (Zwanglosigkeitsprinzip)

- Natural systems persisting over evolutionary timescales self-organize through **intrinsic coherence**, not external control
- Where coercion exists, entropy and decay emerge
- Where non-coercion exists, resilience and antifragility emerge
- This applies universally: ecosystems, neural networks, organizations, educational systems

---

**Questions or gaps?** Please provide feedback – this file is actively maintained and synchronized with schema, pipeline, and dashboard changes.
