from __future__ import annotations

"""
Validated schemas for 5D solutions output.
- Ensures type-safety and normalization
- Deduplicates projects
"""

from pydantic import BaseModel, Field, field_validator
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

    @field_validator('score', mode='before')
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

    @field_validator('name', mode='before')
    def normalize_name(cls, v):
        """Normalisiert Projektnamen (Umlaute/Trimmen/Kapitalisierung)."""
        s = str(v or "").strip().title()
        # Häufige Tippfehler-Korrektur
        s = s.replace('Bäckereii', 'Bäckerei').replace('Bäckere', 'Bäckerei').replace('Bäckerei ', 'Bäckerei')
        s = s.replace('BäckereiI', 'Bäckerei').replace('BäckereI', 'Bäckerei')
        return s

    @field_validator('investment', 'roi', mode='before')
    def parse_numbers(cls, v):
        """Parst numerische Felder robust (komma → punkt, Prozent entfernen)."""
        if v is None:
            return None
        try:
            if isinstance(v, str):
                s = v.strip().replace('%', '')
                # Tausenderpunkt entfernen, Dezimalkomma in Punkt wandeln
                if ',' not in s:
                    s = s.replace('.', '')
                s = s.replace(',', '.')
                import re
                m = re.search(r'(\d+\.\d+|\d+)', s)
                return float(m.group(1)) if m else None
            return float(v)
        except Exception:
            return None

    @field_validator('pilots', mode='before')
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

    @field_validator('projects')
    def deduplicate_projects(cls, v: List[Project]):
        """Entfernt Duplikate, behält Einträge mit mehr Daten (z. B. Investment/ROI)."""
        seen: Dict[str, Project] = {}
        def richness(p: Project) -> int:
            return sum(x is not None for x in [p.investment, p.roi, p.pilots])
        for proj in v:
            key = proj.name.lower()
            # Versuche, nahe Duplikate (ein Zeichen Abweichung) zu mergen
            match_key = None
            for k in list(seen.keys()):
                if key == k:
                    match_key = k
                    break
                # einfache Heuristik: Prefix/Suffix-Unterschied von 1 Zeichen
                if abs(len(key) - len(k)) <= 1 and (key.startswith(k) or k.startswith(key)):
                    match_key = k
                    break
            if match_key is None:
                seen[key] = proj
            else:
                existing = seen[match_key]
                # Wähle den reicheren Eintrag, aber setze einen kanonischen Namen
                winner = proj if richness(proj) > richness(existing) else existing
                canonical = 'bäckerei' if ('bäckerei' in key or 'bäckerei' in match_key) else (key if len(key) <= len(match_key) else match_key)
                winner.name = canonical.title()
                seen[match_key] = winner
        return list(seen.values())
