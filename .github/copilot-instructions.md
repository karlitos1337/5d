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
- **Git Workflow**: Pre-Commit Hook (`.git/hooks/pre-commit`) führt automatisch aus:
  - TODO-Liste Check (zeigt offene Tasks)
  - Python Syntax Validation
  - Flake8 Linting (non-blocking warnings)
  - Core Tests (pytest) - **blockiert bei Failures**
  - JSON Validation
  - Commits werden blockiert bei Test-Failures. TODO-Liste in `TODO.md` tracken.

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
- Sprache/Keys: Nutzer‑Facing in DE (z. B. `"Projekte"`, `"ROI"`, `"Pilots"`). Nicht umbenennen ohne UI/Bot‑Update.

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

---

## 🎯 Akademisches Erhebungsinstrument (NEU)

### Vision: 5D-Intelligence Survey Framework

Entwicklung eines **wissenschaftlich validierten Fragebogens** zur Erhebung multidimensionaler Intelligenz-Daten:

#### Kernprinzipien
1. **Absolute Anonymität**: GitHub OAuth nur als Zugangskontrolle, KEINE Speicherung personenbezogener Daten
2. **Akademische Validität**: Alle Fragen wissenschaftlich fundiert mit BibTeX-Quellen
3. **Interdisziplinarität**: 5 Dimensionen gleichwertig abgebildet
4. **DSGVO-Konformität**: Local-first, keine Cloud-Abhängigkeit, explizites Consent
5. **Open Science**: Alle Algorithmen, Formeln und Daten transparent

### Fragebogen-Architektur

#### Eingangsfragen (Demografisch, anonym)
```python
# surveys/entrance_questions.py
ENTRANCE_SCHEMA = {
    "employment_status": {
        "type": "select",
        "options": ["Angestellt", "Selbstständig", "Student", "Arbeitssuchend", "Rentner", "Sonstiges"],
        "required": True
    },
    "education_level": {
        "type": "select",
        "options": ["Kein Abschluss", "Hauptschule", "Realschule", "Abitur", "Bachelor", "Master", "Promotion"],
        "required": True
    },
    "postal_code": {
        "type": "number",
        "min": 10000,
        "max": 99999,
        "purpose": "Regional clustering (anonymized)"
    },
    "federal_state": {
        "type": "text",
        "max_length": 50
    },
    "country": {
        "type": "select",
        "source": "ISO_3166_countries",
        "default": "DE"
    },
    "life_satisfaction": {
        "type": "likert",
        "scale": [1, 2, 3, 4, 5, 6],  # Schulnoten-System
        "label": "Wie bewerten Sie Ihr aktuelles Leben insgesamt?",
        "reverse_coded": True  # 1=Sehr gut, 6=Ungenügend
    },
    "future_expectation": {
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "label": "Wie zuversichtlich blicken Sie in die Zukunft?"
    },
    "past_evaluation": {
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "label": "Wie bewerten Sie Ihre bisherige Lebensgeschichte?"
    },
    "financial_situation": {
        "type": "select",
        "options": ["Sehr gut", "Gut", "Befriedigend", "Ausreichend", "Schwierig"],
        "coding": {"Sehr gut": 5, "Gut": 4, "Befriedigend": 3, "Ausreichend": 2, "Schwierig": 1}
    }
}
```

#### 5D-Dimensionsfragen (Mindestens 10 pro Dimension)

