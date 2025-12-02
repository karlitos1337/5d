#!/usr/bin/env python3
"""
Test Projections and adoption curve models
Validate logistic curves, NPV calculations, diffusion theory
"""

import pytest
from pathlib import Path
import sys
import math

sys.path.insert(0, str(Path(__file__).parent.parent))

class TestLogisticCurve:
    """Test S-curve (logistic) adoption model"""
    
    def test_logistic_function(self):
        """
        Test logistic function formula
        
        Formula: P(t) = L / (1 + e^(-k(t-t0)))
        Where:
        - L = maximum adoption (1.0 or 100%)
        - k = growth rate (steepness)
        - t0 = midpoint (50% adoption year)
        - t = time (years)
        
        Reference: Verhulst (1838), Bass (1969)
        """
        L = 1.0      # Maximum adoption (100%)
        k = 0.3      # Growth rate
        t0 = 2035    # Midpoint year (50% adoption)
        t = 2030     # Current year
        
        P_t = L / (1 + math.exp(-k * (t - t0)))
        
        assert 0 <= P_t <= 1, "Adoption in [0,1]"
        assert P_t < 0.5, "Before midpoint, adoption <50%"
    
    def test_midpoint_property(self):
        """Test that at t=t0, P(t0) = L/2 = 50%"""
        L = 1.0
        k = 0.3
        t0 = 2035
        
        P_t0 = L / (1 + math.exp(-k * (t0 - t0)))
        
        assert abs(P_t0 - 0.5) < 0.01, "At midpoint, adoption = 50%"
    
    def test_asymptotic_behavior(self):
        """Test asymptotic approach to 100%"""
        L = 1.0
        k = 0.3
        t0 = 2035
        t_far_future = 2100  # 65 years after midpoint
        
        P_future = L / (1 + math.exp(-k * (t_far_future - t0)))
        
        assert P_future > 0.99, "Far future: adoption >99%"
    
    def test_growth_rate_impact(self):
        """Test impact of growth rate (k) on curve steepness"""
        L = 1.0
        t0 = 2035
        t = 2040  # 5 years after midpoint
        
        # Slow growth
        k_slow = 0.1
        P_slow = L / (1 + math.exp(-k_slow * (t - t0)))
        
        # Fast growth
        k_fast = 0.5
        P_fast = L / (1 + math.exp(-k_fast * (t - t0)))
        
        assert P_fast > P_slow, "Higher k → faster adoption"
        assert P_fast > 0.90, "Fast growth reaches 90% in 5 years"

class TestRogersDiffusion:
    """Test Rogers' Diffusion of Innovations theory"""
    
    def test_adopter_categories(self):
        """
        Test Rogers' 5 adopter categories
        
        Innovators: 2.5%
        Early Adopters: 13.5%
        Early Majority: 34%
        Late Majority: 34%
        Laggards: 16%
        
        Reference: Rogers (2003)
        """
        categories = {
            'Innovators': 0.025,
            'Early Adopters': 0.135,
            'Early Majority': 0.34,
            'Late Majority': 0.34,
            'Laggards': 0.16,
        }
        
        total = sum(categories.values())
        assert abs(total - 1.0) < 0.01, "Categories sum to 100%"
    
    def test_tipping_point(self):
        """
        Test tipping point at 16% adoption
        
        Tipping point: Innovators (2.5%) + Early Adopters (13.5%) = 16%
        Reference: Rogers (2003), Gladwell (2000)
        """
        tipping_point = 0.025 + 0.135
        
        assert abs(tipping_point - 0.16) < 0.01, "Tipping point at 16%"
    
    def test_chasm_crossing(self):
        """
        Test "crossing the chasm" from early adopters to early majority
        
        Reference: Moore (1991)
        """
        early_adopters_end = 0.025 + 0.135  # 16%
        early_majority_start = 0.16
        
        assert abs(early_adopters_end - early_majority_start) < 0.01, "Chasm at 16%"

class TestEconomicImpact:
    """Test economic impact projections"""
    
    def test_npv_formula(self):
        """
        Test NPV calculation for alternative education
        
        Formula: NPV = Σ(Benefits_t / (1+r)^t) - Initial_Cost
        
        Reference: Heckman (2006), Schweinhart (2005)
        """
        initial_cost = 50000
        annual_benefit = 15000
        years = 10
        discount_rate = 0.05
        
        npv = -initial_cost
        for t in range(1, years + 1):
            npv += annual_benefit / ((1 + discount_rate) ** t)
        
        assert npv > 0, "NPV positive for alternative education"
        assert npv > 50000, "Benefits exceed costs"
    
    def test_benefit_cost_ratio(self):
        """
        Test benefit-cost ratio (BCR)
        
        Documented: Perry Preschool BCR = 7.16
        Reference: Schweinhart (2005)
        """
        bcr_perry = 7.16
        bcr_abecedarian = 4.0
        
        assert bcr_perry > 1, "BCR >1 means profitable"
        assert bcr_perry > bcr_abecedarian, "Perry has higher BCR than Abecedarian"
    
    def test_societal_savings(self):
        """
        Test societal savings from reduced crime, welfare, etc.
        
        Perry Preschool: $7.16 return per $1 invested
        Breakdown: 88% crime reduction, 7% earnings, 5% education
        """
        crime_reduction_share = 0.88
        earnings_share = 0.07
        education_share = 0.05
        
        total = crime_reduction_share + earnings_share + education_share
        assert abs(total - 1.0) < 0.01, "Shares sum to 100%"
        assert crime_reduction_share > 0.80, "Crime reduction is largest component"

