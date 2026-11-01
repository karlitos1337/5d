#!/usr/bin/env python3
"""
Export freigegebener Pilot-Datenspenden aus Supabase in den öffentlichen Datensatz.

Nur Zeilen mit approved = true werden übernommen. Die CSV wird bei jedem Lauf
vollständig neu geschrieben: Wird eine Spende in Supabase gelöscht (Widerruf)
oder die Freigabe zurückgenommen, verschwindet sie beim nächsten Export.

Umgebungsvariablen:
    SUPABASE_URL          z. B. https://abcd1234.supabase.co
    SUPABASE_SERVICE_KEY  service_role-Schlüssel (nur als GitHub-Secret, nie im Code)

Aufruf:
    python scripts/pilot_export.py            # Export nach DEFAULT_CSV
    python scripts/pilot_export.py --ping     # nur Verbindung prüfen (hält das Projekt wach)
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import sys
import urllib.request
from collections.abc import Callable
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "pilot_import", Path(__file__).resolve().parent / "pilot_import.py"
)
pilot_import = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(pilot_import)

TABLE = "pilot_submissions"
SELECT = "participant_code,submitted_month,age_group,attention_ok,imp,swls"


def fetch_json(url: str, key: str) -> list:
    request = urllib.request.Request(
        url, headers={"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 (feste https-URL)
        return json.loads(response.read().decode("utf-8"))


def approved_url(base_url: str) -> str:
    return (
        f"{base_url.rstrip('/')}/rest/v1/{TABLE}"
        f"?select={SELECT}&approved=eq.true&order=participant_code.asc"
    )


def row_from_record(record: dict) -> dict:
    """Prüft eine Supabase-Zeile und wandelt sie in eine CSV-Zeile um."""
    code = record.get("participant_code")
    if not isinstance(code, str) or not pilot_import.ID_PATTERN.match(code):
        raise pilot_import.SubmissionError(f"Ungültiger Teilnahme-Code: {code!r}")
    month = str(record.get("submitted_month", ""))[:7]
    if not pilot_import.MONTH_PATTERN.match(month):
        raise pilot_import.SubmissionError(f"{code}: ungültiger Monat")
    age = record.get("age_group", "")
    if age not in pilot_import.AGE_GROUPS:
        raise pilot_import.SubmissionError(f"{code}: ungültige Altersgruppe")
    if not isinstance(record.get("attention_ok"), bool):
        raise pilot_import.SubmissionError(f"{code}: ungültiger Aufmerksamkeits-Wert")
    imp = pilot_import._validate_answers(
        record.get("imp"), len(pilot_import.IMP_ITEMS), 1, 5, "IMP"
    )
    swls = pilot_import._validate_answers(
        record.get("swls"), len(pilot_import.SWLS_ITEMS), 1, 7, "SWLS"
    )

    row: dict = {
        "id": code,
        "monat": month,
        "altersgruppe": age,
        "aufmerksamkeit_ok": int(record["attention_ok"]),
    }
    row.update(zip(pilot_import.IMP_ITEMS, imp, strict=True))
    row.update(zip(pilot_import.SWLS_ITEMS, swls, strict=True))
    return row


def export(
    base_url: str,
    key: str,
    csv_path: Path = pilot_import.DEFAULT_CSV,
    fetch: Callable[[str, str], list] = fetch_json,
) -> int:
    """Schreibt alle freigegebenen Spenden in die CSV und gibt ihre Anzahl zurück."""
    rows = [row_from_record(r) for r in fetch(approved_url(base_url), key)]
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=pilot_import.COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def ping(base_url: str, key: str, fetch: Callable[[str, str], list] = fetch_json) -> None:
    fetch(f"{base_url.rstrip('/')}/rest/v1/{TABLE}?select=participant_code&limit=1", key)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freigegebene Pilot-Spenden exportieren")
    parser.add_argument("--ping", action="store_true", help="nur Verbindung prüfen")
    parser.add_argument("--csv", type=Path, default=pilot_import.DEFAULT_CSV)
    args = parser.parse_args(argv)

    base_url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_KEY", "").strip()
    if not base_url.startswith("https://") or not key:
        print(
            "SUPABASE_URL (https://…) und SUPABASE_SERVICE_KEY müssen gesetzt sein.",
            file=sys.stderr,
        )
        return 2

    try:
        if args.ping:
            ping(base_url, key)
            print("Supabase erreichbar.")
        else:
            count = export(base_url, key, args.csv)
            print(f"{count} freigegebene Spende(n) nach {args.csv} geschrieben.")
    except pilot_import.SubmissionError as exc:
        print(f"Abgebrochen, ungültige Zeile: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
