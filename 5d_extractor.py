#!/usr/bin/env python3
"""
5D-EXTRACTOR: Zieht Lösungen aus allen Manifests
Autonomie × Motivation × Resilienz × Partizipation × Authentizität
"""

import re
import os
from pathlib import Path
from collections import defaultdict
import json
# ÄNDERUNG: Konfiguration und PDF-Extraktion
try:
    from config.loader import CONFIG, load_config
except Exception:
# ÄNDERUNG: Konfiguration, PDF und Fuzzy Matching
    CONFIG, load_config = None, None
try:
    import PyPDF2
    HAS_PDF = True
except Exception:
    HAS_PDF = False
# ÄNDERUNG: Pydantic-Validierung optional
try:
    from models.schemas import Solutions, Project, DimensionScore
    HAS_PYDANTIC = True
except Exception:
    HAS_PYDANTIC = False

class FiveDExtractor:
    def __init__(self, manifest_dir="manifest", extra_dirs=None, config_path: str | None = None):
try:
    from fuzzywuzzy import fuzz
    HAS_FUZZY = True
except Exception:
    HAS_FUZZY = False
        """Extractor für Kern-Manifest + optionale zusätzliche Pfade.

        extra_dirs: Liste zusätzlicher Verzeichnisse (z.B. ["external/system-genesis", "external/resonance-formulas"]).
        Diese werden rekursiv gescannt, aber NICHT in die Haupt-JSON gemischt – separater Merge empfohlen.
        """
        # Konfiguration laden
        cfg = None
        if config_path and load_config:
            try:
                cfg = load_config(config_path)
            except Exception:
                cfg = CONFIG
        else:
            cfg = CONFIG
        self.config = cfg or {
            'extractor': {
                'manifest_dir': manifest_dir or 'manifest',
                'output_file': '5d_solutions.json',
                'recursive': True,
                'file_types': ['*.md', '*.txt', '*.pdf'],
                'pdf_extraction': {'method': 'pypdf', 'max_pages': 50},
            }
        }
        self.manifest_dir = Path(self.config['extractor'].get('manifest_dir', manifest_dir))
        self.extra_dirs = [Path(p) for p in (extra_dirs or [])]
        self.imp_keywords = {
            'A': ['autonomie', 'freiheit', 'wahl', 'selbstbestimmung'],
            'IM': ['motivation', 'interesse', 'neugier', 'intrinsisch'],
            'R': ['resilienz', 'sicherheit', 'polyvagal', 'ventral'],
            'SP': ['partizipation', 'kooperation', 'netzwerk', 'tokkatsu'],
            'Au': ['authentizität', 'wahrheit', 'kongruenz', 'selbst']
        }
        
    def extract_text(self, file: Path) -> str:
        """Extrahiert Text aus .md/.txt/.pdf (PDF bis max_pages)."""
        suffix = file.suffix.lower()
        if suffix in {'.md', '.txt'}:
            try:
                return file.read_text(encoding='utf-8')
            except Exception:
                return file.read_text(errors='ignore')
        if suffix == '.pdf' and HAS_PDF:
            try:
                with file.open('rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    max_pages = int(self.config['extractor'].get('pdf_extraction', {}).get('max_pages', 50))
                    pages = reader.pages[:max_pages]
                    return '\n'.join((p.extract_text() or '') for p in pages)
            except Exception as e:
                print(f"⚠️ PDF-Fehler {file.name}: {e}")
                return ''
        return ''

    def load_manifests(self):
        """Lädt REKURSIV .md/.txt/.pdf aus Hauptmanifest + optionale extra_dirs."""
        texts = {}
        count = 0
        recursive = bool(self.config['extractor'].get('recursive', True))
        file_types = self.config['extractor'].get('file_types', ['*.md'])
        globber = self.manifest_dir.rglob if recursive else self.manifest_dir.glob
        for ext in file_types:
            for file in globber(ext):
                rel = str(file.relative_to(self.manifest_dir)) if file.is_relative_to(self.manifest_dir) else file.name
                texts[rel] = self.extract_text(file)
                count += 1
        for extra in self.extra_dirs:
            if extra.exists():
                for ext in file_types:
                    for file in (extra.rglob(ext) if recursive else extra.glob(ext)):
                        key = f"{extra.name}:{file.relative_to(extra)}"
                        texts[key] = self.extract_text(file)
                        count += 1
        print(f"✅ {count} Dateien geladen (inkl. extra_dirs, mit PDF-Unterstützung)")
        return texts
    
    def _extract_projects_regex(self, text: str):
        pattern = (self.config.get('patterns', {}) or {}).get('project')
        if not pattern:
            pattern = r'(Bäcker[ei]|Garten|Imker[ei]|Holz|Kräuter|Werkstatt)'
        return re.findall(pattern, text, re.I | re.DOTALL)

    def _extract_projects_fuzzy(self, text: str, threshold: int = 80):
        if not HAS_FUZZY:
            return []
        candidates = self._extract_projects_regex(text)
        unique = []
        for name in candidates:
            if not any(fuzz.ratio(str(name).lower(), str(u).lower()) > threshold for u in unique):
                unique.append(name)
        return unique

    def extract_solutions(self, texts):
        """Extrahiert konkrete Lösungen nach 5D (Regex + optional Fuzzy)."""
        solutions = defaultdict(list)

        inv_pat = (self.config.get('patterns', {}) or {}).get('investment', r'Investment.?([\d.,]+)')
        roi_pat = (self.config.get('patterns', {}) or {}).get('roi', r'ROI.?([\d]+)')
        pilots_pat = (self.config.get('patterns', {}) or {}).get('pilots', r'Pilot.?([\d]+)')

        for filename, text in texts.items():
            # Projekte
            proj_names = self._extract_projects_fuzzy(text) or self._extract_projects_regex(text)
            solutions['Projekte'].extend([str(p) for p in proj_names])

            # Investment/ROI/Pilots
            investments = re.findall(inv_pat, text, re.I | re.DOTALL)
            rois = re.findall(roi_pat, text, re.I | re.DOTALL)
            pilots = re.findall(pilots_pat, text, re.I | re.DOTALL)
            solutions['ROI'].extend(rois)
            solutions['Pilots'].extend(pilots)
            # Hinweis: Investments separat nutzen, aktuell kein Feld in Schema-Legacy

            # 5D-Keywords & Scores
            for dim, keywords in self.imp_keywords.items():
                if any(kw.lower() in text.lower() for kw in keywords):
                    score_match = re.search(rf'{dim}\s*[:\-]?\s*([\d.,]+)', text)
                    solutions[f'{dim}-Score'].append(score_match.group(1) if score_match else 'HIGH')

        return solutions

    def save_solutions_validated(self, raw_output: dict, filename: str = '5d_solutions.json') -> None:
        """Validiert & speichert via Pydantic; fällt zurück auf Raw-JSON bei Fehlern."""
        if not HAS_PYDANTIC:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(raw_output, f, indent=2, ensure_ascii=False)
            print(f"\n💾 {filename} gespeichert (ohne Pydantic-Validierung)")
            return
        solutions = raw_output.get('solutions', {})
        plan = raw_output.get('plan', {})
        # Projekte generieren
        projects_list = []
        for name in solutions.get('Projekte', []) or []:
            projects_list.append(Project(name=name))
        # ROI/Pilots
        roi_vals = solutions.get('ROI', []) or []
        pilots_vals = solutions.get('Pilots', []) or []
        for i, p in enumerate(projects_list):
            if i < len(roi_vals):
                p.roi = roi_vals[i]
            if i < len(pilots_vals):
                p.pilots = pilots_vals[i]
        # Investment: nur zuordnen, wenn Längen passen
        inv_vals = solutions.get('Investment', []) or []
        if inv_vals and len(inv_vals) == len(projects_list):
            for i, p in enumerate(projects_list):
                p.investment = inv_vals[i]
        # DimensionScores
        dim_scores = []
        for dim in ['A', 'IM', 'R', 'SP', 'Au']:
            for raw in solutions.get(f'{dim}-Score', []) or []:
                dim_scores.append(DimensionScore(dimension=dim, score=raw, source='manifest'))
        validated = Solutions(projects=projects_list, dimension_scores=dim_scores, plan=plan)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(validated.dict(), f, indent=2, ensure_ascii=False)
        print(f"\n💾 {filename} gespeichert (Pydantic-validiert)")
    
    def generate_action_plan(self, solutions):
        """Generiert NEXT STEPS"""
        plan = {
            'Phase1': '10 Pilot-Schulen (50 Mio €)',
            'Phase2': '500 Netzwerk (Gewinne skalieren)',
            'Phase3': '10k selbstfinanziert (Export Polen/RO)',
            'Phase4': '100k global (Kaskade)'
        }
        
        imp_score = 0.77  # Dein Modell
        print(f"🎯 IMP-SCORE: {imp_score} (25% > Dänemark!)")
        return plan
    
    def run(self):
        """Hauptprogramm"""
        print("🚀 5D-EXTRACTOR START")
        texts = self.load_manifests()
        solutions = self.extract_solutions(texts)
        plan = self.generate_action_plan(solutions)
        
        # OUTPUT
        print("\n📊 GEFUNDENE LÖSUNGEN:")
        for category, items in solutions.items():
            print(f"  {category}: {list(set(items))[:3]}...")  # Top 3
        
        print("\n🎯 ACTION PLAN:")
        for phase, action in plan.items():
            print(f"  {phase}: {action}")
        
        # JSON Export (validiert wenn möglich)
        output = {'solutions': solutions, 'plan': plan}
        try:
            self.save_solutions_validated(output, filename='5d_solutions.json')
        except Exception as e:
            with open('5d_solutions.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"\n💾 5d_solutions.json gespeichert (Raw-Fallback: {e})")

if __name__ == "__main__":
    extractor = FiveDExtractor()
    extractor.run()
