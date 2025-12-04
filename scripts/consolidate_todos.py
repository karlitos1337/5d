import re
import sys
from pathlib import Path

SRC_FILES = [
    Path("TODO.md"),
    Path("TODO_MULTIPAGE.md"),
    Path("TODO_RESEARCH.md"),
    Path("TODO_COPILOT_INTEGRATION.md"),
]

HEADER = "# 🔥 MEGA TODO LIST – COMPLETE PROJECT INVENTORY\n\n"


def extract_items(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        if re.match(r"^[-*] \[[ xX]\] ", line):
            items.append(line.strip())
    return items


def main() -> int:
    out = [HEADER]
    total = 0
    missing = []
    for p in SRC_FILES:
        if not p.exists():
            missing.append(str(p))
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        items = extract_items(text)
        total += len(items)
        out.append(f"## Quelle: {p.name} ({len(items)} Items)\n")
        out.extend([f"- {i}" for i in items])
        out.append("\n")
    out.append(f"**Total Items:** {total}\n")
    if missing:
        out.append(f"\n⚠️ Missing sources: {', '.join(missing)}\n")

    Path("MEGA_TODO_CONSOLIDATED.md").write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote MEGA_TODO_CONSOLIDATED.md with {total} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
