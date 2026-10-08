#!/usr/bin/env python3
"""
Gemeinsame Prüfregeln für Pilot-Datenspenden und lokaler Import alter Spenden-Codes.

Die Spende läuft inzwischen über Supabase (siehe docs/PILOT_TEILNAHME.md und
scripts/pilot_export.py). Dieses Modul enthält die Spalten, Wertebereiche und
Prüffunktionen, die der Export mitbenutzt. Lokal lassen sich damit weiterhin
einzelne Codes im alten Format einlesen:

    python scripts/pilot_import.py "5DP1.…"
    python scripts/pilot_import.py K7Q2-9XPA --remove

Ein Code enthält keine Namen, E-Mail-Adressen oder Freitexte.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import re
import sys
from pathlib import Path

PREFIX = "5DP1."
SCHEMA_VERSION = 1

IMP_ITEMS = [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "P1",
    "P2",
    "P3",
    "P4",
    "P5",
    "Au1",
    "Au2",
    "Au3",
    "Au4",
    "Au5",
]
SWLS_ITEMS = ["SWLS1", "SWLS2", "SWLS3", "SWLS4", "SWLS5"]
AGE_GROUPS = {"", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"}

ID_PATTERN = re.compile(r"^[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}$")
MONTH_PATTERN = re.compile(r"^20\d{2}-(0[1-9]|1[0-2])$")

COLUMNS = ["id", "monat", "altersgruppe", "aufmerksamkeit_ok", *IMP_ITEMS, *SWLS_ITEMS]

DEFAULT_CSV = Path("08_experimente_validierung/data/pilot_responses.csv")


class SubmissionError(ValueError):
    """Der Code ist ungültig oder unvollständig."""


def decode_submission(code: str) -> dict:
    """Prüft einen Spenden-Code und gibt eine CSV-Zeile als dict zurück."""
    code = code.strip()
    if not code.startswith(PREFIX):
        raise SubmissionError(f"Code muss mit '{PREFIX}' beginnen.")

    raw = code[len(PREFIX) :]
    padding = "=" * (-len(raw) % 4)
    try:
        payload = json.loads(base64.urlsafe_b64decode(raw + padding).decode("ascii"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise SubmissionError("Code lässt sich nicht dekodieren.") from exc

    if not isinstance(payload, dict):
        raise SubmissionError("Code hat kein gültiges Format.")

    expected_keys = {"v", "id", "m", "age", "att", "imp", "swls"}
    if set(payload) != expected_keys:
        raise SubmissionError("Code enthält unerwartete oder fehlende Felder.")
    if payload["v"] != SCHEMA_VERSION:
        raise SubmissionError("Unbekannte Fragebogen-Version.")
    if not isinstance(payload["id"], str) or not ID_PATTERN.match(payload["id"]):
        raise SubmissionError("Ungültiger Teilnahme-Code.")
    if not isinstance(payload["m"], str) or not MONTH_PATTERN.match(payload["m"]):
        raise SubmissionError("Ungültiger Monat.")
    if payload["age"] not in AGE_GROUPS:
        raise SubmissionError("Ungültige Altersgruppe.")
    if not isinstance(payload["att"], bool):
        raise SubmissionError("Ungültiger Aufmerksamkeits-Wert.")

    imp = _validate_answers(payload["imp"], len(IMP_ITEMS), 1, 5, "IMP")
    swls = _validate_answers(payload["swls"], len(SWLS_ITEMS), 1, 7, "SWLS")

    row: dict = {
        "id": payload["id"],
        "monat": payload["m"],
        "altersgruppe": payload["age"],
        "aufmerksamkeit_ok": int(payload["att"]),
    }
    row.update(zip(IMP_ITEMS, imp, strict=True))
    row.update(zip(SWLS_ITEMS, swls, strict=True))
    return row


def _validate_answers(values, count: int, low: int, high: int, name: str) -> list[int]:
    if not isinstance(values, list) or len(values) != count:
        raise SubmissionError(f"{name}: erwartet {count} Antworten.")
    for value in values:
        # bool ist eine Unterklasse von int und wird deshalb ausdrücklich ausgeschlossen.
        if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
            raise SubmissionError(
                f"{name}: Antworten müssen ganze Zahlen von {low} bis {high} sein."
            )
    return values


def append_submission(code: str, csv_path: Path = DEFAULT_CSV) -> dict:
    """Prüft den Code und hängt ihn an die CSV an. Doppelte Codes werden abgelehnt."""
    row = decode_submission(code)

    if csv_path.exists():
        with csv_path.open(newline="", encoding="utf-8") as f:
            if any(existing["id"] == row["id"] for existing in csv.DictReader(f)):
                raise SubmissionError(f"Teilnahme-Code {row['id']} ist bereits eingetragen.")
        write_header = False
    else:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        write_header = True

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    return row


def remove_submission(participant_id: str, csv_path: Path = DEFAULT_CSV) -> bool:
    """Entfernt einen Datensatz auf Wunsch der teilnehmenden Person (Widerruf)."""
    if not csv_path.exists():
        return False
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    kept = [r for r in rows if r["id"] != participant_id]
    if len(kept) == len(rows):
        return False
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(kept)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pilot-Datenspende freigeben und einpflegen")
    parser.add_argument(
        "code", help="Spenden-Code (beginnt mit 5DP1.) oder bei --remove der Teilnahme-Code"
    )
    parser.add_argument(
        "--remove", action="store_true", help="Datensatz mit diesem Teilnahme-Code löschen"
    )
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args(argv)

    try:
        if args.remove:
            if not remove_submission(args.code.strip(), args.csv):
                print(f"Kein Datensatz mit Code {args.code} gefunden.", file=sys.stderr)
                return 1
            print(f"Datensatz {args.code} entfernt.")
        else:
            row = append_submission(args.code, args.csv)
            print(f"Datensatz {row['id']} eingetragen.")
    except SubmissionError as exc:
        print(f"Abgelehnt: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
