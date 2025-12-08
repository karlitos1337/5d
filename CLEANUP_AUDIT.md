# Repository Cleanup Audit

**Created:** 2025-12-08  
**Status:** 🚨 REVIEW NEEDED (nichts wird automatisch gelöscht)  
**Purpose:** Duplikate mergen, Redundanzen auflisten, Lösch-Kandidaten sammeln

---

## 📊 ZUSAMMENFASSUNG

| **Kategorie** | **Gefunden** | **Aktion** |
|--------------|-------------|------------|
| **Doppelte Ordner** | 3 Paare | → Merge-Strategie unten |
| **Timestamp-Files** | 12 Dateien | → Verschieben nach `outputs/` |
| **Doppelte TODOs** | 2 obsolete | → Lösch-Kandidaten |
| **Data-Files (Root)** | 5 Dateien | → Verschieben nach `data/` |
| **Redundante Ordner** | 2 (`new/`, `99_noch_zu_bearbeiten/`) | → Merge + Umbenennung |

---

## ⚠️ 1. DOPPELTE ORDNER (Merge-Strategie)

### **1.1 Philosophie-Ordner**

**DUPLIKAT GEFUNDEN:**
```
03-philosophie/                    ← ALT (Dash-Naming)
└─ epistemologie/

vs.

03_philosophie_epistemologie/      ← NEU (Underscore-Naming)
└─ 158wegederzwanglosigkeit.md
```

**MERGE-STRATEGIE:**
- ✅ **Behalte:** `03_philosophie_epistemologie/` (korrekte Naming-Convention)
- 🔄 **Merge:** Inhalte aus `03-philosophie/epistemologie/` in `03_philosophie_epistemologie/`
- 📦 **Archiviere:** `03-philosophie/` nach `99_unsortiert/archiv/03-philosophie-OLD/`

**KONFLIKT-CHECK:**
- ❓ **TODO:** Prüfe, ob `03-philosophie/epistemologie/` Files hat, die NICHT in `03_philosophie_epistemologie/` sind

---

### **1.2 Technologie-Ordner**

**DUPLIKAT GEFUNDEN:**
```
05-technologie/                    ← ALT (Dash-Naming)
├─ README.md
└─ examples/

vs.

05_technologie_tesla/              ← NEU (Underscore-Naming)
└─ ...
```

**MERGE-STRATEGIE:**
- ✅ **Behalte:** `05_technologie_tesla/` (korrekte Convention + spezifischer)
- 🔄 **Merge:** 
  - `05-technologie/README.md` → Prüfe, ob Inhalt in `05_technologie_tesla/README.md` fehlt
  - `05-technologie/examples/` → Verschiebe nach `05_technologie_tesla/examples/`
- 📦 **Archiviere:** `05-technologie/` nach `99_unsortiert/archiv/05-technologie-OLD/`

**KONFLIKT-CHECK:**
- ❓ **TODO:** Vergleiche `05-technologie/README.md` mit `05_technologie_tesla/README.md`

---

### **1.3 Experimente-Ordner**

**KEIN DUPLIKAT, aber INKONSISTENZ:**
```
08-experimente-validierung/        ← DASH-Naming (inkonsistent!)
```

**LÖSUNG:**
- 🔄 **Umbenennen:** `08-experimente-validierung/` → `08_experimente_validierung/`
- ✅ **Konsistenz:** Alle Ordner verwenden jetzt `XX_name_name/` Format

---

## 📅 2. TIMESTAMP-FILES (Root-Chaos)

**GEFUNDEN (12 Dateien):**
```
example_responses_20251205_041908.csv
example_responses_20251205_043337.csv
example_responses_20251205_052121.csv
questionnaire_20251205_041908.json
questionnaire_20251205_043337.json
questionnaire_20251205_052121.json
validation_report_20251205_041908.json
validation_report_20251205_043337.json
validation_report_20251205_052121.json
validation_results_20251205_041908.png
validation_results_20251205_043337.png
validation_results_20251205_052121.png
```

**STRATEGIE:**

