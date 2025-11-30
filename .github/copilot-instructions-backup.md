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

### Debug-Playbook (Schnellhilfe)
- Dashboard zeigt nichts/Bild fehlt:
  - Healthcheck: `curl -s http://localhost:8501/_stcore/health` → erwartet `ok`.
  - Neustart:
    ```bash
    pkill -f streamlit || true
    streamlit run 5d_dashboard.py --server.port 8501 --server.headless true
    ```
  - Statischer Fallback: Datei `5d_static_view.html` öffnen.
- Leere Daten:
  - Pipeline neu laufen lassen:
    ```bash
    python 5d_extractor.py && python 5d_research_scraper.py && python 5d_github_api.py
    ```
  - Größen prüfen: `ls -lh 5d_*.json`
- Score‑Validierung > 1.0:
  - Bereits gelöst via Normalisierung in `models/schemas.py` (kein Handlungsbedarf).
- Geringer Speicherplatz:
  - Caches leeren:
    ```bash
    rm -rf ~/.cache/pip ~/.cache/huggingface 2>/dev/null || true
    ```

### Erfolgs-Checks (Akzeptanzkriterien)
- `5d_solutions.json` > 10KB, `5d_research_data.json` > 10KB, `5d_github_data.json` > 20KB.
- Dashboard unter `http://localhost:8501` lädt und zeigt IMP/ROI/Projekte.
- Keine Vorkommen von „PrivateGPT“, „PGPT“ oder `private-gpt-main` im Repo.

### Konventionen & Schnittstellen (bitte erhalten)
- Sprache/Labels: Nutzer-facing Texte und JSON-Keys sind DE (z. B. `"Projekte"`, `"ROI"`, `"Pilots"`). Nicht umbenennen, ohne Dashboard/Bot mit anzupassen.
- Output-Dateien & Schemas:
  - `5d_solutions.json`:
    ```json
    {"solutions": {"Projekte": ["Bäckerei", "Garten"], "ROI": ["95", "485"], "Pilots": ["10"]}, "plan": {"Phase1": "..."}}
    ```
  - `5d_research_data.json`:
    ```json
    {"self-directed learning": {"arxiv": [{"title": "...", "link": "..."}], "pubmed": [{"title": "...", "link": "..."}], "timestamp": "..."}}
    ```
  - `5d_github_data.json`:
    ```json
    {"repositories": {"democratic education": [{"name": "...", "stars": 123, "url": "..."}]}, "trending": {"education": [{"name": "..."}]}, "timestamp": "..."}
    ```
- Dashboard-Erwartungen (`5d_dashboard.py`):
  - Liest obige Dateien; tolerant bei fehlenden Dateien (zeigt Warnungen).
  - Erwartet `solutions['solutions']['ROI']` als Liste parsebarer Zahlen-Strings und `solutions['solutions']['Projekte']` als Liste von Namen.
  - Nutzt `st.cache_data` für `load_data()` – I/O-funktionen rein halten.
- Discord-Bot (`5d_discord_bot.py`):
  - Befehle: `!5d`, `!imp`, `!project`, `!research`, `!github`.
  - Nutzt die gleichen JSON-Dateien (keine abweichenden Strukturen einführen).

### Implementierungsdetails & Muster
- **Extractor** (`5d_extractor.py`):
  - Scannt `manifest/` rekursiv (via `config/default.yaml`: `recursive: true`, `file_types: ['*.md', '*.txt', '*.md']`)
  - Regex für Projekte/ROI/Pilots; IMP-Keywords in `config/default.yaml` unter `keywords: {A, IM, R, SP, Au}`
  - Nutzt Pydantic-Schemas (`models/schemas.py`) für Validierung: `DimensionScore`, `Project`, `Solutions`
  - Fuzzy Matching für Projektnamen (z.B. "Bäckereii" → "Bäckerei" via `normalize_name()`)
  - PDF-Support via PyPDF2 (`max_pages: 50` aus Config)
- **Research-Scraper** (`5d_research_scraper.py`):
  - arXiv (Atom/XML via BeautifulSoup) + PubMed (E-Utilities JSON). 10s Timeout, `time.sleep(1)` Rate-Limit – **beibehalten!**
  - Keywords in `self.keywords`. Neue Themen dort hinzufügen und in `scrape_all()` nutzen.
