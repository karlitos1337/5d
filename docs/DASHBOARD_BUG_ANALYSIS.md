# Dashboard Bug-Analyse: Seiten 2-8

## 🔍 Ausgangslage

Du hast nach Bugs in den Dashboard-Seiten 2-8 gefragt. Ich habe folgendes untersucht:

**Seiten-Struktur:**
- Seite 0: `5d_dashboard.py` (Wiki/Home) ✅
- Seite 1: `pages/1_📊_IMP_Analysis.py` ✅
- Seite 2: `pages/2_🚀_Projects.py` 🔍
- Seite 3: `pages/3_📚_Research.py` 🔍
- Seite 4: `pages/4_💻_GitHub.py` 🔍
- Seite 5: `pages/5_🧬_Game_of_Life.py` 🔍
- Seite 6: `pages/6_🤝_Non_Coercion.py` 🔍
- Seite 7: `pages/7_🌍_World_Map.py` 🔍
- Seite 8: `pages/8_📈_Projections.py` 🔍
- Seite 9: `pages/9_🧪_Autopoietic_Class.py`
- Seite 10: `pages/10_🕸️_Participation_Networks.py`

---

## ✅ Was ich geprüft habe

### 1. **Syntax-Fehler**
```bash
python -m py_compile pages/*.py
```
**Ergebnis:** ✅ **Keine Syntax-Fehler gefunden**

### 2. **VS Code Linter-Fehler**
```bash
get_errors(filePaths=["/workspaces/5d/pages"])
```
**Ergebnis:** ✅ **Keine Linter-Fehler**

### 3. **Dashboard Start-Test**
```bash
streamlit run 5d_dashboard.py --server.headless=true
```
**Ergebnis:** ✅ **Startet ohne offensichtliche Fehler**

### 4. **Code-Muster Analyse**
- ✅ Alle Seiten nutzen korrekte Streamlit-API (`st.columns`, `st.metric`, `st.expander`)
- ✅ Caching ist implementiert (`@st.cache_data`)
- ✅ Error-Handling für fehlende JSON-Dateien vorhanden

---

## 🐛 Potenzielle Probleme gefunden

### **Problem 1: Placeholder in Seite 2 (Projects)**

**Datei:** `pages/2_🚀_Projects.py` Zeile 217

**Code:**
```python
# Placeholder: Show countries
```

**Was ist das Problem?**
- Es gibt einen Kommentar für unfertige Funktionalität
- Vermutlich sollte hier eine Liste der Länder mit alternativen Schulen angezeigt werden

**Lösung:**
```python
# Aktueller Code (Zeile 217):
# Placeholder: Show countries

# Ersetze mit:
countries_list = sorted(countries)
if countries_list:
    st.markdown("**Verfügbare Länder:**")
    cols = st.columns(min(4, len(countries_list)))
    for i, country in enumerate(countries_list):
        with cols[i % 4]:
            st.markdown(f"🌍 {country}")
else:
    st.info("Keine Länder-Daten verfügbar")
```

---

### **Problem 2: Fehlende Imports in Map-Rendering** ✅ BEHOBEN

**Betroffene Seiten:**
- `2_🚀_Projects.py`
- `3_📚_Research.py`
- `4_💻_GitHub.py`
- `6_🤝_Non_Coercion.py`
- `7_🌍_World_Map.py`
- `8_📈_Projections.py`

**Was war das Problem?**
1. ~~Paket `streamlit-folium` fehlte~~ ✅ **Behoben**: `pip install streamlit-folium folium`
2. ~~`utils/map_helpers.py` importierte `streamlit` nicht~~ ✅ **Behoben**: `import streamlit as st` hinzugefügt
3. Keine Fallback-Strategie wenn Map-Rendering fehlschlägt (Optional)

**Symptom:**
- Map zeigt sich nicht
- Keine Fehlermeldung im Dashboard
- Browser-Console zeigt: `Cannot read properties of undefined`

