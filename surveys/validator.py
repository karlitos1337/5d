#!/usr/bin/env python3
"""Validierung von Survey-Responses."""

from typing import Dict, Any, List


def validate_likert_response(value: Any, scale: List[int]) -> bool:
    """Validiert Likert-Skalen-Antwort."""
    if not isinstance(value, int):
        return False
    return value in scale


def validate_select_response(value: Any, options: List[str]) -> bool:
    """Validiert Multiple-Choice-Antwort."""
    return value in options


def validate_number_response(value: Any, min_val: int, max_val: int) -> bool:
    """Validiert numerische Antwort."""
    if not isinstance(value, (int, float)):
        return False
    return min_val <= value <= max_val


def validate_text_response(value: Any, max_length: int) -> bool:
    """Validiert Text-Antwort."""
    if not isinstance(value, str):
        return False
    return len(value) <= max_length


def validate_response(question_id: str, value: Any, schema: Dict) -> bool:
    """Haupt-Validierungsfunktion.
    
    Args:
        question_id: ID der Frage
        value: Antwort-Wert
        schema: Fragen-Schema mit Validierungsregeln
    
    Returns:
        True wenn valide
    """
    if question_id not in schema:
        return False
    
    question = schema[question_id]
    q_type = question['type']
    
    if q_type == 'likert':
        return validate_likert_response(value, question['scale'])
    elif q_type == 'select':
        return validate_select_response(value, question['options'])
    elif q_type == 'number':
        return validate_number_response(value, question['min'], question['max'])
    elif q_type == 'text':
        return validate_text_response(value, question['max_length'])
    
    return False


def validate_completeness(responses: Dict, required_questions: List[str]) -> Dict:
    """Prüft Vollständigkeit.
    
    Returns:
        {'complete': bool, 'missing': List[str]}
    """
    missing = [q for q in required_questions if q not in responses]
    
    return {
        'complete': len(missing) == 0,
        'missing': missing,
        'completeness_rate': (len(required_questions) - len(missing)) / len(required_questions)
    }
