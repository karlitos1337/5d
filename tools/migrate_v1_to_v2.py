#!/usr/bin/env python3
"""
Migriert 5d_solutions.json v1 → v2 (Pydantic-Schema)
"""

import json
from pathlib import Path
from datetime import datetime

try:
    from models.schemas import Solutions, Project, DimensionScore
except Exception as e:
    print(f"Pydantic-Schema fehlt: {e}")
    Solutions = None


def migrate_v1_to_v2(old_file='5d_solutions.json', new_file='5d_solutions.json'):
    """Migriert altes Format zu neuem Pydantic-Schema."""
    p = Path(old_file)
    if not p.exists():
        print("❌ 5d_solutions.json nicht gefunden!")
        return
    old_data = json.loads(p.read_text(encoding='utf-8'))

    # Projekte konvertieren
    projects = []
    proj_names = old_data.get('solutions', {}).get('Projekte', [])
    roi_values = old_data.get('solutions', {}).get('ROI', [])
    pilot_values = old_data.get('solutions', {}).get('Pilots', [])

    for i, name in enumerate(proj_names):
        roi = roi_values[i] if i < len(roi_values) else None
        pilots = pilot_values[i] if i < len(pilot_values) else None
        projects.append(Project(name=name, investment=None, roi=roi, pilots=pilots))

    # Dimension Scores konvertieren
    dimension_scores = []
    for dim in ['A', 'IM', 'R', 'SP', 'Au']:
        scores = old_data.get('solutions', {}).get(f'{dim}-Score', [])
        for i, score in enumerate(scores):
            dimension_scores.append(DimensionScore(dimension=dim, score=score, source='legacy'))

    # Plan übernehmen
    plan = old_data.get('plan', {})

    # Validieren mit Pydantic
    if Solutions is not None:
        validated = Solutions(projects=projects, dimension_scores=dimension_scores, plan=plan,)
        Path(new_file).write_text(json.dumps(validated.dict(), indent=2, ensure_ascii=False), encoding='utf-8')
    else:
        Path(new_file).write_text(json.dumps({'projects': [p.__dict__ for p in projects], 'dimension_scores': [s.__dict__ for s in dimension_scores], 'plan': plan}, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"✅ Migration abgeschlossen: {old_file} → {new_file}")
    print(f"   Projekte: {len(proj_names)} → {len(projects)} (vor Dedup)")
    print(f"   Scores: {len(dimension_scores)}")


if __name__ == "__main__":
    migrate_v1_to_v2()