- **GitHub-Explorer** (`5d_github_api.py`):
  - `search_queries` definieren Suchen. Optionaler `GITHUB_TOKEN` in Header für Rate-Limits.
  - `get_trending_topics()` speichert zusätzliche Daten; Dashboard nutzt primär `repositories`.
- **IMP-Berechnung** (`models/imp.py`):
  - `calculate_imp_verified()` liefert `raw_multiplicative` (A × IM × R × SP × Au), `weighted_additive`, `normalized`
  - Gewichte: `A:1.1, IM:1.05, R:1.0, SP:0.95, Au:1.0` (dokumentiert + konsistent halten)
  - Dashboard verwendet transparente multiplikative Formel (0.52 statt 0.77)
- **Streamlit-Apps**:
  - `5d_dashboard.py`: Nutzt `@st.cache_data` für `load_data()` – I/O-Funktionen rein halten, keine blockierenden Ops im Renderpfad
  - Simulation-Apps (`autopoietic_streamlit.py`, `zwi_streamlit.py`, etc.): Speichern Runs als JSON in `simulations/`
  - Alle lesen JSON-Files gracefully (try/except + Fallbacks bei fehlenden Dateien)

### Änderungen sicher durchführen (Guardrails)
- JSON-Schemas kompatibel halten; neue Felder hinzufügen statt bestehende umzubenennen.
- Output-Dateinamen nicht ändern, außer alle Konsumenten (Dashboard/Bot) werden mitgezogen.
- Netzwerkaufrufe: Timeouts/Fehler fangen und leere Listen zurückgeben (bestehendes Muster beibehalten).
- Streamlit: Keine blockierenden Operationen im Renderpfad; Datenzugriff in `load_data()` kapseln.

### Schnelle Debug-Hinweise
- Fehlen Daten im Dashboard? Stelle sicher, dass `python 5d_extractor.py`, `python 5d_research_scraper.py`, `python 5d_github_api.py` zuvor liefen und JSONs im Repo liegen.
- Rate-Limits bei GitHub? `export GITHUB_TOKEN=...` setzen.
- Discord-Bot startet nicht? `export DISCORD_TOKEN=...` setzen und Datei-JSONs erzeugen.

### Externe 5D Repositories & Integration
- **Verwandte Repos**: `universal-system-genesis-5d`, `resonance-formula-5d-intelligence` (Formeln/System-Genesis & Resonanz-/Intelligenzformeln).
- **Einbindung** (empfohlen): Als Git Submodule unter `external/`:
  ```bash
  mkdir -p external
  git submodule add https://github.com/karlitos1337/universal-system-genesis-5d.git external/system-genesis
  git submodule add https://github.com/karlitos1337/resonance-formula-5d-intelligence.git external/resonance-formulas
  ```
- **Konsistenz**: Änderungen nur ergänzend; vorhandene lokale `formeln/` und `manifest/` Strukturen nicht überschreiben.
- **Extraktion erweitern**: `FiveDExtractor(manifest_dir="manifest")` kann parametriert werden oder zusätzliche Läufe über `external/**` (separat ausführen und Ergebnisse mergen, z. B. `solutions_external.json`).
- **Merge-Strategie JSON**: Neue Felder prefixed (`ext_resonanz_*`, `ext_genesis_*`) statt vorhandene Keys ersetzen.
- **Resonanz-/Genesis-Formeln** nicht direkt in IMP-Scores mischen ohne Mapping-Dokument (`mapping_resonance_imp.md` optional anlegen).
- **Bei Updates der Submodules**: `git submodule update --remote --merge` regelmäßig ausführen; niemals lokal modifizierte fremde Formeln zurückpushen ohne Abstimmung.
- **Automatischer Merge**: Skript `merge_external_solutions.py` erzeugt `solutions_external.json` + `5d_solutions_merged.json` (nicht-invasiv, externe Felder unter `external`).
- **Mapping von Resonanz → IMP**: Vorlage `mapping_resonance_imp.md` nutzen; keine direkten Überschreibungen von Kern-Scores.
- **Optionaler Workflow** (nach Submodule-Update):
  ```bash
  python 5d_extractor.py
  python merge_external_solutions.py
  streamlit run 5d_dashboard.py
  ```
