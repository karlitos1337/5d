"""Tests für scripts/pilot_export.py (Export freigegebener Supabase-Spenden)."""

import csv
import importlib.util
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "pilot_export", Path(__file__).resolve().parents[1] / "scripts" / "pilot_export.py"
)
pilot_export = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(pilot_export)


def record(**overrides) -> dict:
    data = {
        "participant_code": "K7Q2-9XPA",
        "submitted_month": "2026-10-01",
        "age_group": "25-34",
        "attention_ok": True,
        "imp": [3] * 25,
        "swls": [5] * 5,
    }
    data.update(overrides)
    return data


def test_export_writes_only_what_the_api_returns(tmp_path):
    calls = []

    def fake_fetch(url, key):
        calls.append((url, key))
        return [record(), record(participant_code="ABCD-EFGH", attention_ok=False)]

    csv_path = tmp_path / "out" / "pilot.csv"
    count = pilot_export.export("https://x.supabase.co/", "secret", csv_path, fetch=fake_fetch)

    assert count == 2
    url, key = calls[0]
    assert url.startswith("https://x.supabase.co/rest/v1/pilot_submissions?")
    assert "approved=eq.true" in url
    assert key == "secret"
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [r["id"] for r in rows] == ["K7Q2-9XPA", "ABCD-EFGH"]
    assert rows[0]["monat"] == "2026-10"
    assert rows[1]["aufmerksamkeit_ok"] == "0"


def test_export_rewrites_file_so_withdrawals_disappear(tmp_path):
    csv_path = tmp_path / "pilot.csv"
    pilot_export.export("https://x.supabase.co", "k", csv_path, fetch=lambda u, k: [record()])
    pilot_export.export("https://x.supabase.co", "k", csv_path, fetch=lambda u, k: [])
    with csv_path.open(newline="", encoding="utf-8") as f:
        assert list(csv.DictReader(f)) == []


@pytest.mark.parametrize(
    "overrides",
    [
        {"participant_code": "x"},
        {"submitted_month": "gestern"},
        {"age_group": "30"},
        {"attention_ok": 1},
        {"imp": [3] * 24},
        {"swls": [9] * 5},
    ],
)
def test_invalid_rows_abort_export(tmp_path, overrides):
    with pytest.raises(pilot_export.pilot_import.SubmissionError):
        pilot_export.export(
            "https://x.supabase.co",
            "k",
            tmp_path / "p.csv",
            fetch=lambda u, k: [record(**overrides)],
        )


def test_main_requires_credentials(monkeypatch, capsys):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
    assert pilot_export.main([]) == 2
    assert "SUPABASE_URL" in capsys.readouterr().err
