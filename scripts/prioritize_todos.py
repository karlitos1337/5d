import re
import sys
from collections import defaultdict
from pathlib import Path

SRC_FILES = [
    Path("TODO.md"),
    Path("TODO_MULTIPAGE.md"),
    Path("TODO_RESEARCH.md"),
    Path("TODO_COPILOT_INTEGRATION.md"),
    Path("MEGA_TODO_CONSOLIDATED.md"),
]

PRIORITY_KEYWORDS = {
    "PRIORITÄT 1": ["WISSENSCHAFT", "RESEARCH", "BUG", "KRITISCH"],
    "PRIORITÄT 2": ["DASHBOARD", "UI/UX", "KARTEN", "PAGES"],
    "PRIORITÄT 3": ["INFRASTRUCTURE", "DEPLOY", "CI", "DOCS"],
}


def classify(item: str) -> str:
    up = item.upper()
    for prio, kws in PRIORITY_KEYWORDS.items():
        if any(k in up for k in kws):
            return prio
    return "PRIORITÄT 2"  # default middle bucket


def main() -> int:
    seen = set()
    buckets = defaultdict(list)
    sources = defaultdict(int)

    for p in SRC_FILES:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if re.match(r"^[-*] \[[ xX]\] ", line):
                key = re.sub(r"\s+", " ", line.strip())
                if key in seen:
                    continue
                seen.add(key)
                prio = classify(key)
                buckets[prio].append(key)
                sources[p.name] += 1

    out = []
    out.append("# 🔥 MEGA TODO LIST – PRIORITIZED\n")
    total = sum(len(v) for v in buckets.values())
    out.append(f"**Total Items:** {total}\n")
    for prio in ["PRIORITÄT 1", "PRIORITÄT 2", "PRIORITÄT 3"]:
        out.append(f"\n## {prio} ({len(buckets[prio])})\n")
        out.extend(buckets[prio])
    out.append("\n---\nQuellen-Zusammenfassung:\n")
    for src, cnt in sorted(sources.items()):
        out.append(f"- {src}: {cnt} Items")

    Path("MEGA_TODO_CONSOLIDATED_PRIORITIZED.md").write_text(
        "\n".join(out), encoding="utf-8"
    )
    print(f"Wrote MEGA_TODO_CONSOLIDATED_PRIORITIZED.md with {total} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