##### 1D: Neurobiologisch
```python
# surveys/dimension_1_neurobiology.py
NEUROBIOLOGY_QUESTIONS = [
    {
        "id": "neuro_flow_frequency",
        "question": "Wie häufig erleben Sie Flow-Zustände (vollständiges Aufgehen in einer Tätigkeit)?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Nie", "Selten", "Manchmal", "Häufig", "Sehr häufig"],
        "reference": "Csikszentmihalyi, M. (1990). Flow: The Psychology of Optimal Experience.",
        "bibtex_key": "csikszentmihalyi1990flow"
    },
    {
        "id": "neuro_attention_span",
        "question": "Wie schätzen Sie Ihre Konzentrationsfähigkeit ein?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Posner, M. I., & Petersen, S. E. (1990). The attention system of the human brain.",
        "bibtex_key": "posner1990attention"
    },
    {
        "id": "neuro_neuroplasticity",
        "question": "Wie gut können Sie sich an neue Situationen anpassen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Kolb, B., & Whishaw, I. Q. (1998). Brain plasticity and behavior.",
        "bibtex_key": "kolb1998plasticity"
    },
    # ... 7+ weitere Fragen
]
```

##### 2D: Psychologisch
```python
# surveys/dimension_2_psychology.py
PSYCHOLOGY_QUESTIONS = [
    {
        "id": "psych_intrinsic_motivation",
        "question": "Wie stark fühlen Sie sich intrinsisch (von innen heraus) motiviert bei Ihren Haupttätigkeiten?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Deci, E. L., & Ryan, R. M. (2000). Self-determination theory.",
        "bibtex_key": "deci2000sdt",
        "sub_dimension": "Autonomy"
    },
    {
        "id": "psych_growth_mindset",
        "question": "Inwieweit glauben Sie, dass Sie durch Anstrengung Ihre Fähigkeiten verbessern können?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Dweck, C. S. (2006). Mindset: The new psychology of success.",
        "bibtex_key": "dweck2006mindset",
        "sub_dimension": "Competence"
    },
    # ... 8+ weitere Fragen (Selbstwirksamkeit, soziale Verbundenheit, etc.)
]
```

##### 3D: Philosophisch
```python
# surveys/dimension_3_philosophy.py
PHILOSOPHY_QUESTIONS = [
    {
        "id": "philo_critical_thinking",
        "question": "Wie wichtig ist Ihnen die Hinterfragung etablierter Wahrheiten?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Paul, R., & Elder, L. (2006). Critical thinking.",
        "bibtex_key": "paul2006critical"
    },
    {
        "id": "philo_epistemic_pluralism",
        "question": "Wie offen sind Sie gegenüber unterschiedlichen Wissensformen (wissenschaftlich, kulturell, intuitiv)?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Santos, B. d. S. (2014). Epistemologies of the South.",
        "bibtex_key": "santos2014epistemologies"
    },
    # ... 8+ weitere Fragen
]
```

##### 4D: Ökonomisch
```python
# surveys/dimension_4_economics.py
ECONOMICS_QUESTIONS = [
    {
        "id": "econ_participation",
        "question": "Wie wichtig ist Ihnen Mitbestimmung in wirtschaftlichen Entscheidungen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Albert, M., & Hahnel, R. (1991). The political economy of participatory economics.",
        "bibtex_key": "albert1991parecon"
    },
    {
        "id": "econ_commons",
        "question": "Wie wichtig ist Ihnen gemeinschaftliches Eigentum an Ressourcen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Ostrom, E. (1990). Governing the commons.",
        "bibtex_key": "ostrom1990commons"
    },
    # ... 8+ weitere Fragen
]
```

##### 5D: Technologisch
```python
# surveys/dimension_5_technology.py
TECHNOLOGY_QUESTIONS = [
    {
        "id": "tech_open_source",
        "question": "Wie wichtig ist Ihnen Open-Source-Software?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Raymond, E. S. (1999). The cathedral and the bazaar.",
        "bibtex_key": "raymond1999cathedral"
    },
    {
        "id": "tech_digital_autonomy",
        "question": "Wie wichtig ist Ihnen Kontrolle über Ihre digitalen Daten?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "reference": "Zuboff, S. (2019). The age of surveillance capitalism.",
        "bibtex_key": "zuboff2019surveillance"
    },
    # ... 8+ weitere Fragen
]
```

### Datenverarbeitung & Formeln

