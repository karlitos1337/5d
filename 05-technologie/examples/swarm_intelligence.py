"""
Swarm Intelligence: Honeybee Democracy Simulation
Reference: Seeley 2010, ISBN:978-0691149125
"""
from dataclasses import dataclass
from typing import List
import random

@dataclass
class NestSite:
    """Represents a potential nesting site with quality metric."""
    quality: float  # 0-1 scale
    votes: int = 0

class SwarmDecisionMaker:
    """Dezentrale Entscheidungsfindung ohne zentrale Kontrolle.
    
    Based on honeybee nest-site selection where scouts communicate
    site quality through waggle dance intensity.
    """
    
    def __init__(self, sites: List[NestSite], scouts: int = 100):
        self.sites = sites
        self.scouts = scouts
    
    def vote(self) -> NestSite:
        """Scouts tanzen proportional zur Qualität.
        
        Returns:
            Best site chosen by emergent consensus
        """
        for _ in range(self.scouts):
            # Wahrscheinlichkeit ∝ Qualität
            weights = [s.quality for s in self.sites]
            chosen = random.choices(self.sites, weights=weights)[0]
            chosen.votes += 1
        
        return max(self.sites, key=lambda s: s.votes)

# Example Usage
if __name__ == "__main__":
    sites = [
        NestSite(quality=0.3),
        NestSite(quality=0.9),
        NestSite(quality=0.5)
    ]
    swarm = SwarmDecisionMaker(sites)
    best = swarm.vote()
    print(f"Gewählter Nistplatz: Qualität={best.quality}, Stimmen={best.votes}")
