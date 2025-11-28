#!/bin/bash
# 5D Complete Workflow Runner

echo "🚀 5D COMPLETE ANALYSIS SUITE"
echo "=============================="

# 1. Base Extractor
echo ""
echo "📊 Step 1: Extracting 5D Solutions..."
python 5d_extractor.py

# 2. Research Scraping
echo ""
echo "🔍 Step 2: Scraping Research Papers..."
python 5d_research_scraper.py

# 3. GitHub API
echo ""
echo "💻 Step 3: GitHub API Exploration..."
python 5d_github_api.py

# 4. Launch Dashboard
echo ""
echo "📈 Step 4: Launching Dashboard..."
echo "👉 Opening http://localhost:8501 in your browser..."
streamlit run 5d_dashboard.py

# Optional: External Merge (nur wenn Submodules vorhanden)
# echo ""
# echo "🔀 Optional: Merging external 5D solutions..."
# python merge_external_solutions.py

# Optional: Resonance→IMP Mapping (nicht-invasiv; erzeugt 5d_solutions_adjusted.json)
# python apply_resonance_mapping.py

# Optional: Weitere Streamlit-Apps (separat starten)
# streamlit run gol_streamlit.py
# streamlit run zwi_streamlit.py

# Note: Discord Bot requires DISCORD_TOKEN
# python 5d_discord_bot.py