#### Integration von GDrive-Formeln
```python
# analysis/calculate_5d_scores.py
import json
from models.imp import calculate_imp_verified

def calculate_dimension_score(responses, dimension):
    \"\"\"
    Berechnet aggregierten Score pro Dimension.
    Verwendet Formeln aus /formeln/ Ordner.
    
    Args:
        responses: Dict mit Antworten
        dimension: str - 'neurobiology', 'psychology', etc.
    
    Returns:
        dict mit raw_score, normalized_score, sub_scores
    \"\"\"
    dimension_questions = load_dimension_questions(dimension)
    
    raw_scores = []
    for question in dimension_questions:
        qid = question['id']
        if qid in responses:
            raw_scores.append(responses[qid])
    
    # Durchschnitt (5-Punkt-Likert)
    avg_score = sum(raw_scores) / len(raw_scores) if raw_scores else 0
    
    # Normalisierung (0-1)
    normalized = (avg_score - 1) / 4  # Likert 1-5 -> 0-1
    
    return {
        'dimension': dimension,
        'raw_score': avg_score,
        'normalized_score': normalized,
        'n_questions': len(raw_scores),
        'completeness': len(raw_scores) / len(dimension_questions)
    }

def calculate_5d_intelligence_profile(all_responses):
    \"\"\"
    Generiert vollständiges 5D-Profil.
    \"\"\"
    dimensions = ['neurobiology', 'psychology', 'philosophy', 'economics', 'technology']
    
    profile = {
        'entrance_data': extract_entrance_data(all_responses),
        'dimension_scores': {},
        'aggregate_score': 0,
        'timestamp': datetime.now().isoformat()
    }
    
    for dim in dimensions:
        profile['dimension_scores'][dim] = calculate_dimension_score(all_responses, dim)
    
    # Aggregierter Score (gleichgewichtet)
    aggregate = sum([s['normalized_score'] for s in profile['dimension_scores'].values()]) / 5
    profile['aggregate_score'] = aggregate
    
    # Optional: IMP-Score Integration
    if 'imp_components' in all_responses:
        profile['imp_score'] = calculate_imp_verified(all_responses['imp_components'])
    
    return profile
```

#### Clustering & Segmentierung
```python
# analysis/cluster_responses.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

def cluster_participants(all_profiles):
    \"\"\"
    Clustert Teilnehmer basierend auf 5D-Profilen.
    
    Verwendet: K-Means (k=5 als Default)
    Features: Dimension-Scores + Entrance-Daten
    \"\"\"
    df = pd.DataFrame(all_profiles)
    
    # Feature-Extraktion
    features = []
    for profile in all_profiles:
        feature_vector = [
            profile['dimension_scores']['neurobiology']['normalized_score'],
            profile['dimension_scores']['psychology']['normalized_score'],
            profile['dimension_scores']['philosophy']['normalized_score'],
            profile['dimension_scores']['economics']['normalized_score'],
            profile['dimension_scores']['technology']['normalized_score'],
            profile['entrance_data']['life_satisfaction'],
            profile['entrance_data']['financial_situation']
        ]
        features.append(feature_vector)
    
    # Standardisierung
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)
    
    return {
        'cluster_labels': clusters.tolist(),
        'cluster_centers': kmeans.cluster_centers_.tolist(),
        'n_clusters': 5
    }
```

### Visualisierung

```python
# analysis/visualize_results.py
import plotly.graph_objects as go
import plotly.express as px

def generate_dimension_radar_chart(profile):
    \"\"\"
    Erzeugt Radar-Chart für 5D-Profil.
    \"\"\"
    dimensions = ['Neurobiologie', 'Psychologie', 'Philosophie', 'Ökonomie', 'Technologie']
    scores = [
        profile['dimension_scores']['neurobiology']['normalized_score'],
        profile['dimension_scores']['psychology']['normalized_score'],
        profile['dimension_scores']['philosophy']['normalized_score'],
        profile['dimension_scores']['economics']['normalized_score'],
        profile['dimension_scores']['technology']['normalized_score']
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=dimensions,
        fill='toself',
        name='5D-Profil'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False,
        title='5D-Intelligence Profil'
    )
    
    return fig

def generate_cluster_heatmap(cluster_data, profiles):
    \"\"\"
    Heatmap der Cluster-Zentren.
    \"\"\"
    # Implementierung...
    pass

def generate_time_series(longitudinal_data):
    \"\"\"
    Zeitverlauf falls mehrfache Teilnahme (opt-in).
    \"\"\"
    # Implementierung...
    pass
```