### **Option A: Verschieben + Archivieren**
```
→ outputs/surveys/example_responses/
   ├─ 20251205_041908.csv
   ├─ 20251205_043337.csv
   └─ 20251205_052121.csv

→ outputs/surveys/questionnaires/
   ├─ 20251205_041908.json
   ├─ 20251205_043337.json
   └─ 20251205_052121.json

→ outputs/validation/
   ├─ reports/
   │  ├─ 20251205_041908.json
   │  ├─ 20251205_043337.json
   │  └─ 20251205_052121.json
   └─ plots/
      ├─ 20251205_041908.png
      ├─ 20251205_043337.png
      └─ 20251205_052121.png
```

### **Option B: Löschen (wenn obsolet)**
- ❓ **Frage:** Sind diese Files **obsolet** (nur Test-Runs)?
- ✅ **Falls JA:** Behalte nur **neuestes** (`20251205_052121.*`), lösche ältere
- ❌ **Falls NEIN:** Behalte alle, verschiebe nach `outputs/`

**EMPFEHLUNG:** Option A (Verschieben), dann später entscheiden ob Löschen

---

## 📋 3. DOPPELTE TODO-FILES

**GEFUNDEN:**
```
TODO.md                              ← ✅ AKTIV (Infrastructure, 87% done)
TODO_MULTIPAGE.md                    ← ✅ AKTIV (UI, 100% done)
TODO_RESEARCH.md                     ← ✅ AKTIV (Research, 85+ tasks)
TODO_COPILOT_INTEGRATION.md          ← ⚠️ MINI (1KB, 9 tasks)
MEGA_TODO_CONSOLIDATED.md            ← ❌ OBSOLET? (13KB, unpriorisiert)
MEGA_TODO_CONSOLIDATED_PRIORITIZED.md ← ❌ OBSOLET? (13KB, priorisiert)
```

**STRATEGIE:**

### **3.1 MEGA_TODO Files**

**HYPOTHESE:** Diese sind **Vorläufer** von `TODO.md`, `TODO_MULTIPAGE.md`, `TODO_RESEARCH.md`

**AKTION:**
1. 🔍 **Vergleiche:** Sind Tasks aus `MEGA_TODO_CONSOLIDATED_PRIORITIZED.md` in den 3 aktiven TODOs?
2. ✅ **Falls JA:** Lösch-Kandidaten (oder archivieren)
3. ❌ **Falls NEIN:** Merge fehlende Tasks in passende TODO-Datei

**VORSCHLAG:** Archiviere nach `99_unsortiert/archiv/MEGA_TODO_*.md`

### **3.2 TODO_COPILOT_INTEGRATION.md**

**INHALT (1KB, 9 Tasks):**
- Wahrscheinlich spezifisch für Copilot-Integration
- Nicht in `TODO.md` dupliziert (mutmaßlich)

**AKTION:**
- 🔄 **Merge:** Tasks in `TODO.md` unter neuer Sektion "Copilot Integration"
- 📦 **Dann:** Lösch-Kandidat (oder archivieren)

---

## 📊 4. DATA-FILES IM ROOT

**GEFUNDEN:**
```
5d_github_data.json          ← 41KB (GitHub API data)
5d_research_data.json        ← 17KB (Research data)
5d_solutions.json            ← 26KB (Solutions data)
model_comparison_data.csv    ← 144KB (Model comparison)
model_comparison_results.png ← 1.9MB (Visualization)
```

**STRATEGIE:**

### **Verschieben nach `data/`**
```
data/
├─ github/
│  └─ 5d_github_data.json
├─ research/
│  └─ 5d_research_data.json
├─ solutions/
│  └─ 5d_solutions.json
└─ experiments/
   ├─ model_comparison_data.csv
   └─ model_comparison_results.png
```

**ODER:** Falls zu `outputs/` gehören (generierte Daten):
```
outputs/
├─ api_dumps/
│  ├─ 5d_github_data.json
│  ├─ 5d_research_data.json
│  └─ 5d_solutions.json
└─ model_comparison/
   ├─ data.csv
   └─ results.png
```

**EMPFEHLUNG:** 
- `5d_*_data.json` → `data/` (source data)
- `model_comparison_*` → `outputs/` (generated results)

---

## 📦 5. REDUNDANTE ORDNER

**GEFUNDEN:**
```
99_noch_zu_bearbeiten/       ← "noch zu bearbeiten" (German)
new/                         ← "new" (English, generic)
```

**STRATEGIE:**

