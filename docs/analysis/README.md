# 5D Repository - Interaktive Analyse-Dokumentation

## 🎯 Übersicht

Zwei interaktive Analyse-Seiten für das 5D-Repository:

### 1. **Repository-Struktur-Analyse** (⭐ Empfohlen)
- **Datei**: `repository-standalone.html`
- **Fokus**: 8 Domänenordner & 5 Dimensionen
- **Features**: Standalone HTML, sofort nutzbar
- **URL**: [repository-standalone.html](./repository-standalone.html)

### 2. **Vollständige technische Analyse**
- **Datei**: `src/App.jsx` (in Entwicklung)
- **Fokus**: DDD, Architektur, Code-Qualität
- **Features**: React + Vite Build-System

## 🚀 Quick Start

### Option 1: Standalone HTML (⚡ Schnellste)

```bash
cd docs/analysis
python3 -m http.server 8080
# Öffne http://localhost:8080/repository-standalone.html
```

Oder einfach `repository-standalone.html` direkt im Browser öffnen!

### Option 2: React Development

```bash
cd docs/analysis
npm install
npm run dev
```

## 📊 Inhalte

### Repository-Struktur-Analyse

1. **Übersicht**
   - 8 Domänenordner (01-08)
   - 5 Dimensionen-Framework
   - Visuelle Architektur-Darstellung

2. **5D Methodologie**
   - Define, Design, Develop
   - Debug, Deliver, Feedback
   - Iterative Verbesserung

3. **Analyseergebnisse**
   - Domänenstruktur
   - SQL-Datenmodell (635 KB)
   - Dokumentationsbedarf

4. **Architektur**
   - SOLID-Prinzipien
   - DDD-Integration
   - Best Practices

## 🛠️ Features

- ☀️/**🌙 Dark/Light Mode**
- 📱 **Responsive Design**
- ⚡ **Smooth Scrolling**
- 🖼️ **Visualisierungen**
- 🔗 **Externe Quellenlinks**

## 📂 Dateistruktur

```
docs/analysis/
├── repository-standalone.html    # ⭐ Standalone Version
├── src/
│   ├── App.jsx                   # Haupt-Komponente (WIP)
│   ├── RepositoryAnalysis.jsx    # Zweite Variante
│   ├── main.jsx                  # Entry Point
│   └── index.css                 # Styles
├── index.html                    # Haupt-HTML
├── repository.html               # Zweite HTML
├── package.json                  # Dependencies (zu erstellen)
├── vite.config.js
├── tailwind.config.js
└── README.md                     # Diese Datei
```

## 🔗 Integration mit 5D-Framework

### Verlinkungen
- [5D-Map](../5d-map/) - Interaktive Weltkarte
- [Manifest Summary](../../manifest_summary.md) - Projektübersicht
- [Main README](../../README.md) - Haupt-Dokumentation

### Navigation
```
5D Repository
├─ docs/
│  ├─ analysis/           # ⬅️ Sie sind hier
│  └─ 5d-map/            # Weltkarte
├─ manifest_summary.md
└─ README.md
```

## 👥 Verwendung

### Für Entwickler
1. Analysiere Repository-Struktur
2. Verstehe 5D-Methodologie
3. Implementiere Best Practices

### Für Researcher
1. Überblick über 5 Dimensionen
2. Wissenschaftliche Quellenangaben
3. Interdisziplinäre Integration

### Für Stakeholder
1. Projekt-Status visualisiert
2. Verbesserungspotenziale
3. Roadmap-Erkenntnisse

## 📝 Quellen

Basierend auf:
- PDF: "Eine tiefgehende Analyse des Projekts '5d'"
- [5D Methodology (Lancera)](https://lancera.com/5d-methodology/)
- [Domain-Driven Hexagon](https://github.com/Sairyss/domain-driven-hexagon)
- [DDD Repository Pattern](https://svatasimara.medium.com/domain-driven-design-part-5-repository-d5ad32b2e06f)

## ✅ Status

### Implementiert
- [x] Standalone HTML-Version
- [x] React-Komponenten-Struktur
- [x] Vite-Konfiguration
- [x] Dark Mode
- [x] Responsive Design

### In Arbeit
- [ ] Vollständige App.jsx
- [ ] package.json mit Dependencies
- [ ] Build & Deploy-Pipeline

### Geplant
- [ ] Englische Version
- [ ] PDF-Export
- [ ] Erweiterte Visualisierungen

## 🚀 Deployment

### GitHub Pages

```bash
# Standalone Version ist bereits einsatzbereit!
git checkout feature/interactive-analysis
cp docs/analysis/repository-standalone.html docs/analysis/index.html
git add .
git commit -m "deploy: Setup GitHub Pages"
git push
```

### Lokaler Server

```bash
# Python
python3 -m http.server 8080

# Node.js
npx serve docs/analysis

# PHP
php -S localhost:8080
```

## 🤝 Beitragen

1. Branch erstellen: `git checkout -b feature/analysis-improvement`
2. Änderungen committen: `git commit -m 'feat: Add improvement'`
3. Push: `git push origin feature/analysis-improvement`
4. Pull Request erstellen

## 💬 Feedback

Für Fragen oder Anregungen:
- [GitHub Issues](https://github.com/karlitos1337/5d/issues)
- [Diskussionen](https://github.com/karlitos1337/5d/discussions)

---

**Erstellt**: Dezember 2025  
**Status**: Beta  
**Lizenz**: Teil des 5D-Intelligence Framework
