# 5D-Intelligence Survey Framework

## Übersicht

Dieses Verzeichnis enthält das vollständige **akademisch validierte Erhebungsinstrument** für das 5D-Intelligence Framework.

## Struktur

```
surveys/
├── entrance_questions.py    # Demografische Eingangsfragen
├── dimension_1_neurobiology.py
├── dimension_2_psychology.py
├── dimension_3_philosophy.py
├── dimension_4_economics.py
├── dimension_5_technology.py
├── validator.py             # Input-Validierung
├── bibtex_sources.bib       # Alle wissenschaftlichen Quellen
└── README.md                # Diese Datei
```

## Prinzipien

1. **Absolute Anonymität**: Keine personenbezogenen Daten
2. **Wissenschaftliche Validität**: Jede Frage mit Quelle belegt
3. **Likert-Skalen**: Standardisiert (1-5)
4. **DSGVO-Konform**: Explizites Consent, Löschrecht

## Verwendung

```python
from surveys import entrance_questions, dimension_1_neurobiology

# Schema laden
entrance_schema = entrance_questions.ENTRANCE_SCHEMA
neuro_questions = dimension_1_neurobiology.NEUROBIOLOGY_QUESTIONS

# Validieren
from surveys.validator import validate_response
valid = validate_response('neuro_flow_frequency', 4)
```

## Entwicklung

Beim Hinzufügen neuer Fragen:
1. Wissenschaftliche Quelle angeben (BibTeX)
2. Likert-Skala 1-5 verwenden
3. Tests schreiben
4. Wiki aktualisieren
