## 5d – Copilot Arbeitsregeln (AI Coding Agents)

Ziel: Schnell produktiv arbeiten, ohne die projekt­spezifischen Datenflüsse oder Dateischnittstellen zu brechen. Beziehe dich auf konkrete Dateien und bestehende Muster in diesem Repo.

### Big Picture Architektur
- Komponenten: `5d_extractor.py` (Manifest-Parser) → `5d_research_scraper.py` (arXiv/PubMed) → `5d_github_api.py` (GitHub Suche) → JSON Outputs → `5d_dashboard.py` (Streamlit) + optional `5d_discord_bot.py` (Discord Commands).
- Orchestrierung: `RUN_ALL.sh` führt die Schritte in Reihenfolge aus und startet das Dashboard.
- Datenfluss/Artefakte:
  - `5d_solutions.json` aus Extractor
  - `5d_research_data.json` aus Research-Scraper
  - `5d_github_data.json` aus GitHub-Explorer
  - Dashboard/Bot lesen diese JSONs und degradieren bei fehlenden Dateien mit Platzhaltern.

### Setup & Workflows
- Environment: Python 3.10+ empfohlen. Install:
  ```bash
  pip install -r requirements_extended.txt
  ```
- Optional Tokens: `export GITHUB_TOKEN=...` (höhere GitHub Rate-Limits), `export DISCORD_TOKEN=...` (für Bot).
- Komplettlauf:
  ```bash
  chmod +x RUN_ALL.sh
  ./RUN_ALL.sh
  ```
- Einzelne Schritte:
  ```bash
  python 5d_extractor.py
  python 5d_research_scraper.py
  python 5d_github_api.py
  streamlit run 5d_dashboard.py
  # Discord-Bot (separat, benötigt DISCORD_TOKEN):
  python 5d_discord_bot.py
  ```

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
- Extractor (`5d_extractor.py`):
  - Scannt aktuell nur `manifest/*.md` (Top-Level) via `glob("*.md")`. Wenn Unterordner aus `manifest/` berücksichtigt werden sollen, ersetze durch `rglob("*.md")` und prüfe Performance.
  - Regex-basiert für Projekte/ROI/Pilots; IMP-Keywords in `self.imp_keywords`. Erweiterungen dort hinzufügen.
- Research-Scraper (`5d_research_scraper.py`):
  - arXiv (Atom/XML via BeautifulSoup) und PubMed (E-Utilities JSON). 10s Timeout, `time.sleep(1)` Rate-Limit – bitte beibehalten/skalieren statt entfernen.
  - Keywords in `self.keywords`. Neue Themen hier ergänzen und in `scrape_all()` nutzen.
- GitHub-Explorer (`5d_github_api.py`):
  - `search_queries` definieren die Suchen. Optionaler `GITHUB_TOKEN` in Header für Rate-Limits.
  - `get_trending_topics()` speichert zusätzliche Daten; Dashboard nutzt derzeit primär `repositories`.

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
- Verwandte Repos: `universal-system-genesis-5d`, `resonance-formula-5d-intelligence` (Formeln/System-Genesis & Resonanz-/Intelligenzformeln).
- Einbindung (empfohlen): Als Git Submodule unter `external/`:
  ```bash
  mkdir -p external
  git submodule add https://github.com/karlitos1337/universal-system-genesis-5d.git external/system-genesis
  git submodule add https://github.com/karlitos1337/resonance-formula-5d-intelligence.git external/resonance-formulas
  ```
- Konsistenz: Änderungen nur ergänzend; vorhandene lokale `formeln/` und `manifest/` Strukturen nicht überschreiben.
- Extraktion erweitern: `FiveDExtractor(manifest_dir="manifest")` kann parametriert werden oder zusätzliche Läufe über `external/**` (separat ausführen und Ergebnisse mergen, z. B. `solutions_external.json`).
- Merge-Strategie JSON: Neue Felder prefixed (`ext_resonanz_*`) statt vorhandene Keys ersetzen.
- Resonanz-/Genesis-Formeln nicht direkt in IMP-Scores mischen ohne Mapping-Dokument (`mapping_resonance_imp.md` optional anlegen).
- Bei Updates der Submodules: `git submodule update --remote --merge` regelmäßig ausführen; niemals lokal modifizierte fremde Formeln zurückpushen ohne Abstimmung.
 - Automatischer Merge: Skript `merge_external_solutions.py` erzeugt `solutions_external.json` + `5d_solutions_merged.json` (nicht-invasiv, externe Felder unter `external`).
 - Mapping von Resonanz → IMP: Vorlage `mapping_resonance_imp.md` nutzen; keine direkten Überschreibungen von Kern-Scores.
 - Optionaler Workflow (nach Submodule-Update):
   ```bash
   python 5d_extractor.py
   python merge_external_solutions.py
   streamlit run 5d_dashboard.py
   ```
