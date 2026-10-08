"""Tests für scripts/pilot_import.py (Freigabe von Pilot-Datenspenden)."""

import base64
import csv
import importlib.util
import json
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "pilot_import", Path(__file__).resolve().parents[1] / "scripts" / "pilot_import.py"
)
pilot_import = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(pilot_import)


def make_code(**overrides) -> str:
    payload = {
        "v": 1,
        "id": "K7Q2-9XPA",
        "m": "2026-10",
        "age": "25-34",
        "att": True,
        "imp": [3] * 25,
        "swls": [5] * 5,
    }
    payload.update(overrides)
    raw = base64.urlsafe_b64encode(json.dumps(payload).encode("ascii")).decode("ascii")
    return "5DP1." + raw.rstrip("=")


def test_valid_code_is_decoded():
    row = pilot_import.decode_submission(make_code())
    assert row["id"] == "K7Q2-9XPA"
    assert row["A1"] == 3 and row["Au5"] == 3
    assert row["SWLS5"] == 5
    assert row["aufmerksamkeit_ok"] == 1


@pytest.mark.parametrize(
    "overrides",
    [
        {"v": 2},
        {"id": "not-valid"},
        {"m": "2026-13"},
        {"age": "30"},
        {"att": "yes"},
        {"imp": [3] * 24},
        {"imp": [0] + [3] * 24},
        {"imp": [True] + [3] * 24},
        {"swls": [8] * 5},
    ],
)
def test_invalid_values_are_rejected(overrides):
    with pytest.raises(pilot_import.SubmissionError):
        pilot_import.decode_submission(make_code(**overrides))


def test_extra_fields_are_rejected():
    with pytest.raises(pilot_import.SubmissionError):
        pilot_import.decode_submission(make_code(email="someone@example.org"))


def test_garbage_is_rejected():
    for code in ["", "hello", "5DP1.!!!", "5DP1." + base64.urlsafe_b64encode(b"[1,2]").decode()]:
        with pytest.raises(pilot_import.SubmissionError):
            pilot_import.decode_submission(code)


def test_append_creates_file_and_rejects_duplicates(tmp_path):
    csv_path = tmp_path / "data" / "pilot.csv"
    pilot_import.append_submission(make_code(), csv_path)
    pilot_import.append_submission(make_code(id="ABCD-EFGH"), csv_path)

    with pytest.raises(pilot_import.SubmissionError):
        pilot_import.append_submission(make_code(), csv_path)

    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [r["id"] for r in rows] == ["K7Q2-9XPA", "ABCD-EFGH"]
    assert list(rows[0].keys()) == pilot_import.COLUMNS


def test_remove_submission(tmp_path):
    csv_path = tmp_path / "pilot.csv"
    pilot_import.append_submission(make_code(), csv_path)
    pilot_import.append_submission(make_code(id="ABCD-EFGH"), csv_path)

    assert pilot_import.remove_submission("K7Q2-9XPA", csv_path)
    assert not pilot_import.remove_submission("K7Q2-9XPA", csv_path)

    with csv_path.open(newline="", encoding="utf-8") as f:
        assert [r["id"] for r in csv.DictReader(f)] == ["ABCD-EFGH"]


def test_cli_exit_codes(tmp_path, capsys):
    csv_path = tmp_path / "pilot.csv"
    assert pilot_import.main([make_code(), "--csv", str(csv_path)]) == 0
    assert pilot_import.main([make_code(), "--csv", str(csv_path)]) == 1
    assert "bereits eingetragen" in capsys.readouterr().err
