## 5d – Copilot Arbeitsregeln (AI Coding Agents)

Ziel: Schnell produktiv arbeiten, ohne die projekt­spezifischen Datenflüsse oder Dateischnittstellen zu brechen. Beziehe dich auf konkrete Dateien und bestehende Muster in diesem Repo.

Wichtige Leitplanke: KEIN PrivateGPT/PGPT, keine RAG/LLM-Server-Setups in diesem Repo. Fokus: Kern‑5D‑Pipeline und Streamlit‑Frontends.

### Big Picture Architektur
- **Daten-Pipeline**: `5d_extractor.py` (Manifest-Parser) → `5d_research_scraper.py` (arXiv/PubMed) → `5d_github_api.py` (GitHub Suche) → JSON Outputs
- **Frontends**: `5d_dashboard.py` (Hauptdashboard), `autopoietic_streamlit.py`, `zwi_streamlit.py`, `gol_streamlit.py`, `partnet_streamlit.py` (Simulationen)
- **Integration**: Optional `5d_discord_bot.py` (Discord Commands)
- **Orchestrierung**: `RUN_ALL.sh` führt die Hauptpipeline aus und startet das Dashboard
- **Datenfluss/Artefakte**:
  - `5d_solutions.json` aus Extractor (validiert via `models/schemas.py`)
  - `5d_research_data.json` aus Research-Scraper
  - `5d_github_data.json` aus GitHub-Explorer
  - `solutions_external.json` + `5d_solutions_merged.json` aus `merge_external_solutions.py` (Submodule-Daten)
  - `5d_solutions_adjusted.json` aus `apply_resonance_mapping.py` (optionale Resonanz-Mappings)
  - Dashboard/Bot lesen diese JSONs und degradieren graceful bei fehlenden Dateien

### Setup & Workflows
- **Environment**: Python 3.10+ empfohlen. Dev-Container: Ubuntu 24.04.3 LTS
- **Installation**:
  ```bash
  pip install -r requirements_extended.txt
  ```
- **Konfiguration**: YAML-basiert via `config/default.yaml` (lädt `config/loader.py`). Anpassungen dort statt Hardcoded Paths.
- **Env Tokens**: `export GITHUB_TOKEN=...` (höhere Rate-Limits), `export DISCORD_TOKEN=...` (für Bot)
- **Komplettlauf** (Pipeline + Dashboard):
  ```bash
  chmod +x RUN_ALL.sh
  ./RUN_ALL.sh
  ```
- **Einzelne Schritte**:
  ```bash
  python 5d_extractor.py              # Manifest-Parsing → 5d_solutions.json
  python 5d_research_scraper.py       # Research-Scraping → 5d_research_data.json
  python 5d_github_api.py             # GitHub-Suche → 5d_github_data.json
  streamlit run 5d_dashboard.py       # Hauptdashboard (Port 8501)
  streamlit run autopoietic_streamlit.py  # Autopoietische Simulation
  python 5d_discord_bot.py            # Bot (benötigt DISCORD_TOKEN)
  ```
- **Testing**:
  ```bash
  pytest tests/                        # Pytest-Suite mit Fixtures
  pytest tests/test_extractor.py -v   # Einzeltest
  ```
 

### Agent-Verhalten (Prompt-Kern)
- Kein Aufbau/Erwähnung von PrivateGPT, Ollama oder anderen externen RAG‑Stacks.
- Bevorzugte Tasks: Extractor, Research‑Scraper, GitHub‑Explorer, Dashboard, Simulationen, Merge‑Skripte.
- Änderungen minimal-invasiv: Schemas/JSONs kompatibel halten (additiv statt umbauen).
- Netzwerkzugriffe robust: Timeouts, Fehler fangen, leere Listen zurückgeben.
- Streamlit: Keine blockierenden Operationen im Renderpfad; I/O in `load_data()` kapseln.
- Visualisierungs‑Fallbacks nutzen (Plotly‑Alternativen sind in `5d_dashboard.py` enthalten).

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
