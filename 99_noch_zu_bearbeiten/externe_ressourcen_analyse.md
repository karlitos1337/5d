# 🔗 Externe Ressourcen-Integration: 16 analysierte URLs

**Datum**: 2025-12-02  
**Status**: Analyse abgeschlossen, Integration ausstehend  
**Analyst**: Qwen + Perplexity AI

---

## 📊 Zusammenfassung

| Priorität | Anzahl | Ressourcen |
|-----------|--------|------------|
| 🔴 KRITISCH (9-10) | 7 | Microsoft AI, Free Programming Books, Wolfram\|Alpha, AweXplor, FMHYB64, Learn Anything, Elicit, Awesome Cheatsheets |
| 🟡 HOCH (7-8) | 4 | GitHub Docs, FutureTools, HackTricks, Physics Simulations |
| 🟢 MITTEL (5-6) | 3 | GPTs Prompts, Doomsday Calculator |
| 🔵 NIEDRIG (<5) | 2 | Lost Media Wiki |

---

## 🔴 KRITISCHE Ressourcen (Score 9-10)

### 1. Learn Anything
- **URL**: https://learn-anything.xyz/
- **Typ**: Knowledge Graph Platform
- **Score**: 10/10
- **Relevanz**: 🚨 **DIREKTER COMPETITOR/VORBILD** für 5D-Wissenskarte!
- **Features**:
  - Knowledge Graph Visualization
  - Prerequisites & Learning Paths
  - Community-curated Content
  - Open-Source (MIT License)
- **Integration**:
  ```
  🚨 SOFORTIGE ANALYSE ERFORDERLICH
  - Architektur-Studie für web/5d-map/
  - Graph-Algorithmen (kürzester Pfad, Prerequisites)
  - UI/UX-Patterns übernehmen
  - Community-Beitrags-Modell
  ```
- **Action Items**:
  - [ ] GitHub Repo clonen & analysieren: `oseducation/knowledge-graph`
  - [ ] Vergleich mit 5D-Schema (`5d-knowledge-graph.schema.json`)
  - [ ] Dokumentation in `06_synthesen_kompilationen/competitor_analysis.md`

---

### 2. FMHYB64 (FreeMedieHeckYeah)
- **URL**: https://rentry.co/FMHYB64#learn-anything
- **Typ**: Mega-Resource Index
- **Score**: 10/10
- **Relevanz**: 🔴 **GOLDMINE** - umfassendster kostenloser Ressourcen-Index
- **Features**:
  - 10.000+ kuratierte Links
  - Educational Section: Learn Anything, OSSU, OpenCulture, Khan Academy
  - AI Tools, Programming, Science, Languages
  - Reddit Community (r/FREEMEDIAHECKYEAH)
  - GitHub Backups
- **Integration**:
  ```
  01_bildung_education/free_resources_mega_index.md
  - Querverweise zu allen 5D-Dimensionen
  - BibTeX-Eintrag
  - Link zu OSSU/IB-Bridge
  ```
- **BibTeX**:
  ```bibtex
  @misc{fmhy2025,
    title = {FreeMedieHeckYeah: The Largest Collection of Free Stuff on the Internet},
    author = {{FMHY Community}},
    year = {2025},
    howpublished = {\\url{https://fmhy.net}},
    note = {Educational section includes OSSU, Learn Anything, OpenCulture}
  }
  ```

---

### 3. Microsoft Generative AI for Beginners
- **URL**: https://microsoft.github.io/generative-ai-for-beginners/
- **Score**: 10/10
- **Features**:
  - 18 Lektionen (Learn + Build)
  - GitHub-basiert, forkbar
  - Video-Intros, Code-Beispiele, Challenges
  - Discord Community Support
- **Integration**:
  ```
  06_synthesen_kompilationen/ossu_ib_bridge.md
  - Erweiterung: AI/ML Track
  - Referenz in BibTeX
  - Lernpfad für 02_neurobiologie (Cognitive Load, Flow)
  ```

---

### 4. Free Programming Books (EbookFoundation)
- **URL**: https://github.com/EbookFoundation/free-programming-books.git
- **Score**: 10/10
- **Features**:
  - 8000+ Links, 43 Sprachen
  - 2000+ Mitwirkende
  - GitHub Top-10 Starred Repo (243k Stars)
- **Integration**:
  ```
  01_bildung_education/free_resources_index.md
  - BibTeX-Eintrag
  - Verknüpfung mit OSSU/IB-Bridge
  ```
- **BibTeX**:
  ```bibtex
  @misc{freeprogrammingbooks2025,
    author = {{Free Ebook Foundation}},
    title = {Free Programming Books},
    year = {2025},
    howpublished = {\\url{https://github.com/EbookFoundation/free-programming-books}},
    note = {8000+ free learning resources in 43 languages}
  }
  ```