### **5.1 Merge `new/` → `99_noch_zu_bearbeiten/`**
- 🔄 Verschiebe alles aus `new/` nach `99_noch_zu_bearbeiten/new/`
- 🗑️ Lösche leeren `new/` Ordner

### **5.2 Umbenennung für Konsistenz**
- 🔄 `99_noch_zu_bearbeiten/` → `99_unsortiert/`
- ✅ **Grund:** README.md sagt "99_unsortiert/" (inkonsistent mit aktuellem Namen)

**FINALE STRUKTUR:**
```
99_unsortiert/
├─ new/              ← Inhalte aus altem `new/`
├─ archiv/           ← Alte Ordner (03-philosophie-OLD, etc.)
└─ ...               ← Bisherige Inhalte aus `99_noch_zu_bearbeiten/`
```

---

## 🗑️ 6. LÖSCH-KANDIDATEN (Sammlung)

**KATEGORIE 1: Obsolete Files**
```
[ ] MEGA_TODO_CONSOLIDATED.md                 (13KB, ersetzt durch TODO.md)
[ ] MEGA_TODO_CONSOLIDATED_PRIORITIZED.md     (13KB, ersetzt durch TODO.md)
[ ] TODO_COPILOT_INTEGRATION.md               (1KB, merge in TODO.md)
```

**KATEGORIE 2: Alte Timestamp-Files (falls obsolet)**
```
[ ] example_responses_20251205_041908.csv     (älter als 052121)
[ ] example_responses_20251205_043337.csv     (älter als 052121)
[ ] questionnaire_20251205_041908.json        (älter als 052121)
[ ] questionnaire_20251205_043337.json        (älter als 052121)
[ ] validation_report_20251205_041908.json    (älter als 052121)
[ ] validation_report_20251205_043337.json    (älter als 052121)
[ ] validation_results_20251205_041908.png    (älter als 052121)
[ ] validation_results_20251205_043337.png    (älter als 052121)
```

**KATEGORIE 3: Doppelte Ordner (nach Merge)**
```
[ ] 03-philosophie/                           (nach Merge)
[ ] 05-technologie/                           (nach Merge)
[ ] new/                                      (nach Merge)
```

**STATUS:** ⚠️ **NICHT LÖSCHEN** bis manuelle Review abgeschlossen!

---

## ✅ 7. .gitignore UPDATE

**NEUE REGELN HINZUFÜGEN:**
```gitignore
# Timestamp-generated files
*_202[0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][0-9][0-9].*

# Model outputs (keep in outputs/ only)
model_comparison_*

# Validation results (keep in outputs/ only)
validation_results_*.png
validation_report_*.json

# Example data (keep in outputs/ only)
example_responses_*.csv
questionnaire_*.json
```

---

## 🛠️ 8. AKTIONSPLAN (Schritt-für-Schritt)

### **Phase 1: Vorbereitung (KEIN DELETE)**
1. ✅ Erstelle Branch `cleanup/structure-audit-2025-12-08`
2. ✅ Erstelle `99_unsortiert/archiv/` Ordner
3. ✅ Erstelle `outputs/surveys/`, `outputs/validation/` Ordner

### **Phase 2: Merge Duplikate**
4. 🔄 Merge `03-philosophie/epistemologie/` → `03_philosophie_epistemologie/`
5. 🔄 Merge `05-technologie/` → `05_technologie_tesla/`
6. 🔄 Merge `new/` → `99_unsortiert/new/`
7. 🔄 Merge `TODO_COPILOT_INTEGRATION.md` → `TODO.md`

### **Phase 3: Verschieben**
8. 📦 Verschiebe Timestamp-Files → `outputs/`
9. 📦 Verschiebe Data-Files → `data/` oder `outputs/`
10. 📦 Archiviere alte Ordner → `99_unsortiert/archiv/`

### **Phase 4: Umbenennung**
11. 🔄 `08-experimente-validierung/` → `08_experimente_validierung/`
12. 🔄 `99_noch_zu_bearbeiten/` → `99_unsortiert/`

### **Phase 5: Review & Delete**
13. ❓ **MANUAL REVIEW:** Prüfe archivierte Ordner
14. ❓ **MANUAL REVIEW:** Prüfe Lösch-Kandidaten (Sektion 6)
15. 🗑️ **Falls OK:** Lösche nach Freigabe

