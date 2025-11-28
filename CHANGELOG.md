# CHANGELOG

Alle nennenswerten Änderungen werden hier dokumentiert. Format basiert auf Keep a Changelog; Versionierung folgt Semantic Versioning.

## [2.0.0] - 2025-11-28

### Added
- Pydantic-Schema für JSON-Validierung (`models/schemas.py`)
- PDF-Extraktion mit PyPDF2 im Extractor
- YAML-Konfiguration (`config/default.yaml`, `config/loader.py`)
- Pytest-Suite inkl. Discord-Bot-Tests
- CI Pipeline (`.github/workflows/test.yml`)
- Fuzzy Matching für Projektnamen
- Verifizierte IMP-Berechnung (`models/imp.py`) und Integration im Dashboard
- Dashboard: Manifeste-Tab mit Suche/Filter + externe Referenzen

### Fixed
- IMP-Berechnung transparent gemacht (0.52 statt 0.77)
- JSON Type-Inconsistency behoben (z. B. 'HIGH' → 0.75)
- Projekt-Deduplication (Mehrfacheinträge → zusammengeführt)

### Changed
- `5d_solutions.json` Format validiert und robuster
- `5d_dashboard.py` um IMP‑Transparenz und neue Tabs erweitert
- Alle Tools lesen Konfiguration statt Hardcoded Paths

### Notes
- Migration von alten `5d_solutions.json` empfohlen (v1 → v2). Ein eigenes Migrationsskript kann hinzugefügt werden.
