#!/bin/bash
# Cleanup Phase 2-4: Merge duplicates, move files
# Branch: cleanup/structure-audit-2025-12-08
# DO NOT RUN ON MAIN BRANCH!

set -e  # Exit on error

echo "🧹 Starting Cleanup Phase 2-4..."

# ============================================
# PHASE 2: MERGE DUPLICATES
# ============================================

echo ""
echo "🔄 PHASE 2: Merging duplicate folders..."

# 2.1 Merge 03-philosophie/ -> 03_philosophie_epistemologie/
if [ -d "03-philosophie" ]; then
  echo "  ├─ Merging 03-philosophie/ -> 03_philosophie_epistemologie/"
  if [ -d "03-philosophie/epistemologie" ]; then
    cp -r 03-philosophie/epistemologie/* 03_philosophie_epistemologie/ 2>/dev/null || true
  fi
  mv 03-philosophie 99_unsortiert/archiv/03-philosophie-OLD
  echo "  └─ ✅ Archived to 99_unsortiert/archiv/03-philosophie-OLD"
else
  echo "  └─ ⏭️  03-philosophie/ not found, skipping"
fi

# 2.2 Merge 05-technologie/ -> 05_technologie_tesla/
if [ -d "05-technologie" ]; then
  echo "  ├─ Merging 05-technologie/ -> 05_technologie_tesla/"
  # Check if examples/ exists in target
  if [ -d "05-technologie/examples" ] && [ ! -d "05_technologie_tesla/examples" ]; then
    cp -r 05-technologie/examples 05_technologie_tesla/ 2>/dev/null || true
  fi
  # Merge README if different
  if [ -f "05-technologie/README.md" ]; then
    if [ -f "05_technologie_tesla/README.md" ]; then
      echo "  ├─ ⚠️  Both READMEs exist, archiving old one"
      cp 05-technologie/README.md 99_unsortiert/archiv/05-technologie-README.md
    else
      cp 05-technologie/README.md 05_technologie_tesla/
    fi
  fi
  mv 05-technologie 99_unsortiert/archiv/05-technologie-OLD
  echo "  └─ ✅ Archived to 99_unsortiert/archiv/05-technologie-OLD"
else
  echo "  └─ ⏭️  05-technologie/ not found, skipping"
fi

# 2.3 Merge new/ -> 99_unsortiert/new/
if [ -d "new" ]; then
  echo "  ├─ Merging new/ -> 99_unsortiert/new/"
  mkdir -p 99_unsortiert/new
  cp -r new/* 99_unsortiert/new/ 2>/dev/null || true
  rm -rf new
  echo "  └─ ✅ Merged and removed new/"
else
  echo "  └─ ⏭️  new/ not found, skipping"
fi

# 2.4 Merge TODO_COPILOT_INTEGRATION.md -> TODO.md
if [ -f "TODO_COPILOT_INTEGRATION.md" ]; then
  echo "  ├─ Merging TODO_COPILOT_INTEGRATION.md -> TODO.md"
  echo "" >> TODO.md
  echo "## Copilot Integration (merged from TODO_COPILOT_INTEGRATION.md)" >> TODO.md
  echo "" >> TODO.md
  cat TODO_COPILOT_INTEGRATION.md >> TODO.md
  mv TODO_COPILOT_INTEGRATION.md 99_unsortiert/archiv/
  echo "  └─ ✅ Merged and archived"
else
  echo "  └─ ⏭️  TODO_COPILOT_INTEGRATION.md not found, skipping"
fi

echo "✅ PHASE 2 completed!"

# ============================================
# PHASE 3: MOVE FILES
# ============================================

echo ""
echo "📦 PHASE 3: Moving scattered files..."

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

echo ""
echo "🔄 PHASE 4: Renaming folders for consistency..."

# 4.1 Rename 08-experimente-validierung/ -> 08_experimente_validierung/
if [ -d "08-experimente-validierung" ]; then
  echo "  ├─ Renaming 08-experimente-validierung/ -> 08_experimente_validierung/"
  mv 08-experimente-validierung 08_experimente_validierung
  echo "  └─ ✅ Renamed"
else
  echo "  └─ ⏭️  08-experimente-validierung/ not found, skipping"
fi

# 4.2 Rename 99_noch_zu_bearbeiten/ -> 99_unsortiert/
if [ -d "99_noch_zu_bearbeiten" ]; then
  echo "  ├─ Merging 99_noch_zu_bearbeiten/ -> 99_unsortiert/"
  # Merge contents (archiv/ already exists in 99_unsortiert/)
  for item in 99_noch_zu_bearbeiten/*; do
    if [ -e "$item" ]; then
      itemname=$(basename "$item")
      if [ "$itemname" != "archiv" ]; then
        cp -r "$item" 99_unsortiert/ 2>/dev/null || true
      fi
    fi
  done
  rm -rf 99_noch_zu_bearbeiten
  echo "  └─ ✅ Merged and renamed"
else
  echo "  └─ ⏭️  99_noch_zu_bearbeiten/ not found, skipping"
fi

echo "✅ PHASE 4 completed!"

echo ""
echo "✅ ✅ ✅ ALL PHASES COMPLETED! ✅ ✅ ✅"
echo ""
echo "📝 Next steps:"
echo "  1. Review changes: git status"
echo "  2. Stage changes: git add -A"
echo "  3. Commit: git commit -m 'Phase 2-4: Cleanup completed'"
echo "  4. Push: git push origin cleanup/structure-audit-2025-12-08"
echo ""