### **Phase 6: .gitignore**
16. ✅ Update `.gitignore` (Sektion 7)
17. ✅ Commit + Push Branch
18. ✅ Pull Request für Final Review

---

## 📊 9. VORHER/NACHHER (Visualisierung)

### **VORHER (Aktuell):**
```
03-philosophie/              ❌ Duplikat
03_philosophie_epistemologie/ ✅ Behalten
05-technologie/              ❌ Duplikat
05_technologie_tesla/        ✅ Behalten
08-experimente-validierung/  ⚠️ Inkonsistent (Dash)
99_noch_zu_bearbeiten/       ⚠️ Inkonsistent (Name)
new/                         ❌ Redundant

example_responses_*.csv      ❌ Root-Chaos (12 Files)
model_comparison_*           ❌ Root-Chaos (2 Files)
5d_*_data.json               ❌ Root-Chaos (3 Files)

MEGA_TODO_*.md               ❌ Obsolet (2 Files)
```

### **NACHHER (Geplant):**
```
03_philosophie_epistemologie/ ✅ Merged
05_technologie_tesla/        ✅ Merged
08_experimente_validierung/  ✅ Konsistent
99_unsortiert/               ✅ Konsistent
   ├─ new/
   └─ archiv/
      ├─ 03-philosophie-OLD/
      ├─ 05-technologie-OLD/
      └─ MEGA_TODO_*.md

data/
   ├─ github/5d_github_data.json
   ├─ research/5d_research_data.json
   └─ solutions/5d_solutions.json

outputs/
   ├─ surveys/
   │  ├─ example_responses/
   │  └─ questionnaires/
   ├─ validation/
   │  ├─ reports/
   │  └─ plots/
   └─ model_comparison/
      ├─ data.csv
      └─ results.png

TODO.md                      ✅ Merged (incl. Copilot)
TODO_MULTIPAGE.md            ✅ Behalten
TODO_RESEARCH.md             ✅ Behalten
```

---

## ❓ 10. OFFENE FRAGEN (Manual Review)

### **Frage 1: Timestamp-Files**
- ❓ Sind `example_responses_*.csv` und `questionnaire_*.json` nur **Test-Runs**?
- ❓ Falls JA: Nur neueste behalten (`*_052121.*`), Rest löschen?
- ❓ Falls NEIN: Alle behalten, aber in `outputs/` verschieben?

### **Frage 2: MEGA_TODO Files**
- ❓ Sind Tasks aus `MEGA_TODO_CONSOLIDATED_PRIORITIZED.md` **alle** in `TODO.md`, `TODO_MULTIPAGE.md`, `TODO_RESEARCH.md`?
- ❓ Falls JA: Löschen (oder archivieren)?
- ❓ Falls NEIN: Fehlende Tasks mergen?

### **Frage 3: Data vs. Outputs**
- ❓ Sind `5d_*_data.json` **source data** (statisch) oder **generated outputs** (dynamisch)?
- ❓ `data/` für statisch, `outputs/` für dynamisch?

### **Frage 4: 03-philosophie/ und 05-technologie/ Inhalte**
- ❓ Gibt es Files in `03-philosophie/epistemologie/`, die NICHT in `03_philosophie_epistemologie/` sind?
- ❓ Gibt es Files in `05-technologie/examples/`, die NICHT in `05_technologie_tesla/` sind?

---

## 📝 11. NÄCHSTE SCHRITTE

**JETZT:**
1. ✅ Review dieses Dokument
2. ❓ Beantworte offene Fragen (Sektion 10)
3. 👍 Freigabe für Phase 1-4 (Merge + Verschieben, KEIN Delete)

**DANN:**
4. 🔧 Ich erstelle Branch + führe Phase 1-4 aus
5. 📝 Du reviewst Diff im Pull Request
6. 👍 Falls OK: Merge, dann Phase 5 (Delete nach manueller Bestätigung)

**SPÄTER:**
7. 📦 Archivierte Ordner final reviewen
8. 🗑️ Lösch-Kandidaten durchgehen (Checkbox-Liste)
9. ✅ .gitignore update committen

---

**Last Updated:** 2025-12-08  
**Maintainer:** Patrick + Claude  
**Status:** 🚨 AWAITING REVIEW (Phase 1-4 bereit zur Ausführung)
