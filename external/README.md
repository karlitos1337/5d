# External Resources

**Last Updated:** 2025-12-03  
**Purpose:** Zentrale Verwaltung externer Repositories und Archive

---

## 📂 Verzeichnisstruktur

### `sources/` - Externe Repositories (25 Repos, ~280 MB)

**Awesome Lists (12):**
- `awesome-ai-web-search-main/` (104K) - AI-powered search tools
- `awesome-artificial-intelligence-master/` (60K) - AI resources
- `awesome-datascience-live/` (380K) - Data science tools
- `awesome-educational-games-master/` (24K) - Educational games
- `awesome-electronics-master/` (208K) - Electronics projects
- `awesome-free-apps-main/` (500K) - Free applications
- `awesome-mecheng-master/` (596K) - Mechanical engineering
- `awesome-piracy-main/` (172K) - Piracy resources (research only)
- `awesome-research-master/` (64K) - Academic research tools
- `Awesome-Browser-Extensions-for-OSINT-main/` (64K) - OSINT extensions
- `Awesome-Gamedev-main/` (8.1M) - Game development resources

**Educational Resources (4):**
- `books-master/` (92K) - Free books collection
- `free-programming-books-main/` (2.8M) - 8,000+ free programming books
- `Free-Certifications-main/` (76K) - Free certifications list
- `Free-Courses-For-Everyone-master/` (64K) - Free online courses

**Technical Resources (6):**
- `computer-science-master/` (784K) - CS curriculum
- `data-engineer-handbook-main/` (233M) - Data engineering guide
- `data-science-master/` (648K) - Data science resources
- `git-cheat-sheet-main/` (440K) - Git cheat sheets
- `javascript-algorithms-master/` (13M) - JS algorithms & data structures
- `gpt4free-main/` (3.7M) - Free GPT-4 implementations

**Tools & Utilities (3):**
- `complexity-nxt/` (12M) - Complexity analysis tools
- `sitedorks-master/` (464K) - Google dork searches
- `Ebook-Translator-Calibre-Plugin-master/` (1.6M) - Calibre translation plugin
- `FMHY-SafeGuard-main/` (1.2M) - FMHY safety guide

### `archives/` - Alte Versionen & Temp-Dateien

**old_versions/:**
- `RUN_ALL (1).sh` - Duplicate startup script
- `5d_dashboard_backup.py` - Dashboard backup
- `5d_dashboard_v1.py` - Dashboard v1
- `SESSION_SUMMARY_2025-12-02.md` - Old session summary
- `streamlit_report.txt` - Old streamlit report

**Temp/Debug:**
- `64f52163-*` - Temp UUID file
- `dc8da8c2-*` - Temp UUID file
- `bookmarks-tor.html` - Tor bookmarks
- `calibre-64bit-8.15.0.msi` - Calibre installer (Windows)

---

## 🔗 Integration in 5D-Framework

**Alle externen Repositories sind bereits dokumentiert in:**

1. **`99_noch_zu_bearbeiten/externe_ressourcen_analyse.md`** (38 URLs analysiert)
2. **`docs/EXTERNAL_RESOURCES_INTEGRATION.md`** (Sprint 1-3 Roadmap)
3. **Dedizierte Dokumentationsdateien:**
   - `01_bildung_education/free_learning_consolidated.md` (Free Learning List)
   - `01_bildung_education/educational_commons.md` (OpenStax, MIT OCW, Coursera)
   - `05_technologie_tesla/ai_model_tracking.md` (AI Models)
   - `05_technologie_tesla/security_fundamentals.md` (HackTricks, OSINT)
   - `07_daten_analysen/academic_data_sources.md` (Academic Torrents)
   - `02_neurobiologie_psychologie/prompt_engineering_tools.md` (SD Prompts)

**BibTeX-Einträge:** Alle 25 Repositories haben BibTeX-Einträge in `07_daten_analysen/5d-relevant-sources.bib` (Batch 9-11)

---

## 📊 Statistik

- **Anzahl Repositories:** 25
- **Gesamtgröße:** ~280 MB
- **Größte Repos:** 
  - data-engineer-handbook-main (233M)
  - javascript-algorithms-master (13M)
  - complexity-nxt (12M)
  - Awesome-Gamedev-main (8.1M)
  - gpt4free-main (3.7M)

---

## ⚠️ Hinweise

**Lizenz-Compliance:**
- Alle Repositories sind Open Source (MIT, Apache 2.0, CC, etc.)
- `awesome-piracy-main/`: Nur für Forschungszwecke dokumentiert (nicht kommerziell nutzen)
- `gpt4free-main/`: API-Reverse-Engineering (rechtliche Grauzone, nur dokumentarisch)

**Nicht in Git-Tracking:**
- Alle externen Repos sind in `.gitignore` eingetragen
- Nur Dokumentation (Markdown-Dateien) wird versioniert
- Repositories werden bei Bedarf neu geklont

---

## 🔄 Update-Workflow

**Externe Repos aktualisieren:**
```bash
cd /workspaces/5d/external/sources
for dir in */; do
  cd "$dir"
  git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
  cd ..
done
```

**Neue Repos hinzufügen:**
1. Klone Repo nach `external/sources/`
2. Dokumentiere in entsprechendem `0X_*/` Ordner
3. Erstelle BibTeX-Eintrag in `5d-relevant-sources.bib`
4. Update `externe_ressourcen_analyse.md`

---

**Siehe auch:**
- [TODO.md](../TODO.md) - Sprint 1-3 External Resources (✅ 26/26 komplett)
- [LITERATUR_INDEX.md](../07_daten_analysen/LITERATUR_INDEX.md) - BibTeX Batch 9-11
- [EXTERNAL_RESOURCES_INTEGRATION.md](../docs/EXTERNAL_RESOURCES_INTEGRATION.md) - Roadmap
