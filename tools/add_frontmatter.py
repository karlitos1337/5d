#!/usr/bin/env python3
"""
Adds frontmatter to a markdown file or all markdown files in a directory.
Usage: python tools/add_frontmatter.py <file_or_directory> --title <title>
"""

import argparse
import datetime
import os


def add_frontmatter_to_file(filepath, title=None):
    """
    Adds frontmatter to a single file.
    If title is not provided, it attempts to infer it from the filename.
    """
    filename = os.path.basename(filepath)
    if title is None:
        # Infer title from filename: "01_introduction.md" -> "Introduction"
        name_part = os.path.splitext(filename)[0]
        # Remove leading numbers and underscores
        clean_name = name_part.lstrip("0123456789_").replace("_", " ").title()
        title = clean_name

    # Check if frontmatter already exists
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if content.startswith("---"):
        print(f"Skipping {filename}: Frontmatter already exists.")
        return False

    # Create frontmatter
    # Get current date
    date_str = datetime.date.today().isoformat()

    frontmatter = f"""---
title: {title}
date: {date_str}
---

"""

    new_content = frontmatter + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Added frontmatter to {filename}")
    return True


def process_directory(directory):
    """
    Process all .md files in a directory.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") and not file.startswith("."):
                filepath = os.path.join(root, file)
                add_frontmatter_to_file(filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add frontmatter to markdown files.")
    parser.add_argument("file", help="File or directory to process")
    parser.add_argument(
        "--title", help="Title for the frontmatter (only for single file)", default=None
    )

    args = parser.parse_args()

    if os.path.isdir(args.file):
        process_directory(args.file)
    elif os.path.isfile(args.file):
        try:
            add_frontmatter_to_file(
                filepath=args.file,
                title=args.title,
            )
        except Exception as e:
            print(f"Error processing {args.file}: {e}")
    else:
        print(f"Error: {args.file} not found.")