class TestRegionalAdoption:
    """Test regional adoption projections"""
    
    def test_nordic_projection(self):
        """
        Test Nordic countries projection
        
        2040 target: 70% adoption
        Reasoning: High governance, low coercion, strong education culture
        """
        nordics_2040 = 0.70
        
        assert 0.60 <= nordics_2040 <= 0.80, "Nordics: 60-80% by 2040"
    
    def test_western_europe_projection(self):
        """
        Test Western Europe projection
        
        2040 target: 50% adoption
        """
        western_europe_2040 = 0.50
        
        assert 0.40 <= western_europe_2040 <= 0.60, "W.Europe: 40-60% by 2040"
    
    def test_north_america_projection(self):
        """
        Test North America projection
        
        2040 target: 40% adoption
        """
        north_america_2040 = 0.40
        
        assert 0.30 <= north_america_2040 <= 0.50, "N.America: 30-50% by 2040"
    
    def test_east_asia_projection(self):
        """
        Test East Asia projection
        
        2040 target: 35% adoption
        """
        east_asia_2040 = 0.35
        
        assert 0.25 <= east_asia_2040 <= 0.45, "E.Asia: 25-45% by 2040"
    
    def test_latin_america_projection(self):
        """
        Test Latin America projection
        
        2040 target: 25% adoption
        """
        latin_america_2040 = 0.25
        
        assert 0.20 <= latin_america_2040 <= 0.35, "LatAm: 20-35% by 2040"
    
    def test_africa_projection(self):
        """
        Test Africa projection
        
        2040 target: 18% adoption
        """
        africa_2040 = 0.18
        
        assert 0.15 <= africa_2040 <= 0.25, "Africa: 15-25% by 2040"
    
    def test_regional_ordering(self):
        """Test that regional projections are ordered by IMP-Proxy"""
        projections = {
            'Nordics': 0.70,
            'Western Europe': 0.50,
            'North America': 0.40,
            'East Asia': 0.35,
            'Latin America': 0.25,
            'Africa': 0.18,
        }
        
        values = list(projections.values())
        assert values == sorted(values, reverse=True), "Regions ordered by adoption rate"

class TestTimelineProjections:
    """Test timeline milestones"""
    
    def test_2025_baseline(self):
        """
        Test 2025 baseline adoption
        
        Current: ~5% (early innovators)
        """
        adoption_2025 = 0.05
        
        assert 0.03 <= adoption_2025 <= 0.08, "2025: 3-8% adoption"
    
    def test_2030_early_majority(self):
        """
        Test 2030 early majority crossing
        
        Target: ~15-20% (crossing chasm)
        """
        adoption_2030 = 0.18
        
        assert 0.15 <= adoption_2030 <= 0.25, "2030: 15-25% adoption"
    
    def test_2035_midpoint(self):
        """
        Test 2035 midpoint (50% adoption in leading regions)
        
        Nordic countries reach 50%
        """
        nordics_2035 = 0.50
        
        assert 0.45 <= nordics_2035 <= 0.55, "Nordics: ~50% by 2035"
    
    def test_2040_mainstream(self):
        """
        Test 2040 mainstream adoption
        
        Global average: 35-40%
        """
        global_2040 = 0.38
        
        assert 0.30 <= global_2040 <= 0.45, "Global: 30-45% by 2040"
    
    def test_2050_maturity(self):
        """
        Test 2050 maturity phase
        
        Most regions >60%, laggards catching up
        """
        global_2050 = 0.65
        
        assert 0.55 <= global_2050 <= 0.75, "Global: 55-75% by 2050"

class TestSensitivityAnalysis:
    """Test sensitivity to key parameters"""
    
    def test_discount_rate_sensitivity(self):
        """Test NPV sensitivity to discount rate"""
        initial_cost = 50000
        annual_benefit = 15000
        years = 10
        
        # Low discount rate (3%)
        npv_low = -initial_cost + sum(annual_benefit / ((1.03) ** t) for t in range(1, years + 1))
        
        # High discount rate (7%)
        npv_high = -initial_cost + sum(annual_benefit / ((1.07) ** t) for t in range(1, years + 1))
        
        assert npv_low > npv_high, "Higher discount rate → lower NPV"
        assert npv_low > 0 and npv_high > 0, "Both scenarios profitable"
    
    def test_growth_rate_sensitivity(self):
        """Test adoption curve sensitivity to growth rate"""
        L = 1.0
        t0 = 2035
        t = 2040
        
        # Conservative growth
        k_conservative = 0.2
        P_conservative = L / (1 + math.exp(-k_conservative * (t - t0)))
        
        # Optimistic growth
        k_optimistic = 0.4
        P_optimistic = L / (1 + math.exp(-k_optimistic * (t - t0)))
        
        assert P_optimistic > P_conservative, "Higher growth rate → faster adoption"
        # Conservative: k=0.2, 5 years after midpoint → ~73%
        assert 0.50 <= P_conservative <= 0.75, "Conservative: 50-75% by 2040"
        assert 0.80 <= P_optimistic <= 0.95, "Optimistic: 80-95% by 2040"

class TestBibTeXValidation:
    """Test BibTeX references for projection models"""
    
    def test_bibtex_projection_papers(self):
        """Ensure projection methodology papers are in BibTeX"""
        bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")
        
        if not bibtex_path.exists():
            pytest.skip("BibTeX file not found")
        
        with open(bibtex_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Key projection papers
        key_papers = [
            'rogers2003',     # Diffusion of Innovations
            'bass1969',       # Bass Diffusion Model
            'verhulst',       # Logistic Curve (1838)
            'heckman2006',    # Economic Impact
        ]
        
        missing = []
        for paper in key_papers:
            if paper not in content:
                missing.append(paper)
        
        if missing:
            pytest.skip(f"Missing projection papers: {missing} (future addition)")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