### Authentifizierung & Datenschutz

```python
# auth/github_oauth.py
import os
import hashlib
import secrets

class GitHubAuth:
    \"\"\"GitHub OAuth nur für Zugangskontrolle, KEINE Daten-Persistierung.\"\"\"
    
    def __init__(self):
        self.client_id = os.getenv('GITHUB_CLIENT_ID')
        self.client_secret = os.getenv('GITHUB_CLIENT_SECRET')
    
    def generate_session_token(self):
        \"\"\"Generiert anonyme Session-ID.\"\"\"
        return secrets.token_urlsafe(32)
    
    def authenticate(self, code):
        \"\"\"OAuth-Flow, gibt nur Session-Token zurück.\"\"\"
        # 1. Exchange code for access_token
        # 2. Validiere dass User existiert
        # 3. Generiere anonyme Session
        # 4. LÖSCHE alle GitHub-Daten sofort
        
        session_token = self.generate_session_token()
        
        # KEINE Speicherung von:
        # - github_username
        # - github_email
        # - github_id
        
        return {
            'session_token': session_token,
            'expires_at': datetime.now() + timedelta(hours=24)
        }

# storage/anonymize.py
def anonymize_response(response_data):
    \"\"\"
    Entfernt ALLE identifizierenden Informationen.
    \"\"\"
    # Generiere eindeutige, aber nicht-rückverfolgbare ID
    anonymous_id = hashlib.sha256(
        (str(uuid.uuid4()) + secrets.token_hex(16)).encode()
    ).hexdigest()
    
    cleaned_response = {
        'id': anonymous_id,
        'responses': response_data['responses'],
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
    
    # Explizit entfernen:
    prohibited_keys = ['username', 'email', 'github_id', 'ip_address', 'user_agent']
    for key in prohibited_keys:
        if key in cleaned_response:
            del cleaned_response[key]
    
    return cleaned_response
```

### Implementierungs-Roadmap

#### Phase 1: Fragebogen-Development (Priorität 1)
- [ ] `surveys/entrance_questions.py` mit vollständigem Schema
- [ ] `surveys/dimension_X_*.py` für alle 5 Dimensionen (mindestens 10 Fragen je)
- [ ] `surveys/validator.py` für Input-Validierung
- [ ] `surveys/bibtex_sources.bib` mit allen wissenschaftlichen Quellen

#### Phase 2: Web-Interface (Priorität 1)
- [ ] `web/survey-app/` mit React/Vite
- [ ] GitHub OAuth Integration
- [ ] Progressives Multi-Step-Formular
- [ ] DSGVO-Consent-Management
- [ ] Offline-Fähigkeit (Progressive Web App)

#### Phase 3: Datenverarbeitung (Priorität 2)
- [ ] `analysis/calculate_5d_scores.py`
- [ ] `analysis/cluster_responses.py`
- [ ] `analysis/visualize_results.py`
- [ ] Integration mit GDrive-Formeln
- [ ] Export-Funktionen (CSV, JSON, BibTeX)

#### Phase 4: Dokumentation (Priorität 2)
- [ ] Wiki: Methodik, Fragebogen-Design, Ethik
- [ ] README: Schnellstart für Teilnehmer
- [ ] CONTRIBUTING: Richtlinien für neue Fragen
- [ ] API-Dokumentation für Forscher

