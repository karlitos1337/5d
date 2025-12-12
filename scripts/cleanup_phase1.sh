#!/bin/bash
set -e

echo "🧹 Phase 1: Cleanup & Remove Redundancies"

# Remove duplicate backup
echo "  ❌ Removing 5d_research_scraper.py.backup..."
git rm 5d_research_scraper.py.backup

# Remove empty file
echo "  ❌ Removing empty '5d' file..."
rm -f 5d
git add -u

# Consolidate requirements
echo "  📦 Consolidating dependencies..."
cat requirements_extended.txt >> requirements.txt
git rm requirements_extended.txt

# Remove Node config (not a Node project)
echo "  🗑️  Removing package.json..."
git rm package.json

# Create backup of research scraper before modification
cp 5d_research_scraper.py 5d_research_scraper.py.temp

echo "✅ Cleanup complete!"
echo ""
echo "Next steps:"
echo "  1. Review changes with: git status"
echo "  2. Commit: git commit -m 'Phase 1: Remove redundancies'"
echo "  3. Push: git push origin cleanup/remove-redundancies"
