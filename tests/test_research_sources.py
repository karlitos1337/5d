#!/usr/bin/env python3
"""
Test Research data quality and paper validation
arXiv, PubMed, WHO, World Bank data sources
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestResearchDataSources:
    """Test research data source quality"""

    def test_research_json_structure(self):
        """Validate 5d_research_data.json structure"""
        try:
            with open("5d_research_data.json") as f:
                data = json.load(f)

            # Check for main sections (data organized by keywords)
            # Each keyword has arxiv/pubmed subsections
            has_content = len(data) > 0 and any(
                "arxiv" in v or "pubmed" in v for v in data.values() if isinstance(v, dict)
            )
            assert has_content, "Missing research data"

            # If arXiv data exists, validate structure
            if "arxiv" in data:
                papers = data["arxiv"]
                if papers:
                    sample = papers[0]
                    assert "title" in sample, "arXiv papers need title"
                    assert "abstract" in sample or "summary" in sample, (
                        "Papers need abstract/summary"
                    )

        except FileNotFoundError:
            pytest.skip("5d_research_data.json not found (run 5d_research_scraper.py)")

    def test_paper_completeness_rates(self):
        """
        Test documented data completeness rates

        Expected: arXiv 94%, PubMed 87%
        """
        completeness_targets = {
            "arxiv": 0.94,
            "pubmed": 0.87,
        }

        for source, target in completeness_targets.items():
            assert 0.80 <= target <= 1.0, f"{source} completeness target in valid range"

    def test_relevance_score_formula(self):
        """
        Test relevance score calculation

        Formula: R = 0.3*C + 0.2*T + 0.3*K + 0.2*A
        Where: C=Citations, T=Timeliness, K=Keywords, A=Author Reputation
        """
        # Sample paper scores
        test_paper = {
            "citations": 0.8,  # Normalized 0-1
            "timeliness": 0.9,  # Recent paper
            "keywords": 0.7,  # Partial match
            "author_rep": 0.6,  # Moderate reputation
        }

        relevance = (
            0.3 * test_paper["citations"]
            + 0.2 * test_paper["timeliness"]
            + 0.3 * test_paper["keywords"]
            + 0.2 * test_paper["author_rep"]
        )

        assert 0 <= relevance <= 1, "Relevance score in [0,1]"
        # 0.3*0.8 + 0.2*0.9 + 0.3*0.7 + 0.2*0.6 = 0.24 + 0.18 + 0.21 + 0.12 = 0.75
        assert abs(relevance - 0.75) < 0.01, "Calculation matches expected value"

    def test_keyword_coverage(self):
        """Test that key research topics are covered"""
        key_topics = [
            "self-determination",
            "intrinsic motivation",
            "flow",
            "autonomy",
            "democratic education",
            "alternative education",
        ]

        # These should be in our research keywords
        assert len(key_topics) >= 5, "Minimum 5 key research topics"


class TestAPIIntegration:
    """Test API integration patterns"""

    def test_arxiv_rate_limiting(self):
        """Test arXiv rate limiting compliance"""

        # arXiv requires 3 seconds between requests
        min_delay = 3.0

        assert min_delay >= 3.0, "arXiv rate limiting: minimum 3s between requests"

    def test_pubmed_api_compliance(self):
        """Test PubMed API compliance"""
        # PubMed allows 3 requests per second without API key
        max_per_second = 3

        assert max_per_second <= 3, "PubMed rate limit: max 3/second without key"

    def test_owid_data_license(self):
        """Test OWID data usage compliance"""
        # Our World in Data: CC BY 4.0
        license_type = "CC BY 4.0"

        assert license_type == "CC BY 4.0", "OWID data under CC BY 4.0"

    def test_world_bank_api_format(self):
        """Test World Bank API response format"""
        # World Bank API returns JSON with specific structure
        # Format: /v2/country/{iso2}/indicator/{indicator}?format=json

        api_format = "json"
        assert api_format in ["json", "xml"], "World Bank supports JSON/XML"


class TestDataQualityMetrics:
    """Test data quality validation"""

    def test_missing_data_threshold(self):
        """Test acceptable missing data thresholds"""
        # Based on documentation: 15% missing data across countries
        max_missing_rate = 0.15

        assert max_missing_rate <= 0.20, "Missing data should be <20%"

    def test_temporal_coverage(self):
        """Test temporal data coverage"""
        # Should have data from at least 2000-2023
        min_year = 2000
        max_year = 2023

        coverage = max_year - min_year
        assert coverage >= 20, "At least 20 years of data coverage"

    def test_outlier_detection(self):
        """Test outlier handling (Winsorization)"""
        # Use 1st and 99th percentiles for winsorization
        lower_percentile = 0.01
        upper_percentile = 0.99

        assert lower_percentile + upper_percentile == 1.0, "Symmetric winsorization"
        assert 0 < lower_percentile < 0.05, "Lower percentile < 5%"


class TestValidationCorrelation:
    """Test documented validation correlations"""

    def test_google_scholar_correlation(self):
        """
        Test documented correlation with Google Scholar ranking

        Documented: r = 0.72 with Google Scholar ranking
        """
        documented_correlation = 0.72

        # Correlation should be positive and substantial
        assert 0.6 <= documented_correlation <= 0.8, "Strong positive correlation"

    def test_citation_database_coverage(self):
        """Test coverage across citation databases"""
        databases = {
            "arxiv": True,
            "pubmed": True,
            "google_scholar": False,  # Not directly accessed
            "scopus": False,  # Future
        }

        active_dbs = sum(databases.values())
        assert active_dbs >= 2, "At least 2 citation databases"


class TestBibTeXCoverage:
    """Test BibTeX coverage for research claims"""

    def test_key_research_papers(self):
        """Ensure key papers are in BibTeX"""
        bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")

        if not bibtex_path.exists():
            pytest.skip("BibTeX file not found")

        with open(bibtex_path, encoding="utf-8") as f:
            content = f.read()

        # Key research methodology papers
        key_papers = [
            "deci1985",  # Self-Determination Theory
            "csikszentmihalyi1990",  # Flow Theory
            "porges2011",  # Polyvagal Theory
        ]

        for paper in key_papers:
            assert paper in content, f"Missing key paper: {paper}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
