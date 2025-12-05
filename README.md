# 🧠 5D-Intelligence Framework

> A comprehensive, interdisciplinary approach to understanding and developing human intelligence through neurobiological, psychological, philosophical, economic, and technological perspectives.

## 🎯 What is 5D-Intelligence?

Traditional intelligence models are incomplete. The **5D-Intelligence Framework** integrates five essential dimensions:

- **🧬 Neurobiological Dimension**: Understanding cognitive processes at the neural level
- **💭 Psychological Dimension**: Exploring motivation, emotion, and social connection
- **🤔 Philosophical Dimension**: Critical examination of epistemology and consciousness
- **💰 Economic Dimension**: Decentralized governance and alternative incentive systems
- **⚡ Technological Dimension**: Innovative applications inspired by Tesla and quantum systems

## 📚 Documentation

This repository contains comprehensive documentation across multiple knowledge domains:

### Quick Navigation

- **[⭐ Executive Summary 2025](docs/EXECUTIVE_SUMMARY_2025.md)** - **NEW!** Complete framework overview with Week 1 research findings (92% A-, 54.2% facts)
- **[🎯 VISION.md](VISION.md)** - Central framework definition, 1D-5D complexity levels, scientific foundation
- **[🧪 Hypotheses Catalog](docs/HYPOTHESEN_KATALOG.md)** - 10 testable hypotheses with operationalization & abort criteria
- **[📐 1D-5D Definitions](docs/1D_5D_DEFINITIONEN.md)** - Complexity levels for 5 domains (Education, Governance, Mental Health, Ecology, Technology)
- **[🔬 Research Roadmap](TODO_RESEARCH.md)** - Scientific foundations, empirical testability, open questions (85+ tasks)
- **[📊 Manifest Summary](docs/manifest_summary.md)** - Hierarchical overview of all project documents (7578 lines, academic synthesis)
- **[📖 Wiki Home](wiki/)** - Complete 5D-Intelligence overview with detailed glossary
- **[💡 Concepts & Definitions](wiki/Home)** - Detailed explanations of key terms
- **[📚 Docs Index](docs/README.md)** - Local documentation index and quickstarts

## 🗂️ Project Structure

```
01_bildung_education/        # Educational philosophy & decentralized learning systems
02_neurobiologie_psychologie/ # Neuroscience & psychological foundations
03_philosophie_epistemologie/ # Philosophical & epistemological inquiry
04_oekonomie_governance/      # Economic models & governance systems
05_technologie_tesla/         # Technological innovation & resonance
06_synthesen_kompilationen/   # Cross-domain syntheses
07_daten_analysen/            # Data analysis & research
08_personal_biografie/        # Personal development & reflections
99_unsortiert/                # Emerging ideas & work-in-progress
```

## 🚀 Getting Started

### For Researchers
1. Review the [Manifest Summary](manifest_summary.md) for project overview
2. Explore specific domains in numbered folders (01-08, 99)
3. Check the [Wiki](wiki/) for conceptual framework

### For Educators
- Focus on `01_bildung_education/` for pedagogical applications
- Explore intrinsic motivation research in `02_neurobiologie_psychologie/`
- See governance alternatives in `04_oekonomie_governance/`

### For Philosophers
### Weltkarte (MVP)
- Interaktive Karte mit Heatmap, IMP‑Choropleth, Schulen, Validierungsring, Quellen‑Layer & Zeitreise.
- Schnellstart:
	```bash
	cd web/5d-map
	python3 -m http.server 5500
	$BROWSER http://localhost:5500
	```
- Details: `web/5d-map/README.md` · Kurz‑Anweisung: `md_copilot_ki_anweisung`
 - Validierung & Quellen: `docs/VALIDATION_AND_SOURCES.md`

#### Datenvalidierung (CI)
- GitHub Action: `.github/workflows/validate-5d-metadata.yml`
- Validiert JSON‑Artefakte und Metadaten (Schema, Schlüssel, Vollständigkeit)
- Trigger: PRs auf `main` und Änderungen in `manifest/`, `models/`, `web/5d-map/data/`
- Lokal prüfen:
	```bash
	pytest tests/ -k "metadata|world_map_data" -v
	```
- Ergebnisse erscheinen als PR‑Check. Bei Fehlern: Logs prüfen und Keys gemäß `models/schemas.py` korrigieren.

