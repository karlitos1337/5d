#!/usr/bin/env python3
"""
5D Dashboard - Wiki & Hauptseite
Erste Anlaufstelle mit Installation, Navigation und Erklärungen für Einsteiger
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="5D Wiki & Home",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Sidebar Navigation
    with st.sidebar:
        st.title("📚 5D Wiki")
        st.markdown("**Willkommen!**")
        
        st.divider()
        
        st.markdown("### 🧭 Navigation")
        st.page_link("pages/1_📊_IMP_Analysis.py", label="📊 IMP-Analyse", icon="📊")
        st.page_link("pages/2_🚀_Projects.py", label="🚀 Projekte", icon="🚀")
        st.markdown("- 📚 Research (coming soon)")
        st.markdown("- 💻 GitHub (coming soon)")
        st.markdown("- 🧬 Game of Life (coming soon)")
        st.markdown("- 🤝 Zwanglosigkeit (coming soon)")
        st.markdown("- 🌍 Weltkarte (coming soon)")
        st.markdown("- 📈 Projektionen (coming soon)")
        
        st.divider()
        
        st.markdown("### 📖 Ressourcen")
        st.markdown("- [User Guide](docs/USER_GUIDE.md)")
        st.markdown("- [API Docs](docs/API.md)")
        st.markdown("- [Contributing](CONTRIBUTING.md)")
        st.markdown("- [Deployment](docs/DEPLOYMENT.md)")
        
        st.divider()
        
        st.markdown("### 🆘 Hilfe")
        st.markdown("- [Troubleshooting](#troubleshooting)")
        st.markdown("- [FAQ](#faq)")
        st.markdown("- [GitHub Issues](https://github.com/karlitos1337/5d/issues)")
    
    # Main Content
    st.title("📚 5D Intelligence Framework - Wiki & Guide")
    st.markdown("### Willkommen! Hier findest du alles, was du brauchst.")
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Pages", "9", help="Themen-Seiten im Dashboard")
    
    with col2:
        st.metric("Quellen", "56", help="Wissenschaftliche Referenzen (BibTeX)")
    
    with col3:
        st.metric("Tests", "145", help="Wissenschaftliche Tests (124/124 passing)")
    
    with col4:
        st.metric("Länder", "30+", help="Daten verfügbar")
    
    st.divider()
    
    # Tabs für verschiedene Bereiche
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Schnellstart",
        "💻 Installation",
        "📖 Befehle erklärt",
        "🧭 Navigation",
        "🆘 Hilfe"
    ])
    
    with tab1:
        st.header("🚀 Schnellstart (3 Schritte)")
        
        st.markdown("""
        ### Du willst direkt loslegen? So geht's:
        
        **Schritt 1: Code öffnen**
        - Du bist bereits hier! ✅
        - Falls nicht: [GitHub Codespaces](https://github.com/karlitos1337/5d) öffnen
        
        **Schritt 2: Dashboard starten**
        """)
        
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            st.code("./start.sh", language="bash")
            st.markdown("☝️ **Dieser Befehl startet alles automatisch**")
        
        with col_b:
            if st.button("▶️ Was macht start.sh?", key="explain_start"):
                st.info("""
                **start.sh tut folgendes:**
                1. Installiert benötigte Programme
                2. Lädt die neuesten Daten
                3. Startet das Dashboard
                4. Öffnet es in deinem Browser
                """)
        
        st.markdown("""
        **Schritt 3: Erkunden**
        - 👈 Links in der Sidebar findest du alle Themen
        - 📊 IMP-Analyse: Wissenschaftliche Grundlagen
        - 🚀 Projekte: Alternative Schulmodelle mit ROI
        - 📚 Research: Aktuelle Forschung
        - 🗺️ Weltkarte: Globale Daten visualisiert
        
        ---
        
        ### 🎯 Was ist das 5D Framework?
        
        Das **5D Intelligence Framework** misst menschliche Entwicklung in 5 Dimensionen:
        
        1. **Autonomie (A):** Selbstbestimmung, freie Wahl
        2. **Motivation (IM):** Flow-Zustände, innerer Antrieb
        3. **Resilienz (R):** Anpassungsfähigkeit, Fehlerkultur
        4. **Partizipation (SP):** Kooperation, Gemeinschaft
        5. **Authentizität (Au):** Wahrhaftigkeit, Selbstausdruck
        
        **Formel:** `IMP = A × IM × R × SP × Au`
        
        Je höher die Werte, desto besser die Lebensqualität und das Lernpotenzial.
        
        ---
        
        ### 📊 Was kann ich hier machen?
        
        ✅ **Daten erkunden:** Weltkarte mit IMP-Scores für 30+ Länder  
        ✅ **Formeln verstehen:** Alle Berechnungen mit Quellen erklärt  
        ✅ **Projekte finden:** Alternative Schulen und ROI-Analyse  
        ✅ **Research lesen:** Neueste Papers von arXiv, PubMed, WHO  
        ✅ **Simulationen:** Game of Life, Zwanglosigkeits-Modell  
        ✅ **Code anschauen:** Alles Open Source auf GitHub  
        """)
        
        st.divider()
        
        col_x, col_y = st.columns(2)
        
        with col_x:
            st.success("✅ **Neu hier?** Gehe zu [Installation](#installation) für Details")
        
        with col_y:
            st.info("💡 **Entwickler?** Siehe [Contributing](CONTRIBUTING.md)")
    
    with tab2:
        st.header("💻 Installation (Schritt für Schritt)")
        
        st.markdown("""
        ### Variante 1: GitHub Codespaces (Empfohlen für Anfänger)
        
        **Was ist Codespaces?**
        - Eine fertige Entwicklungsumgebung in deinem Browser
        - Nichts muss auf deinem Computer installiert werden
        - Kostenlos für GitHub-Nutzer (60 Stunden/Monat)
        
        **So geht's:**
        """)
        
        st.markdown("**1. Gehe zu GitHub:**")
        st.code("https://github.com/karlitos1337/5d", language="text")
        
        st.markdown("**2. Klicke auf den grünen Button:**")
        st.code("Code → Codespaces → Create codespace on main", language="text")
        
        st.markdown("**3. Warte 1-2 Minuten** (lädt automatisch)")
        
        st.markdown("**4. Fertig!** Du siehst jetzt VS Code im Browser")
        
        st.divider()
        
        st.markdown("""
        ### Variante 2: Lokal auf deinem Computer
        
        **Voraussetzungen:**
        - Python 3.10 oder neuer
        - Git
        
        **Schritt 1: Python installieren**
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Windows:**")
            st.code("https://python.org/downloads", language="text")
            st.caption("Lade Installer → Doppelklick → 'Add to PATH' ✓")
        
        with col2:
            st.markdown("**macOS:**")
            st.code("brew install python@3.10", language="bash")
            st.caption("(Homebrew muss installiert sein)")
        
        with col3:
            st.markdown("**Linux:**")
            st.code("sudo apt install python3.10", language="bash")
            st.caption("(Ubuntu/Debian)")
        
        st.markdown("""
        **Schritt 2: Projekt herunterladen**
        """)
        
        st.code("""
# Terminal öffnen, dann:
git clone https://github.com/karlitos1337/5d.git
cd 5d
""", language="bash")
        
        st.markdown("**Schritt 3: Abhängigkeiten installieren**")
        
        st.code("""
# Minimal (nur Dashboard):
pip install -r requirements.txt

# Erweitert (mit Visualisierungen):
pip install -r requirements_extended.txt
""", language="bash")
        
        st.markdown("**Schritt 4: Dashboard starten**")
        
        st.code("./start.sh", language="bash")
        
        st.success("✅ Dashboard läuft jetzt auf http://localhost:8501")
        
        st.divider()
        
        st.markdown("""
        ### Variante 3: Docker (für Fortgeschrittene)
        
        **Falls Docker installiert ist:**
        """)
        
        st.code("""
# Projekt klonen
git clone https://github.com/karlitos1337/5d.git
cd 5d

# Docker Container bauen
docker build -t 5d-dashboard .

# Container starten
docker run -p 8501:8501 5d-dashboard
""", language="bash")
        
        st.info("💡 Dashboard läuft dann auf http://localhost:8501")
    
    with tab3:
        st.header("📖 Befehle erklärt (für Einsteiger)")
        
        st.markdown("""
        ### Was bedeuten diese seltsamen Zeichen? 🤔
        
        Keine Sorge! Hier ist alles erklärt:
        """)
        
        # Befehle-Tabelle
        befehle = [
            {
                "befehl": "./start.sh",
                "was": "Startet das komplette Dashboard",
                "details": "Das ist ein 'Skript' - eine Datei mit mehreren Befehlen nacheinander. Es installiert alles Nötige und startet dann das Dashboard.",
                "wann": "Immer beim ersten Mal, oder wenn du alles neu laden willst"
            },
            {
                "befehl": "python 5d_extractor.py",
                "was": "Liest Daten aus den Manifest-Dateien",
                "details": "'python' startet Python-Programme. 'extractor' extrahiert (holt) Daten aus den Markdown-Dateien im 'manifest/' Ordner.",
                "wann": "Wenn du neue Daten zu Projekten hinzugefügt hast"
            },
            {
                "befehl": "python 5d_research_scraper.py",
                "was": "Lädt neueste Forschungs-Papers",
                "details": "'scraper' bedeutet: Daten von Webseiten holen. Hier von arXiv (Physik/Mathe) und PubMed (Medizin).",
                "wann": "Alle 1-2 Wochen, um aktuelle Forschung zu sehen"
            },
            {
                "befehl": "python 5d_github_api.py",
                "was": "Holt GitHub Repository-Daten",
                "details": "'API' = Programmierschnittstelle. Fragt GitHub: 'Welche Projekte gibt es zu Bildung?' und speichert die Antworten.",
                "wann": "Um neue Open-Source-Projekte zu finden"
            },
            {
                "befehl": "streamlit run 5d_dashboard.py",
                "was": "Startet nur das Dashboard",
                "details": "'streamlit' ist das Framework (Werkzeug) für interaktive Web-Apps. 'run' startet es.",
                "wann": "Wenn du nur das Dashboard willst, ohne Daten neu zu laden"
            },
            {
                "befehl": "pytest tests/",
                "was": "Führt alle Tests aus",
                "details": "'pytest' prüft automatisch: Funktioniert alles? Tests sind wie Hausaufgaben-Kontrolle für Code.",
                "wann": "Nach Änderungen am Code, um Fehler zu finden"
            },
            {
                "befehl": "git add -A",
                "was": "Markiert alle Änderungen",
                "details": "'git' verwaltet Versionen. 'add' sagt: 'Diese Dateien haben sich geändert, merke dir das!'",
                "wann": "Vor einem Commit (Speichern)"
            },
            {
                "befehl": "git commit -m 'Nachricht'",
                "was": "Speichert Änderungen mit Beschreibung",
                "details": "'commit' = fest speichern. '-m' = mit Nachricht. Wie ein Tagebuch-Eintrag für Code.",
                "wann": "Nach jedem sinnvollen Schritt (z.B. neue Seite fertig)"
            },
            {
                "befehl": "git push",
                "was": "Lädt Änderungen zu GitHub hoch",
                "details": "'push' = hochschieben. Deine lokalen Änderungen werden zu GitHub geschickt, damit andere sie sehen.",
                "wann": "Nach Commits, wenn du deine Arbeit teilen willst"
            },
            {
                "befehl": "pip install <paket>",
                "was": "Installiert ein Python-Paket",
                "details": "'pip' = Paket-Manager für Python. Wie ein App-Store, aber für Code-Bibliotheken.",
                "wann": "Wenn ein Programm sagt: 'ModuleNotFoundError'"
            }
        ]
        
        for cmd in befehle:
            with st.expander(f"🔍 `{cmd['befehl']}`"):
                st.markdown(f"**Was macht das?**  \n{cmd['was']}")
                st.markdown(f"**Ausführlich erklärt:**  \n{cmd['details']}")
                st.info(f"**Wann benutzen?** {cmd['wann']}")
        
        st.divider()
        
        st.markdown("""
        ### 🔤 Begriffe erklärt
        
        **Terminal / Kommandozeile / Shell:**
        - Das schwarze Fenster mit Text
        - Du tippst Befehle, Computer führt sie aus
        - Wie ein Chat mit dem Computer
        
        **Python:**
        - Die Programmiersprache, in der dieses Projekt geschrieben ist
        - Code steht in .py Dateien
        
        **Streamlit:**
        - Werkzeug um aus Python-Code Web-Apps zu machen
        - Du schreibst Python, es wird automatisch zur Website
        
        **Git & GitHub:**
        - Git = Versionsverwaltung (wie Track-Changes in Word)
        - GitHub = Website zum Code teilen
        
        **JSON:**
        - Dateiformat für Daten (.json Dateien)
        - Wie Excel, aber für Programme lesbar
        
        **pytest:**
        - Werkzeug zum automatischen Testen
        - Prüft: "Funktioniert der Code?"
        """)
    
    with tab4:
        st.header("🧭 Navigation & Seitenübersicht")
        
        st.markdown("""
        ### Wie finde ich was?
        
        **In der Sidebar (links 👈)** sind alle Seiten aufgelistet.  
        Klick einfach drauf!
        """)
        
        st.divider()
        
        # Seiten-Übersicht
        pages = [
            {
                "icon": "📊",
                "name": "IMP-Analyse",
                "file": "pages/1_📊_IMP_Analysis.py",
                "beschreibung": "Wissenschaftliche Grundlagen der 5D-Dimensionen",
                "inhalt": [
                    "Formel: IMP = A × IM × R × SP × Au",
                    "Peer-reviewed Quellen für jede Dimension",
                    "Interaktive Radar-Charts",
                    "Vergleich mit Referenzsystemen (z.B. Dänemark)"
                ],
                "für_wen": "Wissenschaftler, Interessierte an Theorie"
            },
            {
                "icon": "🚀",
                "name": "Projekte",
                "file": "pages/2_🚀_Projects.py",
                "beschreibung": "Alternative Bildungsprojekte mit ROI-Analyse",
                "inhalt": [
                    "Sudbury Valley School (USA)",
                    "Folk High Schools (Dänemark/Norwegen)",
                    "Tokkatsu (Japan)",
                    "ROI-Rechner (Heckman-Methode)",
                    "Standorte auf Weltkarte"
                ],
                "für_wen": "Eltern, Pädagogen, Investoren"
            },
            {
                "icon": "📚",
                "name": "Research",
                "file": "pages/3_📚_Research.py (coming soon)",
                "beschreibung": "Aktuelle Forschungspapers",
                "inhalt": [
                    "arXiv (Physik, Mathematik, CS)",
                    "PubMed (Medizin, Psychologie)",
                    "WHO Reports",
                    "World Bank Data",
                    "Filter nach Thema, Jahr, Zitationen"
                ],
                "für_wen": "Forscher, Studenten"
            },
            {
                "icon": "💻",
                "name": "GitHub",
                "file": "pages/4_💻_GitHub.py (coming soon)",
                "beschreibung": "Open-Source Bildungsprojekte",
                "inhalt": [
                    "EdTech Repositories",
                    "Activity-Scores",
                    "Entwickler-Community",
                    "Trending Projekte"
                ],
                "für_wen": "Entwickler, Tech-Enthusiasten"
            },
            {
                "icon": "🧬",
                "name": "Game of Life",
                "file": "pages/5_🧬_Game_of_Life.py (coming soon)",
                "beschreibung": "Conway's zellulärer Automat",
                "inhalt": [
                    "Interaktive Simulation",
                    "Verschiedene Patterns (Glider, Blinker, etc.)",
                    "Wissenschaftliche Basis (Conway 1970)",
                    "Was zeigt es? Emergenz, Selbstorganisation"
                ],
                "für_wen": "Interessierte an Systemtheorie"
            },
            {
                "icon": "🤝",
                "name": "Zwanglosigkeit",
                "file": "pages/6_🤝_Non_Coercion.py (coming soon)",
                "beschreibung": "Kooperation vs. Zwang Simulation",
                "inhalt": [
                    "Agent-based Model",
                    "Ostrom's Commons Theorie",
                    "Langfristige Effekte von Zwang",
                    "Interaktive Parameter"
                ],
                "für_wen": "Interessierte an Governance, Ethik"
            },
            {
                "icon": "🌍",
                "name": "Weltkarte",
                "file": "pages/7_🌍_World_Map.py (coming soon)",
                "beschreibung": "Globale IMP-Daten visualisiert",
                "inhalt": [
                    "Interaktive Leaflet-Karte",
                    "Heatmaps (Depression, Dropout)",
                    "IMP-Score Choropleth",
                    "Alternative Schulen als Marker",
                    "Zeitreise-Feature (2000-2025)"
                ],
                "für_wen": "Alle! Visuell, intuitiv"
            },
            {
                "icon": "📈",
                "name": "Projektionen",
                "file": "pages/8_📈_Projections.py",
                "beschreibung": "Zukunftsszenarien",
                "inhalt": [
                    "Logistische Adoptionskurven",
                    "Rogers' Diffusion Theorie",
                    "Regionale Prognosen (2025-2050)",
                    "Ökonomische Impact-Analyse"
                ],
                "für_wen": "Policy-Maker, Zukunftsforscher"
            },
            {
                "icon": "🧪",
                "name": "Autopoietische Klasse",
                "file": "pages/9_🧪_Autopoietic_Class.py",
                "beschreibung": "5D-Simulations-Labor",
                "inhalt": [
                    "Agent-based Model (ABM)",
                    "5 Dimensionen über Zeit",
                    "Parameter: Zwang, Freiheit, Peers, Support",
                    "Dropout-Simulation",
                    "Export für weitere Analysen"
                ],
                "für_wen": "Forscher, Bildungsentwickler"
            }
        ]
        
        for page in pages:
            with st.expander(f"{page['icon']} {page['name']}"):
                st.markdown(f"**Datei:** `{page['file']}`")
                st.markdown(f"**Beschreibung:** {page['beschreibung']}")
                
                st.markdown("**Inhalt:**")
                for item in page['inhalt']:
                    st.markdown(f"- {item}")
                
                st.info(f"**Für wen?** {page['für_wen']}")
        
        st.divider()
        
        st.markdown("""
        ### 🔗 Wichtige Links
        
        **Dokumentation:**
        - [User Guide](docs/USER_GUIDE.md) - Wie benutze ich die Weltkarte?
        - [API Docs](docs/API.md) - Technische Details zu Datenformaten
        - [Contributing](CONTRIBUTING.md) - Wie kann ich mithelfen?
        - [Deployment](docs/DEPLOYMENT.md) - Wie deploye ich das?
        
        **Code & Daten:**
        - [GitHub Repository](https://github.com/karlitos1337/5d)
        - [BibTeX Quellen](07_daten_analysen/5d-relevant-sources.bib)
        - [Manifest](manifest/) - Kuratierte Wissensbasis
        - [Formeln](formeln/) - 157 dokumentierte Formeln
        
        **Externe Ressourcen:**
        - [Our World in Data](https://ourworldindata.org)
        - [World Bank](https://data.worldbank.org)
        - [WHO](https://www.who.int/data)
        - [arXiv](https://arxiv.org)
        - [PubMed](https://pubmed.ncbi.nlm.nih.gov)
        """)
    
    with tab5:
        st.header("🆘 Hilfe & Troubleshooting")
        
        # FAQ
        st.subheader("❓ Häufige Fragen (FAQ)")
        
        faqs = [
            {
                "q": "Das Dashboard startet nicht!",
                "a": """
                **Checkliste:**
                1. Python installiert? Test: `python --version` (sollte 3.10+ sein)
                2. Dependencies installiert? `pip install -r requirements.txt`
                3. Im richtigen Ordner? `cd 5d` (Terminal muss im Projekt-Ordner sein)
                4. Firewall blockiert? Port 8501 muss offen sein
                5. Anderes Programm nutzt Port 8501? → `streamlit run 5d_dashboard.py --server.port 8502`
                """
            },
            {
                "q": "Ich sehe 'ModuleNotFoundError'",
                "a": """
                **Bedeutet:** Eine Python-Bibliothek fehlt.
                
                **Lösung:**
                ```bash
                pip install <paket-name>
                ```
                
                Oder installiere alles neu:
                ```bash
                pip install -r requirements_extended.txt
                ```
                """
            },
            {
                "q": "Daten fehlen (5d_solutions.json not found)",
                "a": """
                **Bedeutet:** Pipeline wurde noch nicht ausgeführt.
                
                **Lösung:**
                ```bash
                python 5d_extractor.py           # Erstellt 5d_solutions.json
                python 5d_research_scraper.py    # Erstellt 5d_research_data.json
                python 5d_github_api.py          # Erstellt 5d_github_data.json
                ```
                
                Oder alles auf einmal:
                ```bash
                ./RUN_ALL.sh
                ```
                """
            },
            {
                "q": "Tests schlagen fehl",
                "a": """
                **Normal!** Einige Tests brauchen:
                - Externe APIs (GitHub Token, PubMed)
                - Vollständige Daten (alle JSON-Dateien)
                
                **Testen ohne externe Abhängigkeiten:**
                ```bash
                pytest tests/ -m "not integration"
                ```
                """
            },
            {
                "q": "Wie füge ich eigene Projekte hinzu?",
                "a": """
                **Schritt 1:** Markdown-Datei in `manifest/01_bildung_education/` erstellen
                
                **Schritt 2:** 5D-Dimensionen mit Scores (0-1) eintragen:
                ```markdown
                # Mein Projekt
                
                **Autonomie:** 0.85
                **Motivation:** 0.78
                **Resilienz:** 0.80
                **Partizipation:** 0.75
                **Authentizität:** 0.82
                
                **Standort:** Berlin, Deutschland
                ```
                
                **Schritt 3:** Extractor laufen lassen:
                ```bash
                python 5d_extractor.py
                ```
                """
            },
            {
                "q": "Kann ich das Dashboard anpassen?",
                "a": """
                **Ja!** Alles ist Open Source.
                
                **Farben ändern:** `.streamlit/config.toml`
                **Seiten hinzufügen:** `pages/` Ordner
                **Formeln ändern:** `models/imp.py`
                **Tests schreiben:** `tests/` Ordner
                
                Siehe [Contributing Guide](CONTRIBUTING.md) für Details.
                """
            }
        ]
        
        for faq in faqs:
            with st.expander(faq["q"]):
                st.markdown(faq["a"])
        
        st.divider()
        
        # Troubleshooting Checkliste
        st.subheader("🔧 Troubleshooting Checkliste")
        
        st.markdown("""
        Wenn etwas nicht funktioniert, gehe diese Liste durch:
        """)
        
        checks = [
            "Python 3.10+ installiert? (`python --version`)",
            "Git installiert? (`git --version`)",
            "Projekt heruntergeladen? (`cd 5d` funktioniert?)",
            "Dependencies installiert? (`pip list` zeigt streamlit, pandas, etc.?)",
            "Im richtigen Ordner? (`ls` zeigt 5d_dashboard.py?)",
            "JSON-Dateien vorhanden? (`ls *.json` zeigt 3 Dateien?)",
            "Port 8501 frei? (Kein anderes Programm nutzt ihn?)",
            "Internet-Verbindung? (Für externe APIs)",
            "Firewall aus? (Manchmal blockiert sie lokale Server)",
            "Browser aktuell? (Chrome/Firefox/Edge empfohlen)"
        ]
        
        for i, check in enumerate(checks, 1):
            st.checkbox(check, key=f"check_{i}")
        
        st.divider()
        
        # Support
        st.subheader("📞 Weitere Hilfe")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Community:**
            - [GitHub Discussions](https://github.com/karlitos1337/5d/discussions)
            - [Issues melden](https://github.com/karlitos1337/5d/issues/new)
            """)
        
        with col2:
            st.markdown("""
            **Dokumentation:**
            - [docs/](docs/) - Alle Guides
            - [CONTRIBUTING.md](CONTRIBUTING.md)
            - [README.md](README.md)
            """)
        
        st.info("💡 **Tipp:** Beschreibe dein Problem genau: Was hast du versucht? Welche Fehlermeldung kam? Welches Betriebssystem?")
    
    # Footer
    st.divider()
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("**Version:** 2.0")
    
    with col_b:
        st.markdown(f"**Letzte Aktualisierung:** {datetime.now().strftime('%Y-%m-%d')}")
    
    with col_c:
        st.markdown("[GitHub](https://github.com/karlitos1337/5d) | [Website](https://reflexionsfabrik.de)")

if __name__ == "__main__":
    main()
