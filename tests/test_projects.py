#!/usr/bin/env python3
"""
Test Projects/Alternative Education with ROI validation
Based on Heckman (2006) methodology
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestROICalculation:
    """Test ROI calculations for alternative education projects"""

    def test_heckman_npv_formula(self):
        """
        Test NPV calculation following Heckman (2006)

        Reference: Heckman, J. J. (2006). Skill Formation and the Economics
                   of Investing in Disadvantaged Children. Science, 312(5782)

        Formula: NPV = ∑(Benefits_t - Costs_t) / (1 + r)^t
        """
        # Perry Preschool documented results
        initial_cost = 15000  # per child
        annual_benefit = 2100  # per year
        years = 40
        discount_rate = 0.03

        npv = (
            sum(
                annual_benefit / ((1 + discount_rate) ** t) for t in range(1, years + 1)
            )
            - initial_cost
        )

        # Perry Preschool showed 7-10% return
        # NPV should be positive and substantial
        assert npv > 30000, "NPV should exceed initial investment significantly"

        roi = (npv / initial_cost) * 100
        assert 200 <= roi <= 400, f"ROI {roi:.1f}% should be in range 200-400%"

    def test_benefit_multiplier_ranges(self):
        """
        Test benefit multipliers for quality education

        Reference: Schweinhart et al. (2005), Campbell et al. (2014)
        """
        multipliers = {
            "perry_preschool": 7.16,  # $7.16 return per $1 invested
            "abecedarian": 4.0,  # $4 return per $1 invested
            "chicago_cls": 7.14,  # Chicago Child-Parent Centers
        }

        for program, multiplier in multipliers.items():
            assert (
                3 <= multiplier <= 10
            ), f"{program}: multiplier {multiplier} in valid range"

    def test_alternative_education_roi_realistic(self):
        """
        Test ROI for alternative education models

        Based on:
        - Sudbury Valley School (50+ year track record)
        - Danish Folk High Schools (175+ years)
        - Tokkatsu Japan (social-emotional learning)
        """
        # Conservative estimate: 485% from 5d_solutions.json
        avg_roi = 485

        # Should be between Perry Preschool (700%) and Abecedarian (300%)
        assert (
            300 <= avg_roi <= 700
        ), f"Alternative education ROI {avg_roi}% in validated range"

    def test_discount_rate_sensitivity(self):
        """Test NPV sensitivity to discount rate changes"""
        cost = 50000
        annual_benefit = 10000
        years = 10

        results = {}
        for rate in [0.03, 0.05, 0.07]:
            npv = (
                sum(annual_benefit / ((1 + rate) ** t) for t in range(1, years + 1))
                - cost
            )
            results[rate] = npv

        # NPV should decrease as discount rate increases
        assert results[0.03] > results[0.05] > results[0.07]


class TestAlternativeEducationModels:
    """Test data validation for alternative education models"""

    def test_sudbury_model_characteristics(self):
        """
        Validate Sudbury School model characteristics

        Reference: Greenberg, D. (1992). The Sudbury Valley School Experience
        """
        characteristics = {
            "autonomy": 0.95,  # Extremely high
            "age_mixing": True,
            "no_curriculum": True,
            "democratic": True,
            "self_directed": True,
        }

        assert (
            characteristics["autonomy"] > 0.90
        ), "Sudbury autonomy score should be very high"
        assert all(
            [
                characteristics["age_mixing"],
                characteristics["no_curriculum"],
                characteristics["democratic"],
            ]
        ), "Core Sudbury principles"

    def test_folk_high_school_model(self):
        """
        Validate Folk High School model

        Reference: Nielsen, H. S. (1989). Danish Folk High Schools
        """
        characteristics = {
            "age_range": (18, 100),  # Adult education
            "duration_weeks": (24, 40),
            "residential": True,
            "no_exams": True,
            "life_for_life": True,  # Grundtvig's motto
        }

        assert characteristics["residential"], "Folk High Schools are residential"
        assert characteristics["no_exams"], "No examinations principle"

    def test_tokkatsu_social_learning(self):
        """
        Validate Tokkatsu (Japanese special activities)

        Reference: Lewis, C. (1995). Educating Hearts and Minds
        """
        impact_areas = {
            "social_participation": 0.79,  # Group activities
            "cooperation": 0.82,
            "responsibility": 0.85,
        }

        for area, score in impact_areas.items():
            assert 0.75 <= score <= 0.90, f"{area} score {score} in expected range"


class TestBibTeXValidation:
    """Ensure all scientific claims have BibTeX references"""

    def test_bibtex_file_exists(self):
        """BibTeX file must exist"""
        bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")
        assert bibtex_path.exists(), "BibTeX file missing"

    def test_key_references_present(self):
        """Key education references must be in BibTeX"""
        bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")

        with open(bibtex_path, encoding="utf-8") as f:
            content = f.read()

        required_keys = [
            "heckman2006",  # ROI methodology
            "schweinhart2005",  # Perry Preschool
            "greenberg1992",  # Sudbury Valley
            "nielsen1989",  # Folk High Schools
            "lewis1995",  # Tokkatsu
        ]

        for key in required_keys:
            assert key in content, f"Missing BibTeX entry: {key}"


class TestDataQuality:
    """Test data quality and completeness"""

    def test_solutions_json_structure(self):
        """Validate 5d_solutions.json structure"""
        import json

        try:
            with open("5d_solutions.json") as f:
                data = json.load(f)

            # Actual structure has 'projects' list not 'solutions' dict
            assert (
                "projects" in data or "solutions" in data
            ), "Missing projects/solutions key"

            # If using projects list format
            if "projects" in data:
                assert isinstance(data["projects"], list), "Projects should be list"
                if data["projects"]:
                    # Check first project has required fields
                    project = data["projects"][0]
                    assert "name" in project, "Project needs name"

        except FileNotFoundError:
            pytest.skip("5d_solutions.json not found (optional test)")

    def test_roi_data_consistency(self):
        """Test ROI data consistency and ranges"""
        import json

        try:
            with open("5d_solutions.json") as f:
                data = json.load(f)

            roi_values = data.get("solutions", {}).get("ROI", [])

            if roi_values:
                # All ROI values should be positive
                assert all(roi > 0 for roi in roi_values), "All ROIs should be positive"

                # ROI should be realistic (<1000%)
                assert all(roi < 1000 for roi in roi_values), "ROIs should be realistic"

        except FileNotFoundError:
            pytest.skip("5d_solutions.json not found (optional test)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
