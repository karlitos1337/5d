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

# Disable WHO API calls with clear TODO
echo "  🔧 Disabling broken WHO API..."
cat > 5d_research_scraper_patch.py << 'PYEOF'
# ADD THIS METHOD TO ResearchScraper class:

def fetch_who_mental_health_data(self, countries=None):
    """
    Fetch mental health indicators from WHO Global Health Observatory.
    
    ⚠️ CURRENTLY DISABLED: WHO API returns 400 errors
    TODO: Migrate to new WHO API endpoint or find alternative source
    See: https://github.com/karlitos1337/5d/issues/XXX
    
    Args:
        countries: List of ISO3 country codes
    Returns:
        dict: Empty dict until fixed
    """
    print("  ⚠️  WHO API currently disabled (400 errors)")
    print("  📌 TODO: Migrate to new endpoint")
    return {}
PYEOF

echo "✅ Cleanup complete!"
echo ""
echo "Next steps:"
echo "  1. Review changes with: git status"
echo "  2. Commit: git commit -m 'Phase 1: Remove redundancies and disable broken WHO API'"
echo "  3. Push: git push origin cleanup/remove-redundancies"
