#!/usr/bin/env python3
"""Tests für Survey-Validierung."""

import pytest

from surveys.validator import (
    validate_completeness,
    validate_likert_response,
    validate_number_response,
    validate_select_response,
)


def test_validate_likert_5_point():
    """Test 5-Punkt Likert-Skala."""
    scale = [1, 2, 3, 4, 5]

    assert validate_likert_response(1, scale) is True
    assert validate_likert_response(3, scale) is True
    assert validate_likert_response(5, scale) is True

    assert validate_likert_response(0, scale) is False
    assert validate_likert_response(6, scale) is False
    assert validate_likert_response("3", scale) is False


def test_validate_select():
    """Test Multiple Choice."""
    options = ["Option A", "Option B", "Option C"]

    assert validate_select_response("Option A", options) is True
    assert validate_select_response("Option D", options) is False


def test_validate_number():
    """Test numerische Antworten."""
    assert validate_number_response(50000, 10000, 99999) is True
    assert validate_number_response(100000, 10000, 99999) is False
    assert validate_number_response("50000", 10000, 99999) is False


def test_validate_completeness():
    """Test Vollständigkeits-Prüfung."""
    responses = {"q1": 1, "q2": 2, "q3": 3}

    required = ["q1", "q2", "q3", "q4"]

    result = validate_completeness(responses, required)

    assert result["complete"] is False
    assert "q4" in result["missing"]
    assert result["completeness_rate"] == 0.75


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
