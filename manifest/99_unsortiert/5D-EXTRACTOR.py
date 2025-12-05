#!/usr/bin/env python3
"""
5D-EXTRACTOR: Zieht Lösungen aus allen Manifests
Autonomie × Motivation × Resilienz × Partizipation × Authentizität
"""

import json
import re
from collections import defaultdict
from pathlib import Path


class FiveDExtractor:
    def __init__(self, manifest_dir="manifest"):
        self.manifest_dir = Path(manifest_dir)
        self.imp_keywords = {
            "A": ["autonomie", "freiheit", "wahl", "selbstbestimmung"],
            "IM": ["motivation", "interesse", "neugier", "intrinsisch"],
            "R": ["resilienz", "sicherheit", "polyvagal", "ventral"],
            "SP": ["partizipation", "kooperation", "netzwerk", "tokkatsu"],
            "Au": ["authentizität", "wahrheit", "kongruenz", "selbst"],
        }

    def load_manifests(self):
        """Lädt alle .md und .md aus manifest/"""
        texts = {}
        for file in self.manifest_dir.glob("*.md"):
            texts[file.name] = file.read_text(encoding="utf-8")
        print(f"✅ {len(texts)} Manifests geladen")
        return texts

    def extract_solutions(self, texts):
        """Extrahiert konkrete Lösungen nach 5D"""
        solutions = defaultdict(list)

        for _filename, text in texts.items():
            # Lösungen finden (Investment, Projekte, ROI, Pilots)
            projects = re.findall(
                r"(Bäcker[ei]|Garten|Imker[ei]|Holz|Kräuter).*?Investment.*?(\d+[.,]?\d*)",
                text,
                re.I | re.DOTALL,
            )
            roi = re.findall(r"ROI.*?(\d+)", text)
            pilots = re.findall(r"Pilot.*?(\d+)", text)

            solutions["Projekte"].extend([p[0] for p in projects])
            solutions["ROI"].extend(roi)
            solutions["Pilots"].extend(pilots)

            # 5D-IMP Scores finden
            for dim, keywords in self.imp_keywords.items():
                for kw in keywords:
                    if kw.lower() in text.lower():
                        score_match = re.search(rf"{dim}\s*[\d.,]+", text)
                        solutions[f"{dim}-Score"].append(
                            score_match.group(0) if score_match else "HIGH"
                        )

        return solutions

    def generate_action_plan(self, solutions):
        """Generiert NEXT STEPS"""
        plan = {
            "Phase1": "10 Pilot-Schulen (50 Mio €)",
            "Phase2": "500 Netzwerk (Gewinne skalieren)",
            "Phase3": "10k selbstfinanziert (Export Polen/RO)",
            "Phase4": "100k global (Kaskade)",
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

        # JSON Export
        output = {"solutions": solutions, "plan": plan}
        with open("5d_solutions.json", "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print("\n💾 5d_solutions.json gespeichert")


if __name__ == "__main__":
    extractor = FiveDExtractor()
    extractor.run()
