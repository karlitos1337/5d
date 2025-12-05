# 5D Intelligence Framework – Copilot Instructions (Kurzfassung)

Ziel: Sofort produktiv werden mit klaren, projekt‑spezifischen Leitplanken. Fokus auf echte Workflows, stabile Datenverträge und konkrete Beispiele aus diesem Repo.

## Big Picture
- Pipeline: `5d_extractor.py` → `5d_research_scraper.py` → `5d_github_api.py` → JSON‑Artefakte → `5d_dashboard.py` (Streamlit, Seiten in `pages/`).
- Artefakt‑Vertrag: `5d_solutions.json`, `5d_research_data.json`, `5d_github_data.json` sind die Schnittstelle zwischen Schritten. JSON‑Keys niemals umbenennen ohne Schema‑Update + Tests.
- Visualisierung: `web/5d-map/` (Leaflet, statisch). Dashboard rendert ausschließlich aus JSON‑Artefakten.

## Schlüsselkomponenten
- `models/schemas.py`: Pydantic‑Validierung für Artefakte. Schemaänderungen → neue Tests in `tests/`, Pipeline Writer anpassen.
- `config/default.yaml`: Alle konfigurierbaren Werte. Keine Hardcodes in Pipeline‑Skripten.
- `5d_dashboard.py` + `pages/`: Multipage‑App, externe Templates via `st.components.v1.html` möglich (z. B. `web/templates/5d_forschungsplanung.html`).

## Setup & Lauf
- Dev‑Setup: `pip install -r requirements_extended.txt`.
- Full Run: `./start.sh` oder `make start` (führt Extraktion → Scraper → GitHub API → Dashboard).
- Tests: `pytest tests/ -v` oder `make test`.
- Map lokal: `cd web/5d-map && python3 -m http.server 5500` (oder `make serve-map`).
- Dashboard lokal: `streamlit run 5d_dashboard.py` (oder `./start.sh`).

## Projektregeln (verbindlich)
- Evidence Labels in inhaltlichen Änderungen: ✅ Fakt, ⚠️ Hypothese, 🔮 Spekulation; möglichst Quelle aus `07_daten_analysen/5d-relevant-sources.bib`.
- Schema‑First: Neue JSON‑Felder immer zuerst in `models/schemas.py` definieren, dann Tests schreiben, dann die schreibenden Pipeline‑Schritte anpassen.
- Datenherkunft: Änderungen mit Herkunftsimpact erfordern Update von `docs/FAQ.md`.

## Arbeitsmuster (konkrete Beispiele)
- Neues Feld: `models/schemas.py` editieren → Test z. B. `tests/test_solutions_schema.py` ergänzen → `pytest` → Writer in `5d_extractor.py`/`5d_github_api.py` anpassen → PR‑Beschreibung: betroffene JSON‑Keys + Stufen.
- Map Debug: `cd web/5d-map && python3 -m http.server 5500` → Browser `http://localhost:5500` → prüfe `web/5d-map/data/*.json` und `config/default.yaml`.
- Neue Seite: `pages/<order>_<emoji>_<Name>.py` erstellen, `st.set_page_config(...)` setzen, optional Template via `st.components.v1.html` laden; Link in Sidebar per `st.page_link(...)`.

## Konventionen & Patterns
- JSON nur über definierte Artefakte lesen/schreiben; keine stillen Schema‑Abweichungen in `pages/`.
- Befehle über `Makefile`/`start.sh` bevorzugen; CI spiegelt diese Flows.
- Python‑Stil konsistent halten; keine Lizenz‑Header hinzufügen; minimalinvasive Änderungen.

## Quick‑Refs (Dateien/Dirs)
- `5d_extractor.py`, `5d_research_scraper.py`, `5d_github_api.py` – Pipeline Writer/Fetcher.
- `models/schemas.py` – Vertrag/Validierung.
- `config/default.yaml` – Konfiguration.
- `5d_dashboard.py`, `pages/` – UI.
- `web/5d-map/`, `web/templates/` – statische Map/HTML Templates.
- `tests/` – Schema/Workflow‑Tests.

Unklarheiten oder Lücken? Kurze Rückmeldung geben – ich iteriere diese Datei gezielt und halte sie synchron mit Änderungen in Schema, Pipeline und Dashboard.