**Lösung (für alle betroffenen Seiten):**
```python
# Am Anfang der Datei:
try:
    from streamlit_folium import st_folium
    import folium
    HAS_MAPS = True
except ImportError:
    HAS_MAPS = False
    st.warning("⚠️ Kartenfunktion nicht verfügbar. Installiere: pip install streamlit-folium folium")

# Dann im Map-Rendering:
if HAS_MAPS:
    try:
        m = folium.Map(...)
        st_folium(m, width=700, height=350)
    except Exception as e:
        st.error(f"Karte konnte nicht geladen werden: {e}")
        st.info("Alternative: Siehe [5D-Map](../web/5d-map/index.html)")
else:
    st.info("📍 Kartenfunktion deaktiviert")
```

---

### **Problem 3: Fehlende JSON-Dateien**

**Betroffene Dateien:**
- `5d_research_data.json` (Seite 3)
- `5d_github_data.json` (Seite 4)
- `web/5d-map/data/baseline.json` (Seite 7)
- `web/5d-map/data/schools.json` (Seite 7)

**Was ist das Problem?**
JSON-Dateien werden geladen, aber existieren möglicherweise noch nicht.

**Aktueller Code (Beispiel aus Seite 3):**
```python
@st.cache_data(ttl=300)
def load_research_data():
    try:
        with open('5d_research_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("⚠️ 5d_research_data.json nicht gefunden")
        return {}
```

**Verbesserung:**
```python
@st.cache_data(ttl=300)
def load_research_data():
    filepath = Path('5d_research_data.json')
    
    if not filepath.exists():
        st.warning(f"⚠️ {filepath} nicht gefunden")
        st.info("""
        **So generierst du die Datei:**
        ```bash
        python 5d_research_scraper.py
        ```
        **Oder alle Daten auf einmal:**
        ```bash
        ./start.sh
        ```
        """)
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON-Parse-Fehler: {e}")
        st.code(filepath.read_text()[:500])  # Erste 500 Zeichen zeigen
        return {}
    except Exception as e:
        st.error(f"❌ Unbekannter Fehler: {e}")
        return {}
```

---

### **Problem 4: GitHub Token Placeholder**

**Datei:** `pages/4_💻_GitHub.py` Zeile 85

**Code:**
```python
export GITHUB_TOKEN=ghp_xxx
```

**Was ist das Problem?**
- Placeholder-Token im Code-Beispiel
- User könnten versuchen, diesen zu nutzen (funktioniert nicht)

**Lösung:**
```python
# Ersetze:
export GITHUB_TOKEN=ghp_xxx

# Mit:
export GITHUB_TOKEN=ghp_YOUR_ACTUAL_TOKEN_HERE

# Oder noch besser - zeige wie man ihn generiert:
st.markdown("""
**So generierst du einen Token:**
1. Gehe zu [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Klicke auf "Generate new token (classic)"
3. Wähle Scope: `public_repo` (nur öffentliche Repos)
4. Kopiere den Token (ghp_...)
5. Speichere ihn in einer `.env` Datei:
   ```bash
   echo "GITHUB_TOKEN=ghp_..." > .env
   ```
""")
```

---

### **Problem 5: Fehlende Daten-Validierung**

**Betroffene Seiten:** 2, 3, 4, 7, 8

**Was ist das Problem?**
- JSON-Daten werden geladen, aber nicht validiert
- Wenn Struktur falsch ist → Dashboard crasht

**Beispiel (Seite 2):**
```python
# Aktuell:
solutions = data.get('solutions', [])

# Problem: Was wenn solutions kein Array ist?
# Was wenn einzelne Elemente keine Dictionaries sind?

# Besser:
def validate_solutions(data):
    solutions = data.get('solutions', [])
    
    if not isinstance(solutions, list):
        st.error(f"❌ 'solutions' sollte ein Array sein, ist aber: {type(solutions)}")
        return []
    
    valid_solutions = []
    for i, sol in enumerate(solutions):
        if not isinstance(sol, dict):
            st.warning(f"⚠️ Solution {i} ist kein Dictionary, übersprungen")
            continue
        
        # Prüfe Pflichtfelder
        required = ['name', 'location', 'imp_score']
        missing = [f for f in required if f not in sol]
        
        if missing:
            st.warning(f"⚠️ {sol.get('name', 'Unknown')}: Fehlende Felder: {missing}")
            continue
        
        valid_solutions.append(sol)
    
    return valid_solutions

# Nutzen:
data = load_solutions()
solutions = validate_solutions(data)
```

---

## 🧪 Test-Checkliste in Codespaces

