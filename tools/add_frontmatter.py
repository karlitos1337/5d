#!/usr/bin/env python3
import argparse
import os

import yaml


def has_frontmatter(content):
    """
    Checks if the content string starts with YAML frontmatter.
    """
    return content.startswith("---\n")

def add_frontmatter_to_file(filepath, title=None):
    """
    Adds YAML frontmatter to a markdown file if it doesn't exist.
    Tries to infer title from filename if not provided.

    Returns True if frontmatter was added, False if already present.
    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if has_frontmatter(content):
        return False

    # Infer title from filename if needed
    if not title:
        filename = os.path.basename(filepath)
        title = os.path.splitext(filename)[0].replace("-", " ").replace("_", " ").title()

    frontmatter = {
        "title": title,
        "date": "2024-01-01", # Default date, could be dynamic
        "tags": ["documentation"],
        "author": "System"
    }

    yaml_frontmatter = "---\n" + yaml.dump(frontmatter, default_flow_style=False) + "---\n\n"

    new_content = yaml_frontmatter + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True

def process_directory(directory):
    """
    Recursively processes a directory to add frontmatter to .md files.
    """
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                if add_frontmatter_to_file(filepath):
                    print(f"Added frontmatter to: {filepath}")
                    count += 1
                else:
                    # print(f"Skipped (already has frontmatter): {filepath}")
                    pass
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add YAML frontmatter to markdown files.")
    parser.add_argument("--file", help="Specific file to process")
    parser.add_argument("--dir", help="Directory to process recursively")
    parser.add_argument("--title", help="Title to use (only for single file mode)")

    args = parser.parse_args()

    if args.file:
        try:
            add_frontmatter_to_file(
                filepath=args.file,
                title=args.title,
            )
            print(f"Processed {args.file}")
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
    elif args.dir:
        if os.path.isdir(args.dir):
            count = process_directory(args.dir)
            print(f"Processed {count} files in {args.dir}")
        else:
            print(f"Error: Directory not found: {args.dir}")
    else:
        print("Please provide --file or --dir argument.")
        parser.print_help()
