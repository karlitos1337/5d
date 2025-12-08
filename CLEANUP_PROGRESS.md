# Cleanup Progress Report

**Branch:** `cleanup/structure-audit-2025-12-08`  
**Started:** 2025-12-08 23:11 CET  
**Status:** 🟡 IN PROGRESS (Phase 1/4 completed)

---

## ✅ PHASE 1: COMPLETED

**Ziel:** Zielordner erstellen

**Ausgeführt:**
- ✅ `99_unsortiert/archiv/.gitkeep` erstellt
- ✅ `outputs/surveys/.gitkeep` erstellt

**Commits:**
- [d5b87db](https://github.com/karlitos1337/5d/commit/d5b87dbd762dc628b1a3b67d76843d9e99614867) - Phase 1: Create archiv structure
- [3f837db](https://github.com/karlitos1337/5d/commit/3f837dbe9418d6404578afda52dbf06a1c2742a5) - Phase 1: Create outputs structure

---

## 🟡 PHASE 2-4: PENDING (Manual Operations Needed)

**Problem:** GitHub API erlaubt **keine** Folder-Operationen (move/rename/copy).

**Lösung:** Ich dokumentiere die **genauen Schritte**, die du **lokal** ausführen kannst.

---

## 📝 PHASE 2-4: MANUAL SCRIPT

### **Option A: Bash Script (empfohlen)**

Erstelle `scripts/cleanup_phase2-4.sh`:

```bash
#!/bin/bash
# Cleanup Phase 2-4: Merge duplicates, move files
# Branch: cleanup/structure-audit-2025-12-08
# DO NOT RUN ON MAIN BRANCH!

set -e  # Exit on error

echo "🧹 Starting Cleanup Phase 2-4..."

# ============================================
# PHASE 2: MERGE DUPLICATES
# ============================================

echo "
🔄 PHASE 2: Merging duplicate folders..."

# 2.1 Merge 03-philosophie/ -> 03_philosophie_epistemologie/
if [ -d "03-philosophie" ]; then
  echo "  ├─ Merging 03-philosophie/ -> 03_philosophie_epistemologie/"
  cp -r 03-philosophie/epistemologie/* 03_philosophie_epistemologie/ 2>/dev/null || true
  mv 03-philosophie 99_unsortiert/archiv/03-philosophie-OLD
  echo "  └─ ✅ Archived to 99_unsortiert/archiv/03-philosophie-OLD"
fi

# 2.2 Merge 05-technologie/ -> 05_technologie_tesla/
if [ -d "05-technologie" ]; then
  echo "  ├─ Merging 05-technologie/ -> 05_technologie_tesla/"
  # Check if examples/ exists in target
  if [ ! -d "05_technologie_tesla/examples" ]; then
    cp -r 05-technologie/examples 05_technologie_tesla/ 2>/dev/null || true
  fi
  # Merge README if different
  if [ -f "05-technologie/README.md" ] && [ -f "05_technologie_tesla/README.md" ]; then
    echo "  ├─ ⚠️  Both READMEs exist, manual merge needed!"
    cp 05-technologie/README.md 99_unsortiert/archiv/05-technologie-README.md
  fi
  mv 05-technologie 99_unsortiert/archiv/05-technologie-OLD
  echo "  └─ ✅ Archived to 99_unsortiert/archiv/05-technologie-OLD"
fi

# 2.3 Merge new/ -> 99_unsortiert/new/
if [ -d "new" ]; then
  echo "  ├─ Merging new/ -> 99_unsortiert/new/"
  mkdir -p 99_unsortiert/new
  cp -r new/* 99_unsortiert/new/ 2>/dev/null || true
  rm -rf new
  echo "  └─ ✅ Merged and removed new/"
fi

# 2.4 Merge TODO_COPILOT_INTEGRATION.md -> TODO.md
if [ -f "TODO_COPILOT_INTEGRATION.md" ]; then
  echo "  ├─ Merging TODO_COPILOT_INTEGRATION.md -> TODO.md"
  echo "\n\n## Copilot Integration (merged from TODO_COPILOT_INTEGRATION.md)\n" >> TODO.md
  cat TODO_COPILOT_INTEGRATION.md >> TODO.md
  mv TODO_COPILOT_INTEGRATION.md 99_unsortiert/archiv/
  echo "  └─ ✅ Merged and archived"
fi

echo "✅ PHASE 2 completed!"

# ============================================
# PHASE 3: MOVE FILES
# ============================================

echo "\n📦 PHASE 3: Moving scattered files..."

# 3.1 Move timestamp files to outputs/surveys/
echo "  ├─ Moving timestamp files..."
mkdir -p outputs/surveys/example_responses
mkdir -p outputs/surveys/questionnaires
mkdir -p outputs/validation/reports
mkdir -p outputs/validation/plots

mv example_responses_*.csv outputs/surveys/example_responses/ 2>/dev/null || true
mv questionnaire_*.json outputs/surveys/questionnaires/ 2>/dev/null || true
mv validation_report_*.json outputs/validation/reports/ 2>/dev/null || true
mv validation_results_*.png outputs/validation/plots/ 2>/dev/null || true

echo "  └─ ✅ Timestamp files moved"

# 3.2 Move data files
echo "  ├─ Moving data files..."
mkdir -p data/github
mkdir -p data/research
mkdir -p data/solutions
mkdir -p outputs/model_comparison

mv 5d_github_data.json data/github/ 2>/dev/null || true
mv 5d_research_data.json data/research/ 2>/dev/null || true
mv 5d_solutions.json data/solutions/ 2>/dev/null || true
mv model_comparison_data.csv outputs/model_comparison/ 2>/dev/null || true
mv model_comparison_results.png outputs/model_comparison/ 2>/dev/null || true

echo "  └─ ✅ Data files moved"

# 3.3 Archive obsolete TODOs
echo "  ├─ Archiving obsolete TODOs..."
mv MEGA_TODO_CONSOLIDATED.md 99_unsortiert/archiv/ 2>/dev/null || true
mv MEGA_TODO_CONSOLIDATED_PRIORITIZED.md 99_unsortiert/archiv/ 2>/dev/null || true

echo "  └─ ✅ TODOs archived"

echo "✅ PHASE 3 completed!"

# ============================================
# PHASE 4: RENAME FOLDERS
# ============================================

echo "\n🔄 PHASE 4: Renaming folders for consistency..."

# 4.1 Rename 08-experimente-validierung/ -> 08_experimente_validierung/
if [ -d "08-experimente-validierung" ]; then
  echo "  ├─ Renaming 08-experimente-validierung/ -> 08_experimente_validierung/"
  mv 08-experimente-validierung 08_experimente_validierung
  echo "  └─ ✅ Renamed"
fi

# 4.2 Rename 99_noch_zu_bearbeiten/ -> 99_unsortiert/
if [ -d "99_noch_zu_bearbeiten" ]; then
  echo "  ├─ Merging 99_noch_zu_bearbeiten/ -> 99_unsortiert/"
  # Merge contents (archiv/ already exists)
  cp -r 99_noch_zu_bearbeiten/* 99_unsortiert/ 2>/dev/null || true
  rm -rf 99_noch_zu_bearbeiten
  echo "  └─ ✅ Merged and renamed"
fi

echo "✅ PHASE 4 completed!"

echo "\n✅ ALL PHASES COMPLETED!"
echo "📝 Next: Review changes with 'git status' and commit."
```

---

### **Option B: Python Script (alternative)**

Erstelle `scripts/cleanup_phase2-4.py`:

```python
#!/usr/bin/env python3
"""Cleanup Phase 2-4: Merge duplicates, move files"""

import os
import shutil
from pathlib import Path

def main():
    print("🧹 Starting Cleanup Phase 2-4...\n")
    
    # PHASE 2: Merge duplicates
    print("🔄 PHASE 2: Merging duplicate folders...")
    
    # 2.1 Merge 03-philosophie/
    if Path("03-philosophie").exists():
        print("  ├─ Merging 03-philosophie/ -> 03_philosophie_epistemologie/")
        if Path("03-philosophie/epistemologie").exists():
            for item in Path("03-philosophie/epistemologie").iterdir():
                shutil.copy2(item, "03_philosophie_epistemologie/")
        shutil.move("03-philosophie", "99_unsortiert/archiv/03-philosophie-OLD")
        print("  └─ ✅ Archived")
    
    # 2.2 Merge 05-technologie/
    if Path("05-technologie").exists():
        print("  ├─ Merging 05-technologie/ -> 05_technologie_tesla/")
        if Path("05-technologie/examples").exists():
            if not Path("05_technologie_tesla/examples").exists():
                shutil.copytree("05-technologie/examples", "05_technologie_tesla/examples")
        shutil.move("05-technologie", "99_unsortiert/archiv/05-technologie-OLD")
        print("  └─ ✅ Archived")
    
    # 2.3 Merge new/
    if Path("new").exists():
        print("  ├─ Merging new/ -> 99_unsortiert/new/")
        Path("99_unsortiert/new").mkdir(parents=True, exist_ok=True)
        for item in Path("new").iterdir():
            shutil.move(str(item), "99_unsortiert/new/")
        Path("new").rmdir()
        print("  └─ ✅ Merged")
    
    print("✅ PHASE 2 completed!\n")
    
    # PHASE 3: Move files
    print("📦 PHASE 3: Moving scattered files...")
    
    # Create target directories
    dirs = [
        "outputs/surveys/example_responses",
        "outputs/surveys/questionnaires",
        "outputs/validation/reports",
        "outputs/validation/plots",
        "data/github",
        "data/research",
        "data/solutions",
        "outputs/model_comparison"
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    
    # Move timestamp files
    moves = {
        "example_responses_*.csv": "outputs/surveys/example_responses/",
        "questionnaire_*.json": "outputs/surveys/questionnaires/",
        "validation_report_*.json": "outputs/validation/reports/",
        "validation_results_*.png": "outputs/validation/plots/",
        "5d_github_data.json": "data/github/",
        "5d_research_data.json": "data/research/",
        "5d_solutions.json": "data/solutions/",
        "model_comparison_data.csv": "outputs/model_comparison/",
        "model_comparison_results.png": "outputs/model_comparison/"
    }
    
    for pattern, target in moves.items():
        for f in Path(".").glob(pattern):
            if f.is_file():
                shutil.move(str(f), target)
                print(f"  ├─ Moved {f.name} -> {target}")
    
    print("✅ PHASE 3 completed!\n")
    
    # PHASE 4: Rename folders
    print("🔄 PHASE 4: Renaming folders...")
    
    if Path("08-experimente-validierung").exists():
        shutil.move("08-experimente-validierung", "08_experimente_validierung")
        print("  └─ ✅ Renamed 08-experimente-validierung/")
    
    print("✅ PHASE 4 completed!\n")
    print("✅ ALL PHASES COMPLETED!")

if __name__ == "__main__":
    main()
```

---

## 🛠️ AUSFÜHRUNG (Lokal)

### **1. Repository klonen & Branch wechseln**
```bash
git clone https://github.com/karlitos1337/5d.git
cd 5d
git checkout cleanup/structure-audit-2025-12-08
```

### **2. Script ausführen**

**Option A (Bash):**
```bash
chmod +x scripts/cleanup_phase2-4.sh
./scripts/cleanup_phase2-4.sh
```

**Option B (Python):**
```bash
python3 scripts/cleanup_phase2-4.py
```

### **3. Review & Commit**
```bash
git status
git add -A
git commit -m "Phase 2-4: Merge duplicates, move files, rename folders

- Merged 03-philosophie/ -> 03_philosophie_epistemologie/
- Merged 05-technologie/ -> 05_technologie_tesla/
- Moved timestamp files -> outputs/
- Moved data files -> data/
- Renamed folders for consistency"
git push origin cleanup/structure-audit-2025-12-08
```

### **4. Pull Request erstellen**

Gehe zu https://github.com/karlitos1337/5d/compare/cleanup/structure-audit-2025-12-08

---

## 📊 STATUSÜBERSICHT

| Phase | Status | Details |
|-------|--------|--------|
| **Phase 1** | ✅ DONE | Archiv + Outputs Ordner erstellt |
| **Phase 2** | ⚠️ MANUAL | Merge duplicates (Script bereit) |
| **Phase 3** | ⚠️ MANUAL | Move files (Script bereit) |
| **Phase 4** | ⚠️ MANUAL | Rename folders (Script bereit) |
| **Phase 5** | ⏸️ PENDING | Delete after review |

---

## ❓ NÄCHSTE SCHRITTE

**JETZT:**
1. 💻 Script lokal ausführen (siehe oben)
2. 👀 Review mit `git status`
3. 📝 Commit + Push

**DANN:**
4. 🔀 Pull Request erstellen
5. 👀 Review Diff auf GitHub
6. ✅ Merge wenn alles OK

**SPÄTER:**
7. 🗑️ Phase 5: Delete nach Bestätigung

---

**Last Updated:** 2025-12-08 23:12 CET  
**Branch:** [cleanup/structure-audit-2025-12-08](https://github.com/karlitos1337/5d/tree/cleanup/structure-audit-2025-12-08)
