import argparse


# Add frontmatter to a markdown file
def add_frontmatter_to_file(filepath: str, title: str):
    """
    Adds frontmatter to a markdown file if it doesn't already have it.

    Args:
        filepath (str): The path to the markdown file.
        title (str): The title to use in the frontmatter.

    Returns True if frontmatter was added, False if already present.
    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if content.startswith("---"):
        return False

    frontmatter = f"---\ntitle: {title}\n---\n\n"
    new_content = frontmatter + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add frontmatter to a markdown file.")
    parser.add_argument("file", help="The markdown file to process.")
    parser.add_argument("--title", help="The title for the frontmatter.", default="Untitled")

    args = parser.parse_args()

    try:
        add_frontmatter_to_file(
            filepath=args.file,
            title=args.title,
        )
        print(f"✅ Processed {args.file}")
    except Exception as e:
        print(f"❌ Error processing {args.file}: {e}")