#### Google Drive als Datenquelle
- Optionaler Import via `gdown` (siehe `scripts/import_drive.py`).
- Schnellstart:
	```bash
	# einmalig
	pip install gdown
	# Ordner importieren
	python scripts/import_drive.py --folder "https://drive.google.com/drive/folders/1Kzwry6SfWY_HWx9L5zh52jAR-qdeP1QT?usp=sharing"
	```
- Automatisch im Startskript, wenn `DRIVE_FOLDER` gesetzt ist:
	```bash
	DRIVE_FOLDER="https://drive.google.com/drive/folders/1Kzwry6SfWY_HWx9L5zh52jAR-qdeP1QT?usp=sharing" ./start.sh
	```
- Mapping:
  - `03_philosophie_epistemologie/*.md` → `03_philosophie_epistemologie/`
  - `06_synthesen_kompilationen/*.md` → `06_synthesen_kompilationen/`
  - `web/5d-map/data/*.json` → `web/5d-map/data/`
  - `07_daten_analysen/*.bib` → `07_daten_analysen/`

## 🛠 Dev Quickstart

These commands help developers run the main pipeline and preview the UI locally.

Install dependencies:
```bash
pip install -r requirements_extended.txt
```

Make the starter script executable and run it (runs extractor, scrapers and UI servers):
```bash

```

Alternatively use `make`:
```bash
make start   # runs ./start.sh
make test    # runs pytest
make serve-map  # serves web/5d-map on port 5500
```

- Epistemological foundations in `03_philosophie_epistemologie/`
- Systems theory applications in `06_synthesen_kompilationen/`

## 📊 Repository Activity

- **67 Clones** in the last 14 days
- **70 Views** in the last 14 days
- Active development & documentation

## 🔗 External Resources

- **[reflexionsfabrik.de](https://reflexionsfabrik.de)** - Personal research documentation
- **[Wiki Pages](wiki/)** - Interactive glossary and detailed explanations

## 🤝 Contributing

This project thrives on intellectual exchange and critical discussion. We welcome feedback, contributions, and cross-disciplinary insights.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Roadmaps

- **[TODO.md](TODO.md)** - Infrastructure, deployment, CI/CD tasks (13/15 complete, 87%)
- **[TODO_MULTIPAGE.md](TODO_MULTIPAGE.md)** - Dashboard features, UI/UX, scientific validation (10/10 pages, 100%)
- **[TODO_RESEARCH.md](TODO_RESEARCH.md)** - Scientific foundations, empirical testability, theoretical coherence (85+ tasks)
- **[Research Agenda 2026-2028](08-experimente-validierung/experiments/research_agenda.md)** - ⭐ **GESAMTZIEL:** 7 Experimente (1 Woche bis 2 Jahre) - AI-Simulation, Meta-Survey, Bildung-RCT, Neuro-EEG

### Scientific Documentation

- **[EXECUTIVE_SUMMARY_2025.md](docs/EXECUTIVE_SUMMARY_2025.md)** - ⭐ **NEW!** Comprehensive overview with Week 1 research (341 lines, all findings integrated)
- **[CLAIMS_EVIDENCE_MATRIX.md](docs/CLAIMS_EVIDENCE_MATRIX.md)** - 48 claims with evidence labels (54.2% Facts, 35.4% Hypotheses, 10.4% Speculations, 1 falsified)
- **[ETHIK_MANIFEST.md](ETHIK_MANIFEST.md)** - Bias log (13 biases: WEIRD, Power, Publication ⭐), abort criteria, research ethics
- **[HYPOTHESEN_KATALOG.md](docs/HYPOTHESEN_KATALOG.md)** - 10 testable hypotheses (H1-H10 with operationalization, methods, timeline)
- **[1D_5D_DEFINITIONEN.md](docs/1D_5D_DEFINITIONEN.md)** - Complexity levels for 5 domains (Education, Governance, Mental Health, Ecology, Technology)

## 🧬 Why This Matters

Intelligence isn't fixed. It's not measured by a single number. It's:
- **Dynamic** - constantly evolving through experience
- **Multidimensional** - cognitive, emotional, social, embodied
- **Contextual** - situated in specific environments and cultures
- **Generative** - capable of creating new knowledge and meaning

The 5D-Intelligence Framework provides a roadmap for unleashing human potential.

---

**Last Updated**: December 3, 2025  
**Status**: Active Development  
**Framework Status**: 92% (A-) - 54.2% Facts, 35.4% Hypotheses, 10.4% Speculations

*For detailed information, explore the [Wiki](wiki/) or visit [reflexionsfabrik.de](https://reflexionsfabrik.de)*