---

### 5. Elicit AI Research Assistant
- **URL**: https://elicit.com/
- **Score**: 9/10
- **Features**:
  - Automated Literature Search (inkl. Paywalls)
  - AI-powered Paper Summarization
  - Metadata Extraction (Publication Date, Study Type, N)
  - CSV Export für Meta-Analysen
- **Integration**:
  ```
  07_daten_analysen/research_automation.md
  - Integration in BibTeX-Workflow
  - Tool-Empfehlung für Akademiker
  ```

---

### 6. Awesome Cheatsheets
- **URL**: https://lecoupa.github.io/awesome-cheatsheets/
- **Score**: 9/10
- **Features**:
  - 30+ Cheatsheets (Frontend, Backend, Database, Tools)
  - Single-File-Format (1 Datei = 1 Technologie)
  - GitHub 39.9k Stars
- **Integration**:
  ```
  01_bildung_education/technical_references.md
  - Link von OSSU-Bridge
  - Submodule in 05_technologie_tesla/
  ```
- **BibTeX**:
  ```bibtex
  @misc{awesomecheatsheets2024,
    author = {LeCoupa},
    title = {Awesome Cheatsheets: Quick References for Developers},
    year = {2024},
    howpublished = {\\url{https://github.com/LeCoupa/awesome-cheatsheets}},
    note = {30+ programming language and framework cheatsheets}
  }
  ```

---

### 7. AweXplor (Awesome Explorer)
- **URL**: https://github.com/AweXplor/awexplor.github.io.git
- **Score**: 9/10
- **Features**:
  - Sortierung nach Popularität/Aktivität
  - Filter für unmaintained/archived Repos
  - GitHub API Integration (Rate Limits)
  - Responsive Design für Mobile
- **Integration**:
  ```
  Frontend-Architektur für web/5d-map/
  - GitHub API Best Practices
  - Responsive Design Patterns
  ```

---

## 🟡 HOHE Priorität (Score 7-8)

### 8. GitHub Docs Repository
- **URL**: https://github.com/github/docs.git
- **Score**: 8/10
- **Features**:
  - Markdown-basierte Docs mit YAML Frontmatter
  - Strukturiertes Content-Model (Categories, Map Topics)
  - Automated Testing & Validation
- **Integration**:
  ```
  Template für WISSENS_INDEX.md
  - GitHub Actions Workflow-Inspiration
  ```

---

### 9. HackTricks
- **URL**: https://book.hacktricks.wiki/en/index.html
- **Score**: 8/10
- **⚠️ ETHISCH SENSIBEL**: Offensiv-Security-Wissen
- **Features**:
  - Pentesting-Methodologie (Web, Network, Cloud)
  - GitBook-Format (strukturiert, durchsuchbar)
  - HackTricks Training & Certification
- **Integration**:
  ```
  05_technologie_tesla/security_fundamentals.md
  - MIT ETHISCHEM DISCLAIMER
  - Referenz für Systemdesign
  - NICHT für Exploit-Anleitung
  ```

---

### 10. FutureTools.io
- **URL**: https://www.futuretools.io/?pricing-model=free
- **Score**: 7/10
- **Features**:
  - 600+ Tools mit Semantic Search
  - Pricing-Model-Filter (Free/Paid)
  - Kategorie-Tags (Music, Video, Code)
- **Integration**:
  ```
  07_daten_analysen/tool_evaluation.md
  - NICHT als primäre Quelle (kommerziell)
  ```

---

### 11. Physics Simulations (CSUN)
- **URL**: https://www.csun.edu/science/software/simulations/physics.html
- **Score**: 7/10
- **⚠️ ACHTUNG**: Teilweise veraltete Flash-Technologie
- **Features**:
  - PHET Simulations (University of Colorado)
  - Vector Arithmetic Visualizations
  - Light & Optics Simulations
- **Integration**:
  ```
  02_neurobiologie_psychologie/visual_learning_tools.md
  - Mit Hinweis auf moderne HTML5-Alternativen
  - NIEDRIGE PRIORITÄT
  ```

---

## 🟢 MITTLERE Priorität (Score 5-6)

### 12. GPTs Prompt Leak Repository
- **URL**: https://github.com/linexjlin/GPTs.git
- **Score**: 6/10
- **⚠️ ETHISCH PROBLEMATISCH**: Geleakte IPs
- **Features**:
  - 200+ GPT System Prompts
  - Reverse-Engineering von Prompt-Strukturen
- **Integration**:
  ```
  02_neurobiologie_psychologie/prompt_engineering_patterns.md
  - Mit ethischem Disclaimer
  - NICHT direkte Verwendung
  - NUR akademische Analyse
  ```

---

### 13. Doomsday Argument Calculator
- **URL**: https://doomsday.march1studios.com/
- **Score**: 5/10
- **Features**:
  - Bayesianische Inferenz
  - Interaktive Visualisierung
