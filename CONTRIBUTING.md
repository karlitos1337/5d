# Contributing to 5D Intelligence Framework

Vielen Dank für dein Interesse am 5D-Projekt! Wir freuen uns über Beiträge jeder Art: Code, Dokumentation, Bug Reports, Feature Requests oder wissenschaftliche Diskussionen.

## 📋 Inhaltsverzeichnis

- [Code of Conduct](#code-of-conduct)
- [Erste Schritte](#erste-schritte)
- [Entwicklungsumgebung](#entwicklungsumgebung)
- [Projektstruktur](#projektstruktur)
- [Workflow](#workflow)
- [Code-Standards](#code-standards)
- [Testing](#testing)
- [Dokumentation](#dokumentation)
- [Pull Requests](#pull-requests)
- [Issue Guidelines](#issue-guidelines)

## 🤝 Code of Conduct

- **Respektvoll:** Konstruktive Kritik, keine persönlichen Angriffe
- **Wissenschaftlich:** Behauptungen mit Quellen belegen
- **Inklusiv:** Alle Perspektiven sind willkommen
- **Open Source:** Teile dein Wissen

## 🚀 Erste Schritte

### 1. Repository forken

```bash
# Fork auf GitHub erstellen, dann:
git clone https://github.com/DEIN-USERNAME/5d.git
cd 5d
git remote add upstream https://github.com/karlitos1337/5d.git
```

### 2. Dev Container (empfohlen)

Das Projekt nutzt VS Code Dev Containers:

```bash
# In VS Code: "Reopen in Container"
# Oder lokal:
pip install -r requirements_extended.txt
```

### 3. Erste Tests

```bash
# Pipeline testen
python 5d_extractor.py
python 5d_research_scraper.py
python 5d_github_api.py

# Tests ausführen
pytest tests/ -v

# Dashboard starten
streamlit run 5d_dashboard.py
```

## 🛠️ Entwicklungsumgebung

### Erforderlich

- **Python:** 3.10+
- **Git:** 2.x
- **Editor:** VS Code (mit Dev Container Support) oder ähnlich

### Optional

- **GitHub Token:** Für höhere API Rate Limits
- **Discord Token:** Für Bot-Testing

```bash
export GITHUB_TOKEN=ghp_your_token
export DISCORD_TOKEN=your_discord_token
```

### Dependencies

```bash
# Minimal
pip install -r requirements.txt

# Erweitert (Dashboard, Visualisierung)
pip install -r requirements_extended.txt
```

## 📁 Projektstruktur

```
5d/
├── manifest/               # Human-curated knowledge base
├── formeln/                # Scientific formulas (001-157)
├── config/                 # Configuration (default.yaml)
├── models/                 # Pydantic schemas + IMP calculation
├── analysis/               # Data analysis scripts
├── surveys/                # Survey questions with citations
├── storage/                # Anonymization (GDPR)
├── web/5d-map/             # Interactive world map
├── tests/                  # Pytest test suite
├── docs/                   # Documentation
├── 5d_extractor.py         # Stage 1: Manifest extraction
├── 5d_research_scraper.py  # Stage 2: Academic papers
├── 5d_github_api.py        # Stage 3: GitHub repos
└── 5d_dashboard.py         # Main Streamlit dashboard
```

### Wichtige Dateien

| Datei | Zweck | Ändern wenn... |
|-------|-------|---------------|
| `models/schemas.py` | Pydantic validation | JSON-Schema ändert sich |
| `models/imp.py` | IMP calculation | Formel angepasst wird |
| `config/default.yaml` | Configuration | Neue Parameter hinzukommen |
| `.github/copilot-instructions.md` | AI agent guide | Architektur ändert sich |

## 🔄 Workflow

### Branch-Strategie

```bash
# Feature Branch erstellen
git checkout -b feature/deine-feature

# Oder für Bugfixes
git checkout -b fix/bug-beschreibung

# Oder für Dokumentation
git checkout -b docs/update-readme
```

### Commit Messages

Wir folgen [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: <type>(<scope>): <subject>

# Beispiele:
git commit -m "feat(extractor): add PDF extraction support"
git commit -m "fix(dashboard): resolve caching issue"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(pipeline): add integration tests"
git commit -m "refactor(models): simplify IMP calculation"
git commit -m "chore(deps): update plotly to 5.18.0"
```

**Types:**
- `feat`: Neues Feature
- `fix`: Bugfix
- `docs`: Dokumentation
- `test`: Tests
- `refactor`: Code-Refactoring
- `chore`: Maintenance (Dependencies, Config)
- `perf`: Performance-Verbesserung

### Sync mit Upstream

```bash
git fetch upstream
git rebase upstream/main
```

## 💻 Code-Standards

### Python (PEP 8)

```python
# ✅ Good
def calculate_imp(dimensions: dict[str, float]) -> float:
    """Calculate IMP score from 5 dimensions.
    
    Args:
        dimensions: Dict with keys A, IM, R, SP, Au (values 0-1)
    
    Returns:
        Multiplicative IMP score (0-1)
    """
    return (
        dimensions['A'] * 
        dimensions['IM'] * 
        dimensions['R'] * 
        dimensions['SP'] * 
        dimensions['Au']
    )

# ❌ Bad
def calc(d):
    return d['A']*d['IM']*d['R']*d['SP']*d['Au']
```

### Configuration over Hardcoding

```python
# ❌ Bad
manifest_dir = "manifest"

# ✅ Good
from config.loader import load_config
config = load_config()
manifest_dir = config['extractor']['manifest_dir']
```

### Streamlit Caching

```python
# ✅ Always cache expensive operations
@st.cache_data(ttl=300)
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### API Rate Limiting

```python
# ✅ Good
import time

class APIScraper:
    def __init__(self, rate_limit_delay=1.0):
        self.rate_limit_delay = rate_limit_delay
    
    def fetch(self, url):
        time.sleep(self.rate_limit_delay)
        return requests.get(url)
```

## 🧪 Testing

### Tests ausführen

```bash
# Alle Tests
pytest tests/ -v

# Spezifisches Modul
pytest tests/test_extractor.py -v

# Mit Coverage
pytest tests/ --cov=. --cov-report=html

# Nur schnelle Tests (ohne Integration)
pytest tests/ -m "not integration"
```

### Neuen Test schreiben

```python
# tests/test_neues_feature.py
import pytest
from models.schemas import DimensionScore

def test_dimension_score_normalization():
    """Test score normalization to [0, 1] range."""
    # Arrange
    score = DimensionScore(dimension='A', score='3.5', source='test')
    
    # Act
    normalized = score.score
    
    # Assert
    assert 0.0 <= normalized <= 1.0
    assert isinstance(normalized, float)
```

### Test-Kategorien

- **Unit Tests:** Einzelne Funktionen isoliert testen
- **Integration Tests:** Pipeline-Stages zusammen testen
- **E2E Tests:** Vollständiger Workflow

### Pre-Commit Hook

Tests laufen automatisch vor jedem Commit:

```bash
# Manuell triggern
pytest tests/
```

## 📝 Dokumentation

### Docstrings

```python
def calculate_5d_scores(responses: dict) -> dict:
    """Calculate 5D intelligence profile from survey responses.
    
    Args:
        responses: Dict mapping question IDs to Likert values (1-5)
    
    Returns:
        Dict with keys:
            - dimension_scores: Dict[str, float] (normalized 0-1)
            - aggregate_score: float (mean across dimensions)
            - completeness: float (% questions answered)
    
    Raises:
        ValueError: If responses contain invalid Likert values
    
    Example:
        >>> scores = calculate_5d_scores({'neuro_1': 4, 'psych_2': 5})
        >>> scores['aggregate_score']
        0.75
    """
```

### README Updates

Wenn du Features hinzufügst, update:

1. `README.md` – Hauptdokumentation
2. `docs/USER_GUIDE.md` – User-facing docs
3. `.github/copilot-instructions.md` – AI agent guide

### Wissenschaftliche Quellen

**Immer BibTeX-Keys verwenden:**

```python
QUESTIONS = [{
    "id": "neuro_flow",
    "question": "Wie häufig erleben Sie Flow?",
    "reference": "Csikszentmihalyi, M. (1990). Flow Theory.",
    "bibtex_key": "csikszentmihalyi1990flow"  # Must exist in 5d-relevant-sources.bib
}]
```

## 🔀 Pull Requests

### Vor dem PR

- [ ] Tests bestehen (`pytest tests/`)
- [ ] Code ist formatiert (PEP 8)
- [ ] Dokumentation aktualisiert
- [ ] Commit Messages folgen Convention
- [ ] Branch ist aktuell (`git rebase upstream/main`)

### PR-Template

```markdown
## Beschreibung
Kurze Zusammenfassung der Änderungen.

## Typ
- [ ] Bugfix
- [ ] Feature
- [ ] Dokumentation
- [ ] Refactoring

## Checklist
- [ ] Tests hinzugefügt/aktualisiert
- [ ] Dokumentation aktualisiert
- [ ] Keine Breaking Changes
- [ ] Pre-Commit Hook getestet

## Breaking Changes
Liste, falls vorhanden.

## Screenshots
Falls UI-Änderungen.
```

### Review-Prozess

1. **Automatische Checks:** GitHub Actions CI
2. **Code Review:** Mindestens 1 Approval
3. **Merge:** Squash & Merge bevorzugt

## 🐛 Issue Guidelines

### Bug Report

```markdown
**Beschreibung:**
Klare Beschreibung des Bugs.

**Reproduktion:**
1. Schritt 1
2. Schritt 2
3. ...

**Erwartetes Verhalten:**
Was sollte passieren?

**Tatsächliches Verhalten:**
Was passiert stattdessen?

**Umgebung:**
- OS: Ubuntu 24.04
- Python: 3.10.12
- Browser: Chrome 120 (falls relevant)

**Logs/Screenshots:**
Falls verfügbar.
```

### Feature Request

```markdown
**Problem:**
Welches Problem löst das Feature?

**Vorgeschlagene Lösung:**
Wie könnte das Feature aussehen?

**Alternativen:**
Andere Ansätze?

**Kontext:**
Zusätzliche Informationen.
```

## 🎯 Spezielle Guidelines

### Scientific Rigor Checklist

Bei neuen Features **immer** adressieren:

1. **Wissenschaftliche Basis:** Info-Box mit Zitation
2. **Validierungsstatus:** Badge ("Eigene Forschung" vs "Peer-Reviewed")
3. **Datenquelle:** Link + Download-Button
4. **User-Fragen:** FAQ erweitern
5. **UI-Klarheit:** 50-UI-Tips prüfen

### Data Privacy (GDPR)

```python
# ✅ Always anonymize personal data
from storage.anonymize import anonymize_response

def save_survey(response_data):
    anonymized = anonymize_response(response_data)
    # NO: username, email, IP, github_id
    # YES: anonymous_id, responses, timestamp
```

### JSON Schema Evolution

```python
# 1. Update models/schemas.py
class NewField(BaseModel):
    value: float = Field(..., ge=0.0)

# 2. Update producer scripts (5d_extractor.py)
# 3. Update consumer scripts (5d_dashboard.py)
# 4. Add backward compatibility tests
```

## 📞 Kontakt

- **Issues:** GitHub Issues
- **Diskussionen:** GitHub Discussions
- **Website:** [reflexionsfabrik.de](https://reflexionsfabrik.de)

## 🙏 Danke!

Jeder Beitrag zählt – ob Code, Dokumentation, Bug Reports oder Ideen. Vielen Dank, dass du Teil der 5D-Community bist!

---

**Version:** 2.0  
**Last Updated:** December 2, 2025