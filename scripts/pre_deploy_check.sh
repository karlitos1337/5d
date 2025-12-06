#!/usr/bin/env bash
# Pre-deployment validation for 5D-Map GitHub Pages
# Checks: index.html, data files, assets, relative paths

set -e

echo "🔍 Pre-Deployment Validation for 5D-Map"
echo "========================================="
echo ""

MAP_DIR="docs/5d-map"
ERRORS=0

# Check 1: Essential files exist
echo "✓ Checking essential files..."
REQUIRED_FILES=(
    "$MAP_DIR/index.html"
    "$MAP_DIR/app.js"
    "$MAP_DIR/styles.css"
    "$MAP_DIR/manifest.json"
    "$MAP_DIR/data/baseline.json"
    "$MAP_DIR/data/alternative_schools.json"
    "$MAP_DIR/data/scenarios.json"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "  ❌ Missing: $file"
        ERRORS=$((ERRORS + 1))
    else
        echo "  ✅ Found: $file"
    fi
done

echo ""

# Check 2: Validate JSON files
echo "✓ Validating JSON syntax..."
JSON_FILES=(
    "$MAP_DIR/data/baseline.json"
    "$MAP_DIR/data/alternative_schools.json"
    "$MAP_DIR/data/scenarios.json"
    "$MAP_DIR/manifest.json"
)

for json_file in "${JSON_FILES[@]}"; do
    if [ -f "$json_file" ]; then
        if python3 -m json.tool "$json_file" > /dev/null 2>&1; then
            echo "  ✅ Valid JSON: $json_file"
        else
            echo "  ❌ Invalid JSON: $json_file"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

echo ""

# Check 3: Relative paths in index.html (no leading /)
echo "✓ Checking relative paths in index.html..."
if grep -q 'href="/' "$MAP_DIR/index.html" 2>/dev/null; then
    echo "  ⚠️  Warning: Absolute paths found (href=\"/...\") - may break on GitHub Pages"
    grep 'href="/' "$MAP_DIR/index.html" | head -3
else
    echo "  ✅ All paths are relative"
fi

if grep -q 'src="/' "$MAP_DIR/index.html" 2>/dev/null; then
    echo "  ⚠️  Warning: Absolute paths found (src=\"/...\") - may break on GitHub Pages"
    grep 'src="/' "$MAP_DIR/index.html" | head -3
else
    echo "  ✅ All script sources are relative"
fi

echo ""

# Check 4: File sizes (warn if >5MB)
echo "✓ Checking file sizes..."
LARGE_FILES=$(find "$MAP_DIR" -type f -size +5M 2>/dev/null)
if [ -n "$LARGE_FILES" ]; then
    echo "  ⚠️  Warning: Large files detected (>5MB):"
    echo "$LARGE_FILES"
else
    echo "  ✅ All files <5MB"
fi

echo ""

# Check 5: Leaflet library
echo "✓ Checking Leaflet integration..."
if grep -q "leaflet" "$MAP_DIR/index.html" 2>/dev/null; then
    echo "  ✅ Leaflet found in index.html"
else
    echo "  ❌ Leaflet not found in index.html"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# Summary
echo "========================================="
if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed! Ready for deployment."
    echo ""
    echo "Deploy with:"
    echo "  git add docs/5d-map/"
    echo "  git commit -m 'Deploy 5D-Map to GitHub Pages'"
    echo "  git push"
    echo ""
    echo "Monitor: https://github.com/karlitos1337/5d/actions"
    exit 0
else
    echo "❌ $ERRORS error(s) found. Please fix before deploying."
    exit 1
fi
