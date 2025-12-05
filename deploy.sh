git #!/bin/bash
# 5D System Monitor - GitHub Deployment Script

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         5D GLOBAL SYSTEM MONITOR - GITHUB DEPLOYMENT           ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check: Sind wir im 5d Repo?
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Fehler: Nicht im Git-Repository!${NC}"
    echo "   Bitte in dein 5d-Repo gehen:"
    echo "   cd ~/path/to/5d"
    exit 1
fi

echo -e "${GREEN}✅ Im Git-Repository${NC}"

# 1. Verzeichnisse erstellen
echo ""
echo -e "${YELLOW}📁 Erstelle Verzeichnisstruktur...${NC}"
mkdir -p monitors/logs
mkdir -p config
mkdir -p data/archive
mkdir -p scripts
mkdir -p .github/workflows
echo -e "${GREEN}✅ Verzeichnisse erstellt${NC}"

# 2. .gitignore aktualisieren
echo ""
echo -e "${YELLOW}🔐 Aktualisiere .gitignore...${NC}"
cat >> .gitignore << 'EOF'

# 5D Monitoring
config/google-credentials.json
monitors/logs/*.log
data/archive/
.env
.env.local
EOF
echo -e "${GREEN}✅ .gitignore aktualisiert${NC}"

# 3. Status anzeigen
echo ""
echo -e "${YELLOW}📊 Git Status:${NC}"
git status --short | head -20

# 4. Alle Änderungen hinzufügen
echo ""
echo -e "${YELLOW}➕ Staging all changes...${NC}"
git add -A
echo -e "${GREEN}✅ Alle Dateien staged${NC}"

# 5. Commit
echo ""
echo -e "${YELLOW}💾 Committing...${NC}"
COMMIT_MSG="🚀 Deploy 5D Global System Monitor
- 25+ real-time system monitors
- 6-hour polling via GitHub Actions
- Auto-export to Google Sheets (separate sheets per monitor)
- War Deaths tracking (ACLED real-time + UCDP verified)
- Chronological CSV logging with severity classification
- Complete documentation & deployment guide"

git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✅ Committed${NC}"

# 6. Push
echo ""
echo -e "${YELLOW}📤 Pushing to GitHub...${NC}"
git push origin main
echo -e "${GREEN}✅ Pushed!${NC}"

# 7. Status summary
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo -e "${YELLOW}🔧 NÄCHSTE SCHRITTE:${NC}"
echo ""
echo "1️⃣ Google Drive Setup:"
echo "   • Gehe zu: https://console.cloud.google.com/"
echo "   • Erstelle Projekt: '5d-monitors'"
echo "   • Aktiviere: Google Sheets API + Google Drive API"
echo "   • Service Account → JSON Key"
echo ""
echo "2️⃣ GitHub Secret:"
echo "   • Repo → Settings → Secrets → New Secret"
echo "   • Name: GDRIVE_CREDENTIALS"
echo "   • Value: (paste Service Account JSON)"
echo ""
echo "3️⃣ Google Drive Folder:"
echo "   • Erstelle: 'shared' 5d-Monitoring' Folder"
echo "   • Teile mit: 5d-monitor-bot@PROJECT-ID.iam.gserviceaccount.com"
echo ""
echo "4️⃣ GitHub Actions:"
echo "   • Repo → Actions tab"
echo "   • Sollte '5D System Monitor' Workflow sehen"
echo "   • Nächster Run: in ~6 Stunden (oder manuell triggern)"
echo ""
echo -e "${GREEN}Dein globales Nervensystem ist online! 🌍${NC}"
