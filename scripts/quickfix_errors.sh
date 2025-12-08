#!/bin/bash
<<<<<<< HEAD
# Quick Fix Script for 5d Repository Errors
# Fixes: WHO API errors, KeyError in scraper, pytest cache issues

set -e

=======
# Quick Fix Script

set -e
>>>>>>> e3c6597 (Fix all critical bugs - Streamlit working)
echo "🔧 Starting Quick Fix..."

# 1. Clean pytest cache
echo "🧹 Cleaning pytest cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true
echo "✅ Pytest cache cleaned"

<<<<<<< HEAD
# 2. Fix KeyError in 5d_research_scraper.py
echo "🔧 Fixing KeyError in 5d_research_scraper.py..."
if [ -f "5d_research_scraper.py" ]; then
    # Backup original
    cp 5d_research_scraper.py 5d_research_scraper.py.backup
    
    # Fix line 391
    sed -i 's/len(data\["arxiv"\])/len(data.get("arxiv", []))/g' 5d_research_scraper.py
    sed -i 's/len(data\["pubmed"\])/len(data.get("pubmed", []))/g' 5d_research_scraper.py
    
    echo "✅ KeyError fixed (backup: 5d_research_scraper.py.backup)"
=======
# 2. Fix KeyError
echo "🔧 Fixing KeyError in 5d_research_scraper.py..."
if [ -f "5d_research_scraper.py" ]; then
    cp 5d_research_scraper.py 5d_research_scraper.py.backup
    sed -i 's/len(data\["arxiv"\])/len(data.get("arxiv", []))/g' 5d_research_scraper.py
    sed -i 's/len(data\["pubmed"\])/len(data.get("pubmed", []))/g' 5d_research_scraper.py
    echo "✅ KeyError fixed"
>>>>>>> e3c6597 (Fix all critical bugs - Streamlit working)
else
    echo "⚠️  5d_research_scraper.py not found"
fi

<<<<<<< HEAD
# 3. Create WHO API skip patch
echo "🔧 Creating WHO API skip patch..."
cat > scripts/patch_who_api.py << 'EOF'
#!/usr/bin/env python3
"""Patch WHO API calls to skip temporarily"""
import re

with open('5d_research_scraper.py', 'r') as f:
    content = f.read()

# Comment out WHO API calls
content = re.sub(
    r'(def fetch_who_data.*?return who_data)',
    r'\1  # TEMPORARILY DISABLED DUE TO API ERRORS\n    return {}',
    content,
    flags=re.DOTALL
)

with open('5d_research_scraper.py', 'w') as f:
    f.write(content)

print("✅ WHO API calls disabled")
EOF

chmod +x scripts/patch_who_api.py
python3 scripts/patch_who_api.py || echo "⚠️  WHO patch failed (manual fix needed)"

# 4. Summary
echo ""
echo "✅ Quick Fix Complete!"
echo ""
echo "Fixed:"
echo "  ✅ Cleaned __pycache__ and .pyc files"
echo "  ✅ Fixed KeyError in research scraper"
echo "  ✅ Disabled WHO API calls temporarily"
echo ""
echo "Next steps:"
echo "  1. Run: make start"
echo "  2. Run: make test"
echo "  3. Fix WHO API properly later"
=======
echo ""
echo "✅ Quick Fix Complete!"
echo "Run: make start"
>>>>>>> e3c6597 (Fix all critical bugs - Streamlit working)
