# CHANGELOG

Alle nennenswerten Änderungen werden hier dokumentiert. Format basiert auf Keep a Changelog; Versionierung folgt Semantic Versioning.

## [2.5.0] - 2025-12-02

### Added - Dashboard Pages (Phase 1 Complete: 10/10)
- **Page 9:** Autopoietic Class simulation (509 lines)
  - Agent-based 5D dynamics with dropout prediction
  - 7 parameters: coercion, freedom, peers, teacher support, task diversity
  - Visualizations: evolution bands, trajectories, dropout events
  - Scientific basis: Maturana & Varela 1980, Deci & Ryan 1985
- **Page 10:** Participation Networks (460 lines)
  - 3 network topologies: Erdős-Rényi, Watts-Strogatz, Barabási-Albert
  - Knowledge diffusion simulation with threshold model
  - IMP proxies: SP (clustering), R (diffusion speed), IM (sharing)
  - Scientific basis: Granovetter 1973, Watts & Strogatz 1998, Barabási & Albert 1999

### Added - Mini-Maps (Phase 3 Complete: 7/7)
- Interactive Folium maps on all geographic pages
- Consistent styling: 700x350px, CartoDB positron tiles
- `utils/map_helpers.py`: 5 reusable map functions + render wrapper
- Maps: IMP Analysis, Projects, Research, GitHub, Non-Coercion, World Map, Projections

### Added - App Integration (Phase 4 Complete: 4/4)
- Integrated `gol_streamlit.py` → Page 5 (Game of Life, 666 lines)
- Integrated `zwi_streamlit.py` → Page 6 (Non-Coercion, 106 lines)
- Integrated `autopoietic_streamlit.py` → Page 9 (509 lines)
- Integrated `partnet_streamlit.py` → Page 10 (460 lines)

### Added - Scientific Tests (Phase 8 Extended: 9/9 files, 151/151 passing)
- `test_projects.py`: 12 tests (Heckman NPV, alternative education)
- `test_research_sources.py`: 16 tests (arXiv/PubMed API compliance)
- `test_github_metrics.py`: 14 tests (activity score, CHAOSS/OpenSSF)
- `test_game_of_life.py`: 21 tests (Conway rules, Turing completeness)
- `test_non_coercion.py`: 24 tests (Nash equilibrium, Ostrom principles)
- `test_world_map_data.py`: 20 tests (IMP-proxy formula, IHME/WB/WGI)
- `test_projections.py`: 27 tests (logistic curves, Rogers diffusion)
- `test_participation_networks.py`: 16 tests (network topology, weak ties, diffusion)
- **Total:** 161 scientific tests (11+12+16+14+21+24+20+27+16)

### Added - BibTeX References (59 entries, Batch 4-6)
- **Batch 4 (12 entries):** Game of Life, Cooperation, Diffusion
  - Conway 1970, Gardner 1970, Wolfram 2002, Rendell 2016
  - Ostrom 1990, Axelrod 1984, Nash 1950, Hardin 1968
  - Rogers 2003, Bass 1969, Verhulst 1838, Moore 1991
- **Batch 5 (6 entries):** Global Data Sources
  - IHME GBD 2019, World Bank EdStats, WGI, OECD BLI, UNDP HDI, World Happiness 2024
- **Batch 6 (3 entries):** Network Theory
  - Granovetter 1973, Watts & Strogatz 1998, Barabási & Albert 1999

### Added - Utility Modules
- `utils/bibtex_helpers.py`: BibTeX display with copy-to-clipboard (150+ lines)
- `utils/export_helpers.py`: Standardized JSON/CSV/TXT export for simulations (200+ lines)

### Changed
- Dashboard metrics updated: 10 pages, 59 sources, 161 tests (151/151 passing)
- Navigation: Added Page 9 (Autopoietic Class) and Page 10 (Participation Networks)
- Documentation: Updated TODO_MULTIPAGE.md, copilot-instructions.md to version 2.5

### Fixed
- Floating-point assertions in `test_participation_networks.py` (abs() tolerance)
- Test count consistency across all documentation files

### Statistics
- **Commits:** 41 commits in session (2025-12-02)
- **Lines Added:** ~4,500+ lines (pages, tests, utilities)
- **Test Coverage:** 151/151 scientific tests passing (100%)
- **Documentation:** 3 major files updated (TODO, copilot-instructions, CHANGELOG)

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
