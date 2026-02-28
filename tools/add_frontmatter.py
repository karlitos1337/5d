import argparse


def add_frontmatter_to_file(filepath, title):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if "---\n" in content:
        return False

    frontmatter = f"---\ntitle: {title}\n---\n\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    _ = add_frontmatter_to_file(args.file, args.title)
    print(f"Processed {args.file}")
