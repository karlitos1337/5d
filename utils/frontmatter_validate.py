#!/usr/bin/env python3
import os
import re
import sys

try:
    import yaml
except Exception:
    print(
        "Missing dependency: pyyaml. Install via 'pip install pyyaml'", file=sys.stderr
    )
    sys.exit(2)

RE_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
RE_MARKDOWN = re.compile(r"\.md$", re.IGNORECASE)

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(REPO_ROOT)

REQUIRED_FIELDS = [
    "title",
    "author",
    "date",
    "domain",
    "license",
    "evidence",  # one of: ✅, ⚠️, 🔮
]

OPTIONAL_FIELDS = [
    "bibtex_keys",  # list of strings
]

VALID_EVIDENCE = {"✅", "⚠️", "🔮"}
VALID_LICENSES = {"CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0", "MIT", "Proprietary"}

TARGET_DIRS = [
    "01_bildung_education",
    "02_neurobiologie_psychologie",
    "03_philosophie_epistemologie",
    "03-philosophie",
    "04_oekonomie_governance",
    "05_technologie_tesla",
    "05-technologie",
    "06_synthesen_kompilationen",
    "07_daten_analysen",
    "08-experimente-validierung",
    "99_noch_zu_bearbeiten",
]


def find_markdown_files() -> list[str]:
    files = []
    for td in TARGET_DIRS:
        absd = os.path.join(REPO_ROOT, td)
        if not os.path.isdir(absd):
            continue
        for root, _, filenames in os.walk(absd):
            for fn in filenames:
                if RE_MARKDOWN.search(fn):
                    files.append(os.path.join(root, fn))
    return files


def parse_frontmatter(text: str) -> tuple[dict, int]:
    m = RE_FRONTMATTER.search(text)
    if not m:
        return {}, 0
    block = m.group(1)
    try:
        data = yaml.safe_load(block) or {}
        return data, len(block)
    except Exception as e:
        return {"_error": f"YAML parse error: {e}"}, -1


def validate_frontmatter(data: dict, path: str) -> list[str]:
    errors = []
    if not data:
        errors.append(f"{path}: missing YAML frontmatter block")
        return errors

    if "_error" in data:
        errors.append(f"{path}: {data['_error']}")
        return errors

    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            errors.append(f"{path}: missing required field '{f}'")

    # evidence
    ev = data.get("evidence")
    if ev and ev not in VALID_EVIDENCE:
        errors.append(f"{path}: evidence must be one of {sorted(VALID_EVIDENCE)}")

    # license
    lic = data.get("license")
    if lic and lic not in VALID_LICENSES:
        errors.append(f"{path}: license should be one of {sorted(VALID_LICENSES)}")

    # bibtex_keys (optional list of strings)
    bk = data.get("bibtex_keys")
    if bk is not None:
        if not isinstance(bk, (list, tuple)) or not all(isinstance(x, str) for x in bk):
            errors.append(f"{path}: bibtex_keys must be a list of strings")

    # date simple check: YYYY-MM-DD
    dt = data.get("date")
    if dt and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(dt)):
        errors.append(f"{path}: date should be in YYYY-MM-DD format")

    # domain recommendation: 01–08 folder name
    dom = data.get("domain")
    if not dom:
        # recommend based on folder name
        folder = os.path.basename(os.path.dirname(path))
        errors.append(f"{path}: domain missing; consider '{folder}'")

    return errors


def main() -> int:
    files = find_markdown_files()
    all_errors: list[str] = []
    for p in files:
        try:
            with open(p, encoding="utf-8") as f:
                txt = f.read()
        except Exception as e:
            all_errors.append(f"{p}: cannot read file: {e}")
            continue
        data, _ = parse_frontmatter(txt)
        errs = validate_frontmatter(data, p)
        all_errors.extend(errs)

    if all_errors:
        print("Frontmatter validation found issues:\n", file=sys.stderr)
        for e in all_errors:
            print(f"- {e}", file=sys.stderr)
        return 1
    else:
        print("Frontmatter validation: OK (no issues found)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