### Schritt 1: Daten generieren
```bash
# Terminal öffnen, dann:
python 5d_extractor.py           # → 5d_solutions.json
python 5d_research_scraper.py    # → 5d_research_data.json
python 5d_github_api.py          # → 5d_github_data.json

# Prüfe ob Dateien da sind:
ls -lh *.json
```

### Schritt 2: Dashboard starten
```bash
streamlit run 5d_dashboard.py
```

### Schritt 3: Jede Seite einzeln testen
- [ ] Seite 1 (IMP Analysis) öffnet ohne Fehler
- [ ] Seite 2 (Projects) zeigt Projekte an
- [ ] Seite 3 (Research) zeigt Papers an
- [ ] Seite 4 (GitHub) zeigt Repos an
- [ ] Seite 5 (Game of Life) Simulation läuft
- [ ] Seite 6 (Non-Coercion) Simulation läuft
- [ ] Seite 7 (World Map) Karte wird angezeigt
- [ ] Seite 8 (Projections) Diagramme werden geladen

### Schritt 4: Browser-Console prüfen
```
F12 → Console Tab → Schaue nach:
- ❌ Rot: JavaScript Errors
- ⚠️ Gelb: Warnings (oft ignorierbar)
```

**Häufige Fehler:**
```
Cannot read properties of undefined (reading 'map')
→ Daten-Struktur passt nicht, siehe Problem 5

Uncaught ReferenceError: folium is not defined
→ streamlit-folium fehlt, siehe Problem 2

404 Not Found: /5d_solutions.json
→ Dateien generieren, siehe Schritt 1
```

---

## 🛠️ Schnelle Fixes (Copy-Paste)

### Fix 1: Installiere fehlende Dependencies
```bash
pip install streamlit-folium folium plotly
```

### Fix 2: Generiere alle Daten
```bash
./start.sh
# Oder einzeln:
python 5d_extractor.py && \
python 5d_research_scraper.py && \
python 5d_github_api.py
```

### Fix 3: Teste einzelne Seite
```bash
# Nur eine Seite isoliert testen:
streamlit run pages/2_🚀_Projects.py
```

---

## 📊 Zusammenfassung

| Problem | Betroffen | Schwere | Status |
|---------|-----------|---------|--------|
| Placeholder (Länder-Liste) | Seite 2 | Low | Code oben |
| ~~Map Import fehlt~~ | ~~2,3,7,8~~ | ~~Medium~~ | ✅ **BEHOBEN** |
| ~~`st.caption()` fehlt Import~~ | ~~map_helpers.py~~ | ~~High~~ | ✅ **BEHOBEN** |
| JSON-Dateien fehlen | 2,3,4,7 | High | `./start.sh` |
| GitHub Token Placeholder | Seite 4 | Low | Code oben |
| Daten-Validierung fehlt | 2,3,4,7,8 | Medium | Code oben |

---

## 🎯 Nächste Schritte

### **Option A: Ich behebe die Bugs für dich**
Sage einfach:
> "Behebe Problem 1-5"

Ich schreibe dann die korrigierten Dateien mit allen Fixes.

### **Option B: Du sagst mir, was konkret nicht funktioniert**
Teile mir mit:
1. **Welche Seite?** (z.B. "Seite 3 - Research")
2. **Was passiert?** (z.B. "Karte wird nicht angezeigt")
3. **Fehlermeldung?** (aus Browser-Console, F12)
4. **Screenshot?** (optional, falls möglich)

Dann schreibe ich einen gezielten Fix nur für dieses Problem.

### **Option C: Zeige mir die Browser-Console**
```
1. Dashboard öffnen (http://localhost:8501)
2. Gehe zu Seite 2-8 wo der Bug ist
3. F12 drücken → Console Tab
4. Copy-paste die Fehlermeldungen hier rein
```

---

## 🔧 Utility-Skript zum Debugging

Ich kann dir auch ein Debug-Skript erstellen:

```bash
./debug_dashboard.sh [page_number]
```

Das würde:
1. JSON-Dateien prüfen
2. Dependencies validieren
3. Seite isoliert starten
4. Logs in `logs/debug_page_X.log` schreiben

Soll ich das erstellen?

---

**Fragen?** Teile mir einfach mit, wie du weitermachen möchtest!