- **Integration**:
  ```
  03_philosophie_epistemologie/existential_risk_frameworks.md
  - Optional
  - Beispiel für probabilistische Modellierung
  ```

---

## 🔵 NIEDRIGE Priorität (Score <5)

### 14. Lost Media Wiki
- **URL**: https://lostmediawiki.com/Home
- **Score**: 3/10
- **Features**:
  - Community-driven Archivierung
  - MediaWiki-Struktur
- **Integration**:
  ```
  08_personal_biografie/ (optional)
  - Archivierungs-Philosophie
  - NIEDRIGE PRIORITÄT
  ```

---

## 🔄 Bereits Integriert

### 15. Wolfram|Alpha
- **URL**: https://www.wolframalpha.com/
- **Score**: 10/10
- **Status**: ✅ BEREITS in `07_daten_analysen/5d-relevant-sources.bib` (wolframalpha)
- **Features**:
  - Symbolische Mathematik
  - Wissenschaftliche Datenbanken
  - API verfügbar
- **Integration**:
  ```
  API für Dashboard-Validierung (geplant)
  ```

---

## 📋 Action Items (Gesamt)

### Sprint 1 (KRITISCH)
- [ ] **Learn Anything** analysieren: Architektur, Graph-Algorithmen, UI/UX
- [ ] **FMHYB64** integrieren: `01_bildung_education/free_resources_mega_index.md`
- [ ] **BibTeX erweitern**: Free Programming Books, Awesome Cheatsheets, FMHYB64
- [ ] **Elicit** dokumentieren: `07_daten_analysen/research_automation.md`
- [ ] **Microsoft AI Course** verlinken: `06_synthesen_kompilationen/ossu_ib_bridge.md`

### Sprint 2 (HOCH)
- [ ] **AweXplor** Architektur studieren für `web/5d-map/`
- [ ] **GitHub Docs** Content-Model für WISSENS_INDEX.md
- [ ] **HackTricks** mit Disclaimer: `05_technologie_tesla/security_fundamentals.md`

### Sprint 3 (MITTEL)
- [ ] **Physics Simulations** mit HTML5-Alternativen: `02_neurobiologie_psychologie/`
- [ ] **GPTs Prompts** ethische Analyse: `02_neurobiologie_psychologie/prompt_engineering_patterns.md`

---

## 📚 BibTeX-Erweiterungen (TODO)

Folgende Einträge müssen in `07_daten_analysen/5d-relevant-sources.bib` ergänzt werden:

```bibtex
@misc{fmhy2025,
  title = {FreeMedieHeckYeah: The Largest Collection of Free Stuff on the Internet},
  author = {{FMHY Community}},
  year = {2025},
  howpublished = {\\url{https://fmhy.net}},
  note = {Educational section includes OSSU, Learn Anything, OpenCulture}
}

@misc{freeprogrammingbooks2025,
  author = {{Free Ebook Foundation}},
  title = {Free Programming Books},
  year = {2025},
  howpublished = {\\url{https://github.com/EbookFoundation/free-programming-books}},
  note = {8000+ free learning resources in 43 languages}
}

@misc{awesomecheatsheets2024,
  author = {LeCoupa},
  title = {Awesome Cheatsheets: Quick References for Developers},
  year = {2024},
  howpublished = {\\url{https://github.com/LeCoupa/awesome-cheatsheets}},
  note = {30+ programming language and framework cheatsheets}
}

@misc{learnanything2025,
  title = {Learn Anything: Open Knowledge Graph for Learning},
  author = {{Learn Anything Community}},
  year = {2025},
  howpublished = {\\url{https://learn-anything.xyz/}},
  note = {Interactive knowledge graph with prerequisites and learning paths}
}

@misc{elicit2025,
  title = {Elicit: AI Research Assistant},
  author = {{Elicit, Inc.}},
  year = {2025},
  howpublished = {\\url{https://elicit.com/}},
  note = {GPT-powered literature review and paper summarization tool}
}

@misc{microsoftai2024,
  author = {{Microsoft Cloud Advocates}},
  title = {Generative AI for Beginners},
  year = {2024},
  howpublished = {\\url{https://microsoft.github.io/generative-ai-for-beginners/}},
  note = {18-lesson course on generative AI with Python and TypeScript examples}
}

@misc{hacktricks2023,
  title = {HackTricks: Pentesting Knowledge Base},
  author = {{HackTricks Community}},
  year = {2023},
  howpublished = {\\url{https://book.hacktricks.wiki/}},
  note = {Comprehensive penetration testing methodology and techniques}
}
```

---

**Version**: 1.0.0  
**Letzte Aktualisierung**: 2025-12-02  
**Nächste Review**: Nach Sprint 1 Implementierung
