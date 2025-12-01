## 5D – Copilot-Instruktionen (prägnant, projektbezogen)

Ziel: Schnell produktiv arbeiten, ohne Datenflüsse/Verträge zu brechen. Fokus auf Kern‑Pipeline, JSON‑Schnittstellen und Streamlit‑UIs dieses Repos.

### Architektur & Datenfluss
- Pipeline: `5d_extractor.py` → `5d_research_scraper.py` → `5d_github_api.py` → JSON Artefakte.
- UIs: `5d_dashboard.py` (Haupt), plus `autopoietic_streamlit.py`, `zwi_streamlit.py`, `gol_streamlit.py`, `partnet_streamlit.py`.
- Bot: Optional `5d_discord_bot.py` liest dieselben JSONs.
- Orchestrierung: `RUN_ALL.sh` führt (1)–(3) aus und startet das Dashboard.

### Setup & Workflows
- Python: 3.10+ (Dev‑Container: Ubuntu 24.04.3 LTS).
- Install: `pip install -r requirements_extended.txt`.
- Config: `config/default.yaml` (geladen via `config/loader.py`) statt Hardcoding nutzen.
- Tokens: `export GITHUB_TOKEN=...` (API Limits), `export DISCORD_TOKEN=...` (Bot).
- Run (Einzelschritte):
  - `python 5d_extractor.py` → schreibt `5d_solutions.json`
  - `python 5d_research_scraper.py` → `5d_research_data.json`
  - `python 5d_github_api.py` → `5d_github_data.json`
  - `streamlit run 5d_dashboard.py` (Port 8501)
- Tests: `pytest tests/` oder gezielt `pytest tests/test_extractor.py -v`.

### Schneller Start (Try it)
- Setup: `pip install -r requirements_extended.txt`
- Test: `pytest -q tests/test_extractor.py`
- Pipeline: `python 5d_extractor.py && python 5d_research_scraper.py && python 5d_github_api.py`
- Dashboard: `streamlit run 5d_dashboard.py`

### Datenverträge (beibehalten)
- Dateien: `5d_solutions.json`, `5d_research_data.json`, `5d_github_data.json`.
- Extractor‑Output: Pydantic‑validiert (`models/schemas.py`):
  - `Solutions = { projects: Project[], dimension_scores: DimensionScore[], plan: {} }`
  - Dashboard liest zusätzlich legacy Felder unter `solutions` (wenn vorhanden) und fällt weich zurück, falls leer.
- Research/GitHub: Map nach Keywords/Queries; enthalten `timestamp` und reichen für UI‑Abschnitte.
- Sprache/Keys: Nutzer‑Facing in DE (z. B. `"Projekte"`, `"ROI"`, `"Pilots"`). Nicht umbenennen ohne UI/Bot‑Update.

### Muster & Konventionen
- Extractor (`5d_extractor.py`):
  - Rekursiver Scan `manifest/` (Dateitypen/Regex aus `config/default.yaml`).
  - Zahlen robust parsen, Projekte deduplizieren (siehe `models/schemas.py`).
- Research (`5d_research_scraper.py`):
  - arXiv (Atom/XML) + PubMed (E‑Utilities JSON). 10s Timeout, `time.sleep(1)` Rate‑Limit beibehalten.
- GitHub (`5d_github_api.py`):
  - `search_queries` definieren Suchthemen; optional `GITHUB_TOKEN` für höhere Limits.
- IMP (`models/imp.py`):
  - `calculate_imp_verified({'A','IM','R','SP','Au'})` liefert `raw_multiplicative`, `weighted_additive`, `normalized` (Gewichte dokumentiert).
- Streamlit (`5d_dashboard.py`):
  - Datenzugriff in `@st.cache_data`‑Funktionen; keine Blocking‑Ops im Renderpfad; Plotly‑Fallbacks vorhanden.

### Guardrails (Änderungen sicher)
- JSON additiv erweitern statt Keys umzubenennen; Dateinamen stabil halten.
- Netzwerkzugriffe robust: Timeouts/Fehler → leere Listen; kein harter Abbruch.
- Keine RAG/PrivateGPT/Ollama‑Setups in diesem Repo; Fokus auf Kern‑5D‑Tools.

### Diagnose & Recovery
- Dashboard leer? Pipeline neu ausführen und Dateigröße prüfen: `ls -lh 5d_*.json`.
- Healthcheck: `curl -s http://localhost:8501/_stcore/health` → `ok` erwartet.
- Neustart UI: `pkill -f streamlit || true && streamlit run 5d_dashboard.py --server.headless true`.
- GitHub Limits: `export GITHUB_TOKEN=...`; Bot: `export DISCORD_TOKEN=...`.

### Externe Quellen (optional)
- Submodules unter `external/` möglich (siehe Ordnerstruktur); Merge via `merge_external_solutions.py` erzeugt `solutions_external.json`/`5d_solutions_merged.json` additiv.

### Weltkarte (Frontend)
- Vollständige Spezifikation: `docs/5d-map/COPILOT_INSTRUCTIONS.md` (Pointer → `md_copilot_ki_anweisung`).
- Kurz‑Anweisung (MVP, präzise Formeln & Pfade): `md_copilot_ki_anweisung`.
- Stack: Static Web (HTML/CSS/JS), Leaflet + Leaflet.heat + Chart.js, ohne Backend.
- Scope: Unabhängig von Python‑Pipeline; nutzt öffentliche APIs (World Bank/OWID/OECD/WHO) mit lokalem Cache (1h TTL).
- Implementiert: Status‑Quo‑Heatmap (OWID/WorldBank), IMP‑Choropleth mit WGI‑Proxies (RL.EST/VA.EST/GE.EST) und Legende.
- Quick start:
  - `cd web/5d-map && python3 -m http.server 5500`
  - Öffnen: `http://localhost:5500`, Layer‑Buttons: „Status Quo“, „Alternative Schulen“, „IMP‑Score“.
  - Zeitreise: Button „Zeitreise“, Slider erscheint; Baseline (`data/baseline.json`) für feste Ausgangswerte.

Referenzen: `5d_extractor.py`, `5d_dashboard.py`, `5d_research_scraper.py`, `5d_github_api.py`, `5d_discord_bot.py`, `models/schemas.py`, `models/imp.py`, `config/default.yaml`, `tests/`.
