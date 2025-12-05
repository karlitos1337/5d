# 5D Intelligence Framework – AI Agent Instructions

**Version:** 4.0 (Streamlined Architecture Guide)  
**Last Updated:** 2025-12-03  
**Goal:** Help AI agents be immediately productive with scientific rigor

---

## 🏗️ Core Architecture

### Data Pipeline (Sequential Flow)
```
# Copilot/Agent Guidance — 5d (Kurzfassung)

Zweck: Kurzes, handlungsorientiertes Leitblatt für AI-Coding‑Agenten, damit Änderungen schnell korrekt, testsicher und reproducible sind.

**Kernaussagen (Big Picture)**
- Pipeline: `5d_extractor.py` → `5d_research_scraper.py` → `5d_github_api.py` → JSON artifacts → `5d_dashboard.py` (Streamlit pages in `pages/`).
- Stabiler Vertrag: `d5_solutions.json`, `d5_research_data.json`, `d5_github_data.json` sind das Interface zwischen Schritten — niemals JSON-Schlüssel ohne Koordination umbenennen.

**Wichtige Dateien & Komponenten**
- `models/schemas.py`: zentrale Pydantic-Validierung. Änderungen hier erfordern Tests und ggf. Migrationsschritte für JSON-artifacts.
- `config/default.yaml`: alle konfigurierbaren Werte; vermeide Hardcoding.
- `web/5d-map/`: statische Leaflet‑Map (serve mit `python3 -m http.server 5500`).
- `start.sh` / `Makefile`: Standardworkflow zum Starten der Pipeline/Dev‑Umgebung.

**Konkrete Workflows / Kommandos**
- Dev-Setup: `pip install -r requirements_extended.txt`.
- Full run: `./start.sh` (Extraktion → Scraper → GitHub API → Dashboard). Alternativ: `make start`.
- Tests: `pytest tests/ -v` oder `make test`.
- Map lokal: `cd web/5d-map && python3 -m http.server 5500` oder `make serve-map`.

**Projekt-spezifische Regeln (unbedingt befolgen)**
- Evidence Labels: Jede Änderung mit inhaltlicher Behauptung braucht ein Evidence-Label (✅ Fakt, ⚠️ Hypothese, 🔮 Spekulation) und, falls möglich, eine BibTeX‑Quelle aus `07_daten_analysen/5d-relevant-sources.bib`.
- Schema-First: Neue JSON-Felder → zuerst `models/schemas.py` anpassen, dann Tests in `tests/` schreiben, dann Pipeline-Anpassungen.
- FAQ: Änderungen, die Datenherkunft betreffen, erfordern ein Update von `docs/FAQ.md`.

**Praktische Beispiele**
- Neue Feld hinzufügt: edit `models/schemas.py` → add test `tests/test_schema_xyz.py` → run `pytest` → update pipeline writer (`5d_extractor.py` / `5d_github_api.py`) → bump artifact contract in PR description.
- Map-Fehler debuggen: `cd web/5d-map && python3 -m http.server 5500` → Browser auf `http://localhost:5500` → prüfe `data/` JSONs und `config/default.yaml`.

**PR / Commit Hinweise für Agenten**
- Beschreibe im PR die veränderten JSON‑Keys, betroffene pipeline‑stufen und Tests. Beispiel-PR-Header: "schema: add `score_source` to Solutions — update extractor + tests (models/schemas.py, tests/test_solutions.py)".

Wenn etwas unklar ist oder Ergänzungen nötig sind, sag kurz Bescheid — ich iteriere die Datei gezielt nach deinem Feedback.

*** Ende Kurzfassung ***
    - ✅ Autonomy → IM (Deci & Ryan 1985, 1000+ studies)
