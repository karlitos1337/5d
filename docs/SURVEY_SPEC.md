# Full Survey Specification

This file contains the full survey specification and example code extracted from the agent instructions. The canonical, importable code remains in `surveys/` (use those files for production runs and tests). This document is a human-readable reference for editors and reviewers.

---

## 1) Entrance Schema (complete example)

```python
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
        "scale": [1, 2, 3, 4, 5, 6],
        "label": "Wie bewerten Sie Ihr aktuelles Leben insgesamt?",
        "reverse_coded": True
    },
    "future_expectation": {
        "type": "likert",
        "scale": [1, 2, 3, 4, 5]
    },
    "past_evaluation": {
        "type": "likert",
        "scale": [1, 2, 3, 4, 5]
    },
    "financial_situation": {
        "type": "select",
        "options": ["Sehr gut", "Gut", "Befriedigend", "Ausreichend", "Schwierig"],
        "coding": {"Sehr gut": 5, "Gut": 4, "Befriedigend": 3, "Ausreichend": 2, "Schwierig": 1}
    }
}
```

---

## 2) Dimension Questions (excerpts)

### 2.1 Neurobiology (examples)

```python
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
    }
]
```

### 2.2 Psychology (examples)

```python
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
    }
]
```

### 2.3 Philosophy / Economics / Technology (examples)

```python
PHILOSOPHY_QUESTIONS = [
    {"id": "philo_critical_thinking", "question": "Wie wichtig ist Ihnen die Hinterfragung etablierter Wahrheiten?", "type": "likert"}
]

ECONOMICS_QUESTIONS = [
    {"id": "econ_participation", "question": "Wie wichtig ist Ihnen Mitbestimmung in wirtschaftlichen Entscheidungen?", "type": "likert"}
]

TECHNOLOGY_QUESTIONS = [
    {"id": "tech_open_source", "question": "Wie wichtig ist Ihnen Open-Source-Software?", "type": "likert"}
]
```

---

## 3) Data processing (where to implement formulas)

- `analysis/calculate_5d_scores.py`: per-dimension aggregation, normalization (0..1), completeness counts.
- `analysis/cluster_responses.py`: clustering examples using scikit-learn.
- `analysis/visualize_results.py`: plotly / radar charts.

## 4) IMP integration

- Use `models/imp.py` and call `calculate_imp_verified(...)` to compute IMP-related metrics.

## 5) Privacy & anonymization

- Use `storage/anonymize.py` to generate non-reversible IDs and remove PII. Follow consent text in `docs/` or `surveys/`.

---

Notes:
- The canonical, importable question sets remain in `surveys/`. Keep `docs/SURVEY_SPEC.md` as the human-readable source of truth for reviewers and editors.
# Survey specification (summary)

This file summarizes the survey/questionnaire material present in the repo and points to the canonical locations.

Purpose
- Hold the long-form survey/spec content separately from the agent instructions.

Where the canonical code lives
- Entrance and dimension questions: `surveys/entrance_questions.py` and `surveys/dimension_*_*.py`
- Validator helpers: `surveys/validator.py`
- BibTeX sources: `surveys/bibtex_sources.bib`

Notes for contributors
- Keep all question text and scales inside `surveys/` files (not in docs) so code and tests can import them.
- When changing question IDs or scales update `analysis/calculate_5d_scores.py` and tests under `tests/`.

Example structure (already in `surveys/`):

- `entrance_questions.py`: demographic/entrance schema (Likert scales, coded options)
- `dimension_1_neurobiology.py` … `dimension_5_technology.py`: at least 10 items per dimension

Privacy / Ethics
- Follow `storage/anonymize.py` when storing or processing responses. No PII must be persisted.

If you want the full original, long survey spec (previously embedded in `.github/copilot-instructions.md`), tell me and I will extract it verbatim into this file.
