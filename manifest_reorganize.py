#!/usr/bin/env python3
"""
5D Manifest Reorganizer - Sortiert Dateien thematisch nach Inhalt
Basiert auf PROJECT-PROMPT.md Prinzipien: Emergenz statt Kontrolle
"""

import os
import shutil
from pathlib import Path
import re

class ManifestOrganizer:
    def __init__(self, manifest_dir="manifest"):
        self.manifest_dir = Path(manifest_dir)
        
        # Thematische Kategorien mit Keywords
        self.categories = {
            "01_bildung_education": [
                "bildung", "schule", "education", "lernen", "learning", "student",
                "curriculum", "tokkatsu", "waldorf", "sudbury", "pilot", "dänemark",
                "japan", "university", "mental health"
            ],
            "02_neurobiologie_psychologie": [
                "neurobiologie", "polyvagal", "resilienz", "resilience", "cortisol",
                "dopamin", "nervensystem", "porges", "trauma", "mental", "psycho",
                "stress", "ventral", "vagal"
            ],
            "03_philosophie_epistemologie": [
                "wahrheit", "erkenntnis", "philosophie", "epistemologie", "authentizität",
                "authenticity", "selbst", "bewusstsein", "consciousness", "sinn",
                "spiritualität", "würde", "ethik", "freiheit"
            ],
            "04_oekonomie_governance": [
                "ökonomie", "dezentral", "partizipation", "governance", "kooperation",
                "netzwerk", "demokratie", "wirtschaft", "investment", "roi", "finanzierung",
                "selbstfinanzierend"
            ],
            "05_technologie_tesla": [
                "tesla", "patent", "transmission", "electrical", "energy", "apparatus",
                "signaling", "ki", "quantencomputer", "technologie", "automation"
            ],
            "06_synthesen_kompilationen": [
                "master", "kompilation", "mega", "synthese", "umfassend", "vollständig",
                "interkulturell", "best-practice", "extended", "final"
            ],
            "07_daten_analysen": [
                ".csv", ".json", "analysis", "validierung", "matrix", "chart", "data",
                "timeline", "projektion", "wahrscheinlichkeit", "szenario"
            ],
            "08_personal_biografie": [
                "mein", "zwanglos", "weg", "denkbiografie", "archaeologie", "persönlich",
                "beobachtung", "reflexion", "arletz", "pablö"
            ]
        }
        
    def categorize_file(self, filename):
        """Ermittelt Kategorie basierend auf Dateinamen und Inhalt"""
        filename_lower = filename.lower()
        
        # Dateiendung prüfen
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            return "07_daten_analysen"
        
        # Score für jede Kategorie berechnen
        scores = {}
        for category, keywords in self.categories.items():
            score = sum(1 for kw in keywords if kw in filename_lower)
            if score > 0:
                scores[category] = score
        
        # Höchste Score zurückgeben
        if scores:
            return max(scores, key=scores.get)
        
        return "99_unsortiert"
    
    def analyze_content(self, filepath):
        """Liest Textinhalt für bessere Kategorisierung (optional)"""
        try:
            if filepath.suffix in ['.md', '.txt']:
                content = filepath.read_text(encoding='utf-8', errors='ignore')[:5000]
                return content.lower()
        except:
            pass
        return ""
    
    def organize_subcategories(self, dry_run=True):
        """Sortiert Dateien in Unterkategorien"""
        subcategory_rules = {
            "01_bildung_education": {
                "kapitel": ["kapitel_"],
                "synthesen": ["mega", "extended"],
                "daten": [".csv", ".json"],
                "quellen": ["quellen", "top-25"]
            },
            "02_neurobiologie_psychologie": {
                "kapitel": ["kapitel_"],
                "anleitungen": ["anleitung", "training"]
            },
            "03_philosophie_epistemologie": {
                "kapitel": ["kapitel_"],
                "essays": ["paradox", "denkbiografie"]
            },
            "04_oekonomie_governance": {
                "kapitel": ["kapitel_"],
                "konzepte": ["prompt", "quantencomputer"]
            },
            "05_technologie_tesla": {
                "patente": [".pdf", "apparatus", "transmission", "signaling"],
                "ki_automation": ["ki_", "automation"],
                "notizen": [".txt", "tesla"]
            },
            "06_synthesen_kompilationen": {
                "master": ["master", "000-"],
                "mega": ["mega-"],
                "finale": ["final"],
                "strukturen": ["struktur", "schritt"]
            },
            "07_daten_analysen": {
                "csv": [".csv"],
                "visualisierungen": [".png"],
                "analysen": ["analysis", "validierung", "matrix"]
            },
            "08_personal_biografie": {
                "kapitel": ["kapitel_"],
                "reflexionen": ["reflexion", "mein_", "zwanglos"],
                "dokumente": [".pdf", ".docx", "arletz", "pablö"]
            }
        }
        
        for category_dir in self.manifest_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name not in subcategory_rules:
                continue
            
            files = [f for f in category_dir.iterdir() if f.is_file() and f.name != "INDEX.md"]
            rules = subcategory_rules[category_dir.name]
            
            for file in files:
                filename_lower = file.name.lower()
                
                # Finde passende Unterkategorie
                subcategory = None
                for subcat, keywords in rules.items():
                    if any(kw in filename_lower for kw in keywords):
                        subcategory = subcat
                        break
                
                if subcategory:
                    target = category_dir / subcategory / file.name
                    if dry_run:
                        print(f"   📄 {file.name} → {subcategory}/")
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(file), str(target))
                        print(f"   ✅ {file.name} → {category_dir.name}/{subcategory}/")
    
    def organize(self, dry_run=True):
        """Organisiert alle Manifest-Dateien thematisch"""
        files = [f for f in self.manifest_dir.iterdir() if f.is_file()]
        
        categorization = {}
        
        for file in files:
            # Systemdateien überspringen
            if file.name.startswith('.') or file.name == 'README.md':
                continue
            
            category = self.categorize_file(file.name)
            
            # Content-basierte Verfeinerung für unsortierte
            if category == "99_unsortiert":
                content = self.analyze_content(file)
                for cat, keywords in self.categories.items():
                    if any(kw in content for kw in keywords[:3]):  # Top 3 Keywords
                        category = cat
                        break
            
            if category not in categorization:
                categorization[category] = []
            categorization[category].append(file)
        
        # Ausgabe
        print("📂 5D MANIFEST ORGANISATION\n")
        for category in sorted(categorization.keys()):
            files = categorization[category]
            print(f"\n{'='*60}")
            print(f"📁 {category.replace('_', ' ').upper()}")
            print(f"{'='*60}")
            print(f"   {len(files)} Dateien\n")
            
            for file in sorted(files):
                target = self.manifest_dir / category / file.name
                
                if dry_run:
                    print(f"   📄 {file.name}")
                    print(f"      → {category}/")
                else:
                    # Tatsächlich verschieben
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), str(target))
                    print(f"   ✅ {file.name} → {category}/")
        
        print(f"\n{'='*60}")
        print(f"Gesamt: {sum(len(f) for f in categorization.values())} Dateien kategorisiert")
        
        if dry_run:
            print("\n⚠️  DRY RUN - Keine Dateien verschoben")
            print("Führe mit --execute aus zum tatsächlichen Verschieben")
    
    def create_index(self):
        """Erstellt INDEX.md für jede Kategorie"""
        for category in self.categories.keys():
            cat_dir = self.manifest_dir / category
            if not cat_dir.exists():
                continue
            
            files = sorted(cat_dir.glob("*"))
            if not files:
                continue
            
            index_content = f"# {category.replace('_', ' ').upper()}\n\n"
            index_content += "## Themen\n"
            index_content += ", ".join(self.categories[category][:10]) + "\n\n"
            index_content += "## Dateien\n\n"
            
            for file in files:
                if file.name != "INDEX.md":
                    size = file.stat().st_size
                    size_str = f"{size/1024:.1f}KB" if size < 1024*1024 else f"{size/(1024*1024):.1f}MB"
                    index_content += f"- [{file.name}](./{file.name}) ({size_str})\n"
            
            (cat_dir / "INDEX.md").write_text(index_content, encoding='utf-8')
            print(f"✅ INDEX.md erstellt: {category}")

if __name__ == "__main__":
    import sys
    
    organizer = ManifestOrganizer()
    
    # Dry Run oder Execute
    execute = "--execute" in sys.argv
    subcat = "--subcategories" in sys.argv
    
    if subcat:
        print("📂 5D UNTERKATEGORIEN ORGANISATION\n")
        organizer.organize_subcategories(dry_run=not execute)
        if execute:
            print("\n✅ Unterkategorien-Organisation abgeschlossen!")
    else:
        organizer.organize(dry_run=not execute)
        
        if execute:
            print("\n📝 Erstelle INDEX-Dateien...")
            organizer.create_index()
            print("\n✅ Organisation abgeschlossen!")
