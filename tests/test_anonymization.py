#!/usr/bin/env python3
"""Tests für Anonymisierung."""

import os
import sys
import pytest

# Add parent dir to path to find 'storage' package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage.anonymize import (
    PROHIBITED_FIELDS,
    anonymize_response,
    generate_anonymous_id,
    verify_anonymity,
)


def test_generate_anonymous_id():
    """Test ID-Generierung."""
    id1 = generate_anonymous_id()
    id2 = generate_anonymous_id()

    # IDs müssen unterschiedlich sein
    assert id1 != id2

    # SHA256 = 64 Hex-Zeichen
    assert len(id1) == 64
    assert len(id2) == 64


def test_anonymize_response_basic():
    """Test Basis-Anonymisierung."""
    response = {"responses": {"neuro_flow_frequency": 4, "psych_intrinsic_motivation": 5}}

    anonymized = anonymize_response(response)

    # Prüfe Pflichtfelder
    assert "id" in anonymized
    assert "timestamp" in anonymized
    assert "version" in anonymized
    assert "responses" in anonymized

    # Prüfe Daten intakt
    assert anonymized["responses"]["neuro_flow_frequency"] == 4


def test_anonymize_response_prohibits_personal_data():
    """Test dass personenbezogene Daten blockiert werden."""
    for field in PROHIBITED_FIELDS:
        response = {"responses": {"test": 1}, field: "should_not_exist"}

        with pytest.raises(ValueError):
            anonymize_response(response)


def test_verify_anonymity_valid():
    """Test Anonymitäts-Verifikation mit valider Response."""
    response = {"responses": {"test": 1}}

    anonymized = anonymize_response(response)
    assert verify_anonymity(anonymized) is True


def test_verify_anonymity_invalid():
    """Test Anonymitäts-Verifikation mit invalider Response."""
    bad_response = {
        "id": generate_anonymous_id(),
        "responses": {"test": 1},
        "email": "test@example.com",  # Verboten!
    }

    assert verify_anonymity(bad_response) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
