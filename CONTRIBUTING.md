# CONTRIBUTING

Kurzleitfaden für Beiträge zum 5D‑Projekt.

- Stil & Qualität
  - PEP 8, lesbare Namen, keine Seiteneffekte in Reinfunktionen.
  - Nutze `black`, `ruff`, `mypy` (siehe `pyproject.toml`).
- Struktur
  - Kerncode unter `src/universal_system_genesis_5d/`.
  - Daten unter `data/` (roh/processed/meta). Keine personenbezogenen Daten.
- Tests
  - Pytest unter `tests/`. Schreibe Tests für neue zentrale Funktionen.
- Pre‑Commit
  - Installiere Hooks: `pre-commit install` oder `./scripts/uv_run.ps1 -Hook`.
  - Vor dem Commit lokal `./scripts/uv_run.ps1 -Tests` laufen lassen.
- CI
  - PRs sollten lokal lint/format/type/tests bestehen. CI prüft das ebenfalls.

Danke für sorgfältige, nachvollziehbare Beiträge!