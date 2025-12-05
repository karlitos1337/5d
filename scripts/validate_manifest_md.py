import argparse
import sys
from pathlib import Path

FRONTMATTER = "---\n# minimal YAML frontmatter\n# title: <auto>\n---\n"


def scan_files(base: Path) -> list[Path]:
    return [p for p in base.rglob("*.md")]


def has_frontmatter(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            first = f.readline().strip()
            return first == "---"
    except Exception:
        return False


def fix_frontmatter(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        path.write_text(FRONTMATTER + text, encoding="utf-8")
        return True
    except Exception:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter in manifest Markdown files"
    )
    parser.add_argument("manifest_dir", nargs="?", default="manifest", help="Base manifest dir")
    parser.add_argument(
        "--fix", action="store_true", help="Automatically add minimal frontmatter where missing"
    )
    args = parser.parse_args()

    base = Path(args.manifest_dir)
    if not base.exists():
        print(f"Error: manifest base not found: {base}")
        return 2

    files = scan_files(base)
    print(f"📄 Scanning {len(files)} markdown files under {base}...")
    missing = []
    for p in files:
        if not has_frontmatter(p):
            missing.append(p)

    if missing:
        print("❌ Metadata validation failed:")
        for m in missing:
            print(f"Error: {m}: Missing YAML frontmatter (must start with ---)")
        if args.fix:
            print("🔧 Attempting to add minimal frontmatter...")
            fixed = 0
            for m in missing:
                if fix_frontmatter(m):
                    fixed += 1
            print(f"✅ Fixed {fixed}/{len(missing)} files")
            return 0 if fixed == len(missing) else 1
        return 1
    else:
        print("✅ Metadata validation passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
