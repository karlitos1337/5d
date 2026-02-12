import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from storage.anonymize import (
    anonymize_response,
    generate_anonymous_id,
    verify_anonymity,
)

class TestAnonymization:
    def test_anonymize_response_removes_prohibited_fields(self):
        """Test that prohibited fields are removed from the response."""
        response_data = {
            "responses": {"q1": "answer"},
            "email": "test@example.com",  # Should raise error
        }
        with pytest.raises(ValueError, match="Prohibited field 'email' found"):
            anonymize_response(response_data)

    def test_generate_anonymous_id_format(self):
        """Test that the generated ID has the correct format (SHA256)."""
        anon_id = generate_anonymous_id()
        assert len(anon_id) == 64
        assert isinstance(anon_id, str)

    def test_verify_anonymity_success(self):
        """Test that a valid anonymous response passes verification."""
        response = {
            "id": generate_anonymous_id(),
            "responses": {"q1": "answer"},
            "timestamp": "2023-01-01T00:00:00",
        }
        assert verify_anonymity(response) is True

    def test_verify_anonymity_failure_prohibited_field(self):
        """Test that verification fails if a prohibited field is present."""
        response = {
            "id": generate_anonymous_id(),
            "responses": {"q1": "answer", "email": "test@example.com"},
            "timestamp": "2023-01-01T00:00:00",
        }
        assert verify_anonymity(response) is False

    def test_verify_anonymity_failure_missing_id(self):
        """Test that verification fails if 'id' is missing."""
        response = {
            "responses": {"q1": "answer"},
            "timestamp": "2023-01-01T00:00:00",
        }
        assert verify_anonymity(response) is False

    def test_anonymize_response_structure(self):
        """Test the structure of the anonymized response."""
        response_data = {"responses": {"q1": "answer"}}
        anon_response = anonymize_response(response_data)

        assert "id" in anon_response
        assert "timestamp" in anon_response
        assert "version" in anon_response
        assert "metadata" in anon_response
        assert anon_response["responses"] == {"q1": "answer"}
        assert anon_response["metadata"]["anonymized"] is True
