#!/usr/bin/env python3
"""
Helper script to add frontmatter to markdown files.
"""

import argparse
import os
import re
from datetime import datetime


def add_frontmatter_to_file(filepath, title=None, description=None, tags=None):
    """
    Adds YAML frontmatter to a markdown file if it doesn't exist.
    """
    if not filepath.endswith(".md"):
        print(f"Skipping non-markdown file: {filepath}")
        return False

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Check if frontmatter already exists
    if content.startswith("---"):
        print(f"Frontmatter already exists in: {filepath}")
        return False

    # Generate frontmatter
    filename = os.path.basename(filepath)
    name = os.path.splitext(filename)[0]

    # Infer title if not provided
    if not title:
        # Try to find first h1 header
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
        else:
            title = name.replace("-", " ").replace("_", " ").title()

    # Default values
    date = datetime.now().strftime("%Y-%m-%d")

    frontmatter = [
        "---",
        f"title: \"{title}\"",
        f"date: {date}",
    ]

    if description:
        frontmatter.append(f"description: \"{description}\"")

    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        frontmatter.append("tags:")
        for tag in tag_list:
            frontmatter.append(f"  - {tag}")

    frontmatter.append("---\n\n")

    new_content = "\n".join(frontmatter) + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Added frontmatter to: {filepath}")
    return True


def process_directory(directory, tags=None):
    """
    Process all markdown files in a directory.
    """
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                if add_frontmatter_to_file(filepath, tags=tags):
                    count += 1
    print(f"\nProcessed {count} files in {directory}")


def main():
    parser = argparse.ArgumentParser(description="Add YAML frontmatter to markdown files.")
    parser.add_argument("path", help="File or directory path")
    parser.add_argument("--title", help="Title (for single file)")
    parser.add_argument("--tags", help="Comma-separated tags")

    args = parser.parse_args()

    if os.path.isfile(args.path):
        # We don't use the return value here, so simply call the function
        add_frontmatter_to_file(
            filepath=args.path,
            title=args.title,
            tags=args.tags
        )
    elif os.path.isdir(args.path):
        process_directory(args.path, tags=args.tags)
    else:
        print("Invalid path")

if __name__ == "__main__":
    main()
