#!/usr/bin/env python3
"""
Adds a frontmatter block (title, description) to the beginning of a file.
Useful for prepping files for LLM context or documentation.
"""

import argparse
import os
import sys


def add_frontmatter_to_file(filepath, title=None, description=None):
    """
    Adds frontmatter to the file if it doesn't already exist.

    Args:
        filepath (str): Path to the file.
        title (str, optional): Title to add.
        description (str, optional): Description to add.

    Returns:
        bool: True if frontmatter was added, False if already present.
    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Check if frontmatter already exists (naive check)
    if content.strip().startswith('"""') or content.strip().startswith("'''"):
        # print(f"ℹ️  Frontmatter might already exist in {filepath}")
        return False

    filename = os.path.basename(filepath)
    if not title:
        title = filename

    frontmatter = f'"""\n{title}\n'
    if description:
        frontmatter += f"\n{description}\n"
    frontmatter += '"""\n\n'

    new_content = frontmatter + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def process_directory(directory, recursive=False):
    """
    Process all python files in a directory.
    """
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                if add_frontmatter_to_file(filepath):
                    print(f"✅ Added frontmatter to: {filepath}")
                    count += 1

        if not recursive:
            break

    print(f"\n🎉 Processed {count} files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add docstring frontmatter to Python files.")
    parser.add_argument("file", help="File or directory to process")
    parser.add_argument("--title", "-t", help="Title to add (default: filename)")
    parser.add_argument("--desc", "-d", help="Description to add")
    parser.add_argument("--recursive", "-r", action="store_true", help="Process directories recursively")

    args = parser.parse_args()

    if os.path.isdir(args.file):
        process_directory(args.file, args.recursive)
    elif os.path.isfile(args.file):
        try:
            add_frontmatter_to_file(
                filepath=args.file,
                title=args.title,
                description=args.desc
            )
            print(f"✅ Processed {args.file}")
        except Exception as e:
            print(f"❌ Error processing {args.file}: {e}")
    else:
        print(f"❌ Path not found: {args.file}")
        sys.exit(1)
