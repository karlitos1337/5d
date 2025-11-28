from __future__ import annotations

"""
Validated schemas for 5D solutions output.
- Ensures type-safety and normalization
- Deduplicates projects
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from enum import Enum


class DimensionEnum(str, Enum):
    A = "A"
    IM = "IM"
    R = "R"
    SP = "SP"
    Au = "Au"


class DimensionScore(BaseModel):
    """Validiertes 5D-Score-Schema"""
    dimension: DimensionEnum = Field(..., description="Dimension: A|IM|R|SP|Au")
    score: float = Field(..., ge=0.0, le=1.0, description="0–1 normalisiert")
    source: str = Field(..., description="Manifest-Dateiname")

    @validator('score', pre=True)
    def parse_score(cls, v):
        """Konvertiert 'HIGH', 'A,' etc. zu numerisch."""
        if isinstance(v, str):
            s = v.strip()
            if s.upper() == 'HIGH':
                return 0.75
            import re
            m = re.search(r'(\d+\.\d+|\d+)', s.replace(',', '.'))
            return float(m.group(1)) if m else 0.5
        try:
            return float(v)
        except Exception:
            return 0.5


class Project(BaseModel):
    """Projekt mit Investment/ROI"""
    name: str
    investment: Optional[float] = None
    roi: Optional[float] = None
    pilots: Optional[int] = None

    @validator('name', pre=True)
    def normalize_name(cls, v):
        """Normalisiert Projektnamen (Umlaute/Trimmen/Kapitalisierung)."""
        s = str(v or "").strip().title()
        # Häufige Tippfehler-Korrektur
        s = s.replace('Bäckere', 'Bäckerei').replace('BäckereI', 'Bäckerei')
        return s

    @validator('investment', 'roi', pre=True)
    def parse_numbers(cls, v):
        """Parst numerische Felder robust (komma → punkt, Prozent entfernen)."""
        if v is None:
            return None
        try:
            if isinstance(v, str):
                s = v.strip().replace('%', '').replace(',', '.')
                import re
                m = re.search(r'(\d+\.\d+|\d+)', s)
                return float(m.group(1)) if m else None
            return float(v)
        except Exception:
            return None

    @validator('pilots', pre=True)
    def parse_int(cls, v):
        """Parst Pilots als int."""
        if v is None:
            return None
        try:
            if isinstance(v, str):
                import re
                m = re.search(r'(\d+)', v)
                return int(m.group(1)) if m else None
            return int(v)
        except Exception:
            return None


class Solutions(BaseModel):
    """Gesamtes Solutions-Schema"""
    projects: List[Project] = []
    dimension_scores: List[DimensionScore] = []
    plan: Dict

    @validator('projects')
    def deduplicate_projects(cls, v: List[Project]):
        """Entfernt Duplikate, behält Einträge mit mehr Daten (z. B. Investment/ROI)."""
        seen: Dict[str, Project] = {}
        for proj in v:
            key = proj.name.lower()
            existing = seen.get(key)
            if not existing:
                seen[key] = proj
            else:
                def richness(p: Project) -> int:
                    return sum(x is not None for x in [p.investment, p.roi, p.pilots])
                if richness(proj) > richness(existing):
                    seen[key] = proj
        return list(seen.values())
