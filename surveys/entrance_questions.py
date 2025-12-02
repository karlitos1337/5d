#!/usr/bin/env python3
"""Eingangsfragen für 5D-Intelligence Survey.

Anonym erhobene demografische Daten zur Kontextualisierung.
KEINE personenbezogenen Daten (Name, E-Mail, etc.).
"""

ENTRANCE_SCHEMA = {
    "employment_status": {
        "type": "select",
        "question": "Was beschreibt Ihre aktuelle berufliche Situation am besten?",
        "options": [
            "Angestellt (Vollzeit)",
            "Angestellt (Teilzeit)",
            "Selbstständig",
            "Student/in",
            "Arbeitssuchend",
            "Rentner/in",
            "Sonstiges"
        ],
        "required": True,
        "purpose": "Kontext für wirtschaftliche Perspektive"
    },
    "education_level": {
        "type": "select",
        "question": "Was ist Ihr höchster Bildungsabschluss?",
        "options": [
            "Kein Abschluss",
            "Hauptschulabschluss",
            "Realschulabschluss / Mittlere Reife",
            "Fachhochschulreife / Fachabitur",
            "Allgemeine Hochschulreife / Abitur",
            "Bachelor",
            "Master / Diplom",
            "Promotion",
            "Sonstiges"
        ],
        "required": True,
        "purpose": "Bildungshintergrund für Analyse"
    },
    "postal_code": {
        "type": "number",
        "question": "Postleitzahl Ihres Wohnorts (optional, für regionale Clusterung):",
        "min": 1000,
        "max": 99999,
        "required": False,
        "purpose": "Anonymisierte regionale Zuordnung",
        "privacy_note": "Wird nur für statistische Clusterung verwendet, nicht gespeichert mit anderen Daten"
    },
    "federal_state": {
        "type": "text",
        "question": "Bundesland (optional):",
        "max_length": 50,
        "required": False,
        "purpose": "Regionale Unterschiede analysieren"
    },
    "country": {
        "type": "select",
        "question": "Land:",
        "source": "ISO_3166_countries",
        "default": "DE",
        "required": True,
        "purpose": "Kultureller Kontext"
    },
    "life_satisfaction": {
        "type": "likert",
        "question": "Wie bewerten Sie Ihr aktuelles Leben insgesamt?",
        "scale": [1, 2, 3, 4, 5, 6],
        "labels": ["Sehr gut (1)", "Gut (2)", "Befriedigend (3)", "Ausreichend (4)", "Mangelhaft (5)", "Ungenügend (6)"],
        "reverse_coded": True,
        "required": True,
        "purpose": "Allgemeines Wohlbefinden",
        "reference": "Schulnotensystem DE"
    },
    "future_expectation": {
        "type": "likert",
        "question": "Wie zuversichtlich blicken Sie in Ihre persönliche Zukunft?",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr pessimistisch", "Eher pessimistisch", "Neutral", "Eher optimistisch", "Sehr optimistisch"],
        "required": True,
        "purpose": "Zukunftsorientierung"
    },
    "past_evaluation": {
        "type": "likert",
        "question": "Wie bewerten Sie Ihre bisherige Lebensgeschichte?",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr unzufrieden", "Eher unzufrieden", "Neutral", "Eher zufrieden", "Sehr zufrieden"],
        "required": True,
        "purpose": "Vergangenheitsbewertung"
    },
    "financial_situation": {
        "type": "select",
        "question": "Wie würden Sie Ihre finanzielle Situation einschätzen?",
        "options": [
            "Sehr gut - keine finanziellen Sorgen",
            "Gut - komme gut zurecht",
            "Befriedigend - komme einigermaßen zurecht",
            "Ausreichend - muss sehr auf Ausgaben achten",
            "Schwierig - habe finanzielle Probleme"
        ],
        "coding": {
            "Sehr gut - keine finanziellen Sorgen": 5,
            "Gut - komme gut zurecht": 4,
            "Befriedigend - komme einigermaßen zurecht": 3,
            "Ausreichend - muss sehr auf Ausgaben achten": 2,
            "Schwierig - habe finanzielle Probleme": 1
        },
        "required": True,
        "purpose": "Ökonomischer Kontext"
    }
}

# ISO 3166 Länderliste (Auswahl)
COUNTRIES = [
    {"code": "DE", "name": "Deutschland"},
    {"code": "AT", "name": "Österreich"},
    {"code": "CH", "name": "Schweiz"},
    {"code": "LI", "name": "Liechtenstein"},
    {"code": "LU", "name": "Luxemburg"},
    {"code": "BE", "name": "Belgien"},
    {"code": "FR", "name": "Frankreich"},
    {"code": "IT", "name": "Italien"},
    {"code": "NL", "name": "Niederlande"},
    {"code": "PL", "name": "Polen"},
    {"code": "CZ", "name": "Tschechien"},
    {"code": "GB", "name": "Vereinigtes Königreich"},
    {"code": "US", "name": "Vereinigte Staaten"},
    {"code": "OTHER", "name": "Anderes Land"}
]
