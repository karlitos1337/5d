#!/usr/bin/env python3
"""
Utility to add YAML frontmatter to markdown files that are missing it.

Usage:
    python tools/add_frontmatter.py path/to/file.md --title "My Title" --domain "01_bildung_education"

Only adds frontmatter if the file is missing a YAML frontmatter block.
"""

import argparse
import re
import sys
from datetime import date

RE_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def has_frontmatter(content: str) -> bool:
    """Check if content starts with a YAML frontmatter block."""
    return bool(RE_FRONTMATTER.search(content))


def create_frontmatter(
    title: str,
    author: str = "Unknown",
    file_date: str = None,
    domain: str = "",
    license_type: str = "CC-BY-4.0",
    evidence: str = "🔮",
) -> str:
    """Generate a YAML frontmatter block."""
    if file_date is None:
        file_date = date.today().isoformat()
    return f'''---
title: "{title}"
author: "{author}"
date: "{file_date}"
domain: "{domain}"
license: "{license_type}"
evidence: "{evidence}"
---

'''


def add_frontmatter_to_file(
    filepath: str,
    title: str,
    domain: str,
    author: str = "Unknown",
    file_date: str = None,
    license_type: str = "CC-BY-4.0",
    evidence: str = "🔮",
    dry_run: bool = False,
) -> bool:
    """
    Add frontmatter to a file if it's missing.

    Returns True if frontmatter was added, False if already present.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if has_frontmatter(content):
        print(f"Skipped (already has frontmatter): {filepath}")
        return False

    frontmatter = create_frontmatter(
        title=title,
        author=author,
        file_date=file_date,
        domain=domain,
        license_type=license_type,
        evidence=evidence,
    )

    new_content = frontmatter + content

    if dry_run:
        print(f"Would add frontmatter to: {filepath}")
        print(frontmatter)
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Added frontmatter to: {filepath}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Add YAML frontmatter to markdown files"
    )
    parser.add_argument("file", help="Path to the markdown file")
    parser.add_argument("--title", required=True, help="Document title")
    parser.add_argument("--domain", required=True, help="Domain/folder name")
    parser.add_argument("--author", default="Unknown", help="Author name")
    parser.add_argument("--date", default=None, help="Date (YYYY-MM-DD format)")
    parser.add_argument("--license", default="CC-BY-4.0", help="License type")
    parser.add_argument("--evidence", default="🔮", help="Evidence level (✅, ⚠️, or 🔮)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )

    args = parser.parse_args()

    try:
        added = add_frontmatter_to_file(
            filepath=args.file,
            title=args.title,
            domain=args.domain,
            author=args.author,
            file_date=args.date,
            license_type=args.license,
            evidence=args.evidence,
            dry_run=args.dry_run,
        )
        return 0 if added or args.dry_run else 0
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
