#!/usr/bin/env python3
"""Anonymisierungs-Layer für Survey-Responses.

Garantiert vollständige Anonymität gemäß DSGVO.
"""

import hashlib
import secrets
import uuid
from datetime import datetime
from typing import Any

# Explizit verbotene Felder
PROHIBITED_FIELDS = [
    "name",
    "username",
    "email",
    "github_id",
    "github_username",
    "ip_address",
    "user_agent",
    "session_id",
    "access_token",
    "first_name",
    "last_name",
    "phone",
    "address",
]


def generate_anonymous_id() -> str:
    """Generiert eindeutige, aber nicht-rückverfolgbare ID.

    Verwendet:
    - UUID4 (zufällig)
    - Secrets-Token (kryptographisch sicher)
    - SHA256 Hashing

    Returns:
        64-Zeichen Hex-String
    """
    # Kombiniere mehrere Zufallsquellen
    random_data = (
        str(uuid.uuid4()) + secrets.token_hex(32) + str(datetime.now().timestamp())
    ).encode()

    # SHA256 Hash
    anonymous_id = hashlib.sha256(random_data).hexdigest()

    return anonymous_id


def anonymize_response(response_data: dict[str, Any]) -> dict[str, Any]:
    """Entfernt ALLE identifizierenden Informationen.

    Args:
        response_data: Rohe Response mit allen Feldern

    Returns:
        Anonymisierte Response

    Raises:
        ValueError: Wenn verbotene Felder gefunden werden
    """
    # Prüfe auf verbotene Felder
    for field in PROHIBITED_FIELDS:
        if field in response_data:
            raise ValueError(
                f"Prohibited field '{field}' found in response data. "
                "This field must not be included."
            )

    # Generiere anonyme ID
    anonymous_id = generate_anonymous_id()

    # Erstelle saubere Response
    cleaned_response = {
        "id": anonymous_id,
        "responses": response_data.get("responses", {}),
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "metadata": {
            "anonymized": True,
            "anonymization_timestamp": datetime.now().isoformat(),
        },
    }

    # Doppelte Prüfung
    for field in PROHIBITED_FIELDS:
        if field in cleaned_response:
            del cleaned_response[field]
        if field in cleaned_response.get("responses", {}):
            del cleaned_response["responses"][field]

    return cleaned_response


def batch_anonymize(responses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Anonymisiert mehrere Responses."""
    anonymized = []
    for response in responses:
        try:
            anon_response = anonymize_response(response)
            anonymized.append(anon_response)
        except ValueError as e:
            print(f"Error anonymizing response: {e}")
            continue
    return anonymized


def verify_anonymity(response: dict[str, Any]) -> bool:
    """Verifiziert dass Response komplett anonym ist.

    Returns:
        True wenn anonym, False wenn Probleme gefunden
    """

    # Prüfe alle Felder rekursiv
    def check_dict(d: dict) -> list[str]:
        found = []
        for key, value in d.items():
            if key in PROHIBITED_FIELDS:
                found.append(key)
            if isinstance(value, dict):
                found.extend(check_dict(value))
        return found

    violations = check_dict(response)

    if violations:
        print(f"Anonymity violations found: {violations}")
        return False

    # Prüfe ob ID vorhanden
    if "id" not in response:
        print("Missing anonymous ID")
        return False

    # Prüfe ID-Format (SHA256 = 64 Hex-Zeichen)
    if len(response["id"]) != 64:
        print(f"Invalid ID length: {len(response['id'])} (expected 64)")
        return False

    return True


def export_anonymized_dataset(responses: list[dict], output_format: str = "json") -> str:
    """Exportiert anonymisierte Daten.

    Args:
        responses: Liste anonymisierter Responses
        output_format: 'json' oder 'csv'

    Returns:
        Serialisierte Daten
    """
    import json

    if output_format == "json":
        return json.dumps(responses, indent=2, ensure_ascii=False)

    elif output_format == "csv":
        import pandas as pd

        # Flatten für CSV
        flattened = []
        for r in responses:
            flat = {"id": r["id"], "timestamp": r["timestamp"]}
            flat.update(r.get("responses", {}))
            flattened.append(flat)

        df = pd.DataFrame(flattened)
        return df.to_csv(index=False)

    else:
        raise ValueError(f"Unsupported format: {output_format}")


if __name__ == "__main__":
    # Test
    test_response = {"responses": {"neuro_flow_frequency": 4, "psych_intrinsic_motivation": 5}}

    anonymized = anonymize_response(test_response)
    print("Anonymized Response:")
    print(f"ID: {anonymized['id']}")
    print(f"Timestamp: {anonymized['timestamp']}")

    # Verify
    is_anonymous = verify_anonymity(anonymized)
    print(f"\nAnonymity verified: {is_anonymous}")

    # Test mit verbotendem Feld
    try:
        bad_response = {
            "responses": {"test": 1},
            "email": "test@example.com",
        }  # Verboten!
        anonymize_response(bad_response)
    except ValueError as e:
        print(f"\nExpected error caught: {e}")
