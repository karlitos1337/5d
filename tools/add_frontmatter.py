#!/usr/bin/env python3
"""
Add Frontmatter to Markdown Files
=================================
Fügt YAML-Frontmatter zu Markdown-Dateien hinzu, falls noch nicht vorhanden.
"""

import argparse
import os
from pathlib import Path

import yaml


def add_frontmatter_to_file(filepath, title=None, tags=None):
    """
    Fügt Frontmatter zu einer Datei hinzu.

    Args:
        filepath (str): Pfad zur Datei
        title (str, optional): Titel für Frontmatter. Wenn None, wird Dateiname verwendet.
        tags (list, optional): Liste von Tags.

    Returns:
        bool: True wenn Frontmatter hinzugefügt wurde, False wenn schon vorhanden.
    """
    path = Path(filepath)
    if not path.exists():
        print(f"❌ Datei nicht gefunden: {filepath}")
        return False

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ Fehler beim Lesen von {filepath}: {e}")
        return False

    # Check if frontmatter already exists (starts with ---)
    if content.strip().startswith("---"):
        print(f"⚠️  Frontmatter bereits vorhanden in {filepath}")
        return False

    # Prepare Frontmatter
    if title is None:
        # Use filename as title (remove extension and replace underscores)
        title = path.stem.replace("_", " ").title()

    frontmatter = {
        "title": title,
        "date": "2024-03-20",  # Default date or current date
        "tags": tags or ["5d-intelligence", "documentation"],
    }

    # Convert to YAML string
    yaml_str = yaml.dump(frontmatter, sort_keys=False).strip()

    new_content = f"---\n{yaml_str}\n---\n\n{content}"

    try:
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ Frontmatter hinzugefügt zu {filepath}")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Schreiben von {filepath}: {e}")
        return False


def process_directory(directory):
    """Verarbeitet alle Markdown-Dateien in einem Verzeichnis rekursiv."""
    print(f"📂 Verarbeite Verzeichnis: {directory}")
    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                add_frontmatter_to_file(filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add YAML frontmatter to markdown files.")
    parser.add_argument("path", help="File or directory path")
    parser.add_argument("--title", help="Title for the frontmatter (only for single file)")

    args = parser.parse_args()

    if os.path.isfile(args.path):
        _added = add_frontmatter_to_file(
            filepath=args.path,
            title=args.title,
        )
    elif os.path.isdir(args.path):
        process_directory(args.path)
    else:
        print("❌ Ungültiger Pfad.")
