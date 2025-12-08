#!/bin/bash
echo "🔧 Fixing Streamlit import errors..."

# Fix Projections.py - Remove failed import, function already exists in file
sed -i '659s/.*/        # from utils.map_helpers import create_regional_adoption_map, render_minimap  # Function defined above/' pages/8_📈_Projections.py

# Fix Projects.py - Remove failed import, function already exists in file  
sed -i '541s/.*/        # from utils.map_helpers import create_alternative_schools_map, render_minimap  # Function defined above/' pages/2_🚀_Projects.py

echo "✅ Fixed both files - commented out duplicate imports"