#### Phase 5: Testing & Validierung (Priorität 1)
- [ ] Unit-Tests für alle Berechnungen
- [ ] Validierung der Fragebogen-Zuverlässigkeit (Cronbach's Alpha)
- [ ] Pilotphase mit 50-100 Teilnehmern
- [ ] Iterative Verbesserung basierend auf Feedback

### Code-Generierungs-Richtlinien für Copilot

**Beim Generieren von Survey-Code:**

1. **Immer wissenschaftliche Quelle angeben**:
   ```python
   # Referenz: Csikszentmihalyi (1990) - Flow Theory
   # BibTeX: csikszentmihalyi1990flow
   FLOW_THRESHOLD = 0.7
   ```

2. **Likert-Skalen konsistent verwenden**:
   ```python
   LIKERT_5 = [1, 2, 3, 4, 5]  # Standard
   LIKERT_LABELS_DE = ["Stimme überhaupt nicht zu", "Stimme nicht zu", "Neutral", "Stimme zu", "Stimme voll zu"]
   ```

3. **Validierung einbauen**:
   ```python
   def validate_likert_response(value, scale=[1,2,3,4,5]):
       assert value in scale, f"Invalid Likert value: {value}"
       return True
   ```

4. **Anonymität garantieren**:
   ```python
   PROHIBITED_FIELDS = ['name', 'email', 'username', 'github_id', 'ip']
   
   def ensure_anonymity(data):
       for field in PROHIBITED_FIELDS:
           assert field not in data, f"Prohibited field found: {field}"
   ```

5. **Tests schreiben**:
   ```python
   def test_anonymization():
       response = {'question_1': 3, 'user_id': 'SHOULD_NOT_EXIST'}
       anonymized = anonymize_response(response)
       assert 'user_id' not in anonymized
       assert 'id' in anonymized
       assert len(anonymized['id']) == 64  # SHA256 hex
   ```

### Datei-Locations

```
5d/
├── surveys/
│   ├── entrance_questions.py
│   ├── dimension_1_neurobiology.py
│   ├── dimension_2_psychology.py
│   ├── dimension_3_philosophy.py
│   ├── dimension_4_economics.py
│   ├── dimension_5_technology.py
│   ├── validator.py
│   └── bibtex_sources.bib
├── analysis/
│   ├── calculate_5d_scores.py
│   ├── cluster_responses.py
│   └── visualize_results.py
├── auth/
│   ├── github_oauth.py
│   └── session_manager.py
├── storage/
│   ├── anonymize.py
│   └── database.py  # SQLite
├── web/
│   └── survey-app/  # React + Vite
├── tests/
│   ├── test_surveys.py
│   ├── test_anonymization.py
│   └── test_calculations.py
└── wiki/
    ├── Survey-Methodology.md
    ├── Question-Design.md
    ├── Data-Processing.md
    └── Ethics-GDPR.md
```

### Ethik & DSGVO

**Consent-Text (Beispiel)**:
```markdown
## Einwilligungserklärung

Mit Ihrer Teilnahme erklären Sie sich einverstanden:

1. ✅ Ihre Antworten werden **vollständig anonymisiert** gespeichert
2. ✅ **Keine personenbezogenen Daten** (Name, E-Mail, GitHub-Username) werden gespeichert
3. ✅ Daten werden nur für **wissenschaftliche Forschung** im 5D-Framework verwendet
4. ✅ Alle Daten sind **Open Science** - aggregierte Ergebnisse werden veröffentlicht
5. ✅ Sie können jederzeit **Löschung** beantragen (via GitHub Issue mit Session-Token)

**Datenschutz**: DSGVO-konform, lokale Speicherung, keine Cloud-Services.

[ ] Ich habe die Datenschutzerklärung gelesen und stimme zu
```

---

**Version**: 2.0.0 (erweitert mit akademischem Survey-Framework)  
**Letzte Aktualisierung**: 2025-12-02  
**Status**: Spezifikation vollständig, Implementierung Priorität 1
