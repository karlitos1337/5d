#!/usr/bin/env python3
"""5D-Intelligence Score Calculation.

Berechnet Scores für alle fünf Dimensionen und aggregiert
zu einem Gesamt-5D-Intelligence-Profil.

Formeln basierend auf:
- /formeln/IMP_formula.md
- models/imp.py
- Wissenschaftliche Quellen in surveys/bibtex_sources.bib
"""

import json
from datetime import datetime
from typing import Any


def load_dimension_questions(dimension: str) -> list[dict]:
    """Lädt Fragen für spezifische Dimension.

    Args:
        dimension: 'neurobiology', 'psychology', 'philosophy', 'economics', 'technology'

    Returns:
        Liste von Fragen-Dictionaries
    """
    # Dynamischer Import
    if dimension == "neurobiology":
        from surveys.dimension_1_neurobiology import NEUROBIOLOGY_QUESTIONS

        return NEUROBIOLOGY_QUESTIONS
    elif dimension == "psychology":
        from surveys.dimension_2_psychology import PSYCHOLOGY_QUESTIONS

        return PSYCHOLOGY_QUESTIONS
    elif dimension == "philosophy":
        from surveys.dimension_3_philosophy import PHILOSOPHY_QUESTIONS

        return PHILOSOPHY_QUESTIONS
    elif dimension == "economics":
        from surveys.dimension_4_economics import ECONOMICS_QUESTIONS

        return ECONOMICS_QUESTIONS
    elif dimension == "technology":
        from surveys.dimension_5_technology import TECHNOLOGY_QUESTIONS

        return TECHNOLOGY_QUESTIONS
    else:
        raise ValueError(f"Unknown dimension: {dimension}")


def calculate_dimension_score(responses: dict[str, Any], dimension: str) -> dict:
    """Berechnet Score für eine Dimension.

    Args:
        responses: Dictionary mit Antworten {question_id: likert_value}
        dimension: Name der Dimension

    Returns:
        Dictionary mit raw_score, normalized_score, sub_scores
    """
    questions = load_dimension_questions(dimension)

    raw_scores = []
    sub_dimension_scores = {}

    for question in questions:
        qid = question["id"]
        if qid in responses:
            value = responses[qid]

            # Reverse-Codierung wenn nötig
            if question.get("reverse_coded", False):
                # Likert 1-5 -> 5-1 oder 1-6 -> 6-1
                scale_max = max(question["scale"])
                scale_min = min(question["scale"])
                value = (scale_max + scale_min) - value

            raw_scores.append(value)

            # Sub-Dimension tracking
            sub_dim = question.get("sub_dimension", "General")
            if sub_dim not in sub_dimension_scores:
                sub_dimension_scores[sub_dim] = []
            sub_dimension_scores[sub_dim].append(value)

    if not raw_scores:
        return {
            "dimension": dimension,
            "raw_score": 0,
            "normalized_score": 0,
            "n_questions": 0,
            "completeness": 0,
            "sub_dimensions": {},
        }

    # Durchschnitt (Likert 1-5)
    avg_score = sum(raw_scores) / len(raw_scores)

    # Normalisierung (0-1)
    # Annahme: Likert-Skala 1-5 (kann angepasst werden)
    normalized = (avg_score - 1) / 4  # 1->0, 3->0.5, 5->1

    # Sub-Dimensionen berechnen
    sub_dim_normalized = {}
    for sub_dim, scores in sub_dimension_scores.items():
        avg = sum(scores) / len(scores)
        sub_dim_normalized[sub_dim] = (avg - 1) / 4

    return {
        "dimension": dimension,
        "raw_score": round(avg_score, 3),
        "normalized_score": round(normalized, 3),
        "n_questions_answered": len(raw_scores),
        "n_questions_total": len(questions),
        "completeness": round(len(raw_scores) / len(questions), 3),
        "sub_dimensions": sub_dim_normalized,
    }


def extract_entrance_data(responses: dict[str, Any]) -> dict:
    """Extrahiert anonymisierte Eingangsdaten."""
    from surveys.entrance_questions import ENTRANCE_SCHEMA

    entrance = {}
    for key in ENTRANCE_SCHEMA.keys():
        if key in responses:
            value = responses[key]

            # Codierung für finanzielle Lage
            if key == "financial_situation" and isinstance(value, str):
                coding = ENTRANCE_SCHEMA[key].get("coding", {})
                value = coding.get(value, value)

            # Reverse-Codierung für life_satisfaction (Schulnoten)
            if key == "life_satisfaction" and ENTRANCE_SCHEMA[key].get("reverse_coded", False):
                value = 7 - value  # 1->6, 6->1

            entrance[key] = value

    return entrance


def calculate_5d_intelligence_profile(all_responses: dict[str, Any]) -> dict:
    """Generiert vollständiges 5D-Intelligence-Profil.

    Args:
        all_responses: Alle Antworten (Eingang + 5 Dimensionen)

    Returns:
        Vollständiges Profil-Dictionary
    """
    dimensions = ["neurobiology", "psychology", "philosophy", "economics", "technology"]

    profile = {
        "entrance_data": extract_entrance_data(all_responses),
        "dimension_scores": {},
        "aggregate_score": 0,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }

    # Dimensionen berechnen
    for dim in dimensions:
        profile["dimension_scores"][dim] = calculate_dimension_score(all_responses, dim)

    # Aggregierter Score (gleichgewichtet)
    normalized_scores = [s["normalized_score"] for s in profile["dimension_scores"].values()]
    aggregate = sum(normalized_scores) / len(normalized_scores)
    profile["aggregate_score"] = round(aggregate, 3)

    # Optional: IMP-Score Integration
    if "imp_components" in all_responses:
        try:
            from models.imp import calculate_imp_verified

            profile["imp_score"] = calculate_imp_verified(all_responses["imp_components"])
        except ImportError:
            pass  # IMP-Modell nicht verfügbar

    return profile


def batch_calculate_profiles(all_participant_responses: list[dict]) -> list[dict]:
    """Batch-Verarbeitung für mehrere Teilnehmer."""
    profiles = []
    for responses in all_participant_responses:
        try:
            profile = calculate_5d_intelligence_profile(responses)
            profiles.append(profile)
        except Exception as e:
            print(f"Error processing response: {e}")
            continue
    return profiles


if __name__ == "__main__":
    # Test-Beispiel
    test_responses = {
        # Entrance
        "employment_status": "Angestellt",
        "life_satisfaction": 2,  # Gut (Schulnote)
        "financial_situation": 4,
        # Neuro
        "neuro_flow_frequency": 4,
        "neuro_attention_span": 3,
        "neuro_neuroplasticity": 4,
        # Psych
        "psych_intrinsic_motivation": 5,
        "psych_growth_mindset": 5,
        "psych_self_efficacy": 4,
        # Philo
        "philo_critical_thinking": 5,
        "philo_epistemic_pluralism": 4,
        # Econ
        "econ_participation": 5,
        "econ_commons": 4,
        # Tech
        "tech_open_source": 5,
        "tech_digital_autonomy": 5,
    }

    profile = calculate_5d_intelligence_profile(test_responses)
    print(json.dumps(profile, indent=2))
