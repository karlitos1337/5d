#!/bin/bash
# 5D Dashboard Debug Script
# Usage: ./debug_dashboard.sh [page_number]
# Example: ./debug_dashboard.sh 2  (tests Page 2 - Projects)

set -e

PAGE=${1:-0}  # Default to page 0 (main dashboard)

echo "🔍 5D Dashboard Debug Tool"
echo "=========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check 1: Python version
echo "1️⃣ Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
    echo -e "${GREEN}✅ Python $PYTHON_VERSION (OK)${NC}"
else
    echo -e "${RED}❌ Python $PYTHON_VERSION (need 3.10+)${NC}"
    exit 1
fi

# Check 2: Required packages
echo ""
echo "2️⃣ Checking dependencies..."
REQUIRED_PACKAGES=(
    "streamlit"
    "pandas"
    "plotly"
    "folium"
    "streamlit_folium"
)

MISSING=()
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if python -c "import $pkg" 2>/dev/null; then
        echo -e "${GREEN}✅ $pkg${NC}"
    else
        echo -e "${RED}❌ $pkg (missing)${NC}"
        MISSING+=("$pkg")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️ Missing packages. Install with:${NC}"
    echo "pip install ${MISSING[@]}"
    read -p "Install now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install "${MISSING[@]}"
    else
        exit 1
    fi
fi

# Check 3: JSON files
echo ""
echo "3️⃣ Checking JSON data files..."
JSON_FILES=(
    "5d_solutions.json"
    "5d_research_data.json"
    "5d_github_data.json"
)

MISSING_JSON=()
for file in "${JSON_FILES[@]}"; do
    if [ -f "$file" ]; then
        # Validate JSON syntax
        if python -c "import json; json.load(open('$file'))" 2>/dev/null; then
            SIZE=$(du -h "$file" | cut -f1)
            echo -e "${GREEN}✅ $file ($SIZE)${NC}"
        else
            echo -e "${RED}❌ $file (invalid JSON)${NC}"
            MISSING_JSON+=("$file")
        fi
    else
        echo -e "${YELLOW}⚠️ $file (not found)${NC}"
        MISSING_JSON+=("$file")
    fi
done

if [ ${#MISSING_JSON[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️ Missing or invalid JSON files. Generate with:${NC}"
    echo "./start.sh"
    echo ""
    echo "Or individually:"
    echo "python 5d_extractor.py"
    echo "python 5d_research_scraper.py"
    echo "python 5d_github_api.py"
    
    read -p "Run ./start.sh now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./start.sh
    else
        echo "Continuing without data generation..."
    fi
fi

# Check 4: Map data (for page 7)
echo ""
echo "4️⃣ Checking 5D-Map data files..."
MAP_FILES=(
    "web/5d-map/data/baseline.json"
    "web/5d-map/data/schools.json"
)

for file in "${MAP_FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(du -h "$file" | cut -f1)
        echo -e "${GREEN}✅ $file ($SIZE)${NC}"
    else
        echo -e "${YELLOW}⚠️ $file (not found)${NC}"
    fi
done

# Check 5: Page files
echo ""
echo "5️⃣ Checking dashboard pages..."
if [ "$PAGE" -eq 0 ]; then
    PAGE_FILE="5d_dashboard.py"
else
    # Find page file by number
    PAGE_FILE=$(find pages -name "${PAGE}_*.py" | head -1)
    
    if [ -z "$PAGE_FILE" ]; then
        echo -e "${RED}❌ Page $PAGE not found${NC}"
        echo ""
        echo "Available pages:"
        ls -1 pages/*.py | nl -w1 -s'. '
        exit 1
    fi
fi

echo "Testing: $PAGE_FILE"

# Syntax check
if python -m py_compile "$PAGE_FILE" 2>/dev/null; then
    echo -e "${GREEN}✅ Syntax OK${NC}"
else
    echo -e "${RED}❌ Syntax errors:${NC}"
    python -m py_compile "$PAGE_FILE"
    exit 1
fi

# Check 6: Port availability
echo ""
echo "6️⃣ Checking port 8501..."
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ Port 8501 already in use${NC}"
    PID=$(lsof -Pi :8501 -sTCP:LISTEN -t)
    echo "Process: $(ps -p $PID -o comm=)"
    
    read -p "Kill existing process and restart? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill $PID
        sleep 2
    else
        echo "Using alternative port 8502..."
        PORT=8502
    fi
else
    echo -e "${GREEN}✅ Port 8501 available${NC}"
    PORT=8501
fi

# Summary
echo ""
echo "=========================="
echo "🎯 Debug Summary"
echo "=========================="
echo "Python: $PYTHON_VERSION"
echo "Page: $PAGE_FILE"
echo "Port: $PORT"
echo ""

# Run the dashboard
echo "🚀 Starting dashboard..."
echo "Press Ctrl+C to stop"
echo ""

LOG_FILE="logs/debug_page_${PAGE}.log"
mkdir -p logs

echo "Logging to: $LOG_FILE"
echo ""

# Start streamlit with logging
streamlit run "$PAGE_FILE" \
    --server.port="$PORT" \
    --server.headless=true \
    --logger.level=debug \
    2>&1 | tee "$LOG_FILE"
