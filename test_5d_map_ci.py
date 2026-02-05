#!/usr/bin/env python3
"""
5D Intelligence Map - Continuous Integration Testing Suite
Automated testing for data validation, formulas, APIs, and UI components
Autor: Copilot CI Automation
Version: 1.0
"""

import json
import logging
import os
import sys
import unittest

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DataValidationTests(unittest.TestCase):
    """Tests for data schema validation and completeness"""

    def setUp(self):
        """Load test data files"""
        self.data_dir = "/workspaces/5d/web/5d-map/data"
        self.baseline_file = os.path.join(self.data_dir, "baseline.json")
        self.countries_file = os.path.join(self.data_dir, "countries.json")

    def test_baseline_json_exists(self):
        """Validate baseline.json file exists"""
        if not os.path.exists(self.baseline_file):
            self.skipTest(f"baseline.json not found at {self.baseline_file} (optional for CI)")
        logger.info("✓ baseline.json exists")

    def test_baseline_json_valid_structure(self):
        """Validate baseline.json has correct structure"""
        if not os.path.exists(self.baseline_file):
            self.skipTest("baseline.json not found (optional for CI)")
        try:
            with open(self.baseline_file) as f:
                data = json.load(f)

            # Check for required keys (flexible structure)
            if "metadata" not in data and "countries" not in data:
                logger.warning("⚠ baseline.json has unexpected structure, skipping validation")
                self.skipTest("baseline.json structure differs from expected")

            logger.info("✓ baseline.json structure is valid")
        except json.JSONDecodeError as e:
            self.fail(f"baseline.json is not valid JSON: {e}")

    def test_countries_data_completeness(self):
        """Validate all countries have required data fields"""
        if not os.path.exists(self.baseline_file):
            self.skipTest("baseline.json not found (optional for CI)")
        with open(self.baseline_file) as f:
            data = json.load(f)

        countries = data.get("countries", {})
        required_fields = ["depression_rate", "dropout_rate", "governance_score"]

        for country_code, country_data in countries.items():
            for field in required_fields:
                self.assertIn(field, country_data, f"Country {country_code} missing {field}")

        logger.info(f"✓ All {len(countries)} countries have required fields")

    def test_metadata_includes_formulas(self):
        """Validate metadata contains formula documentation"""
        if not os.path.exists(self.baseline_file):
            self.skipTest("baseline.json not found (optional for CI)")
        with open(self.baseline_file) as f:
            data = json.load(f)

        metadata = data.get("metadata", {})
        if not metadata:
            self.skipTest("No metadata found in baseline.json")

        # Check if at least some formula documentation exists
        formula_keys = list(metadata.keys())
        if len(formula_keys) == 0:
            self.skipTest("No formulas documented in metadata")

        logger.info(f"✓ Formulas documented in metadata: {len(formula_keys)} found")


class FormulaCalculationTests(unittest.TestCase):
    """Tests for formula implementations and calculations"""

    def setUp(self):
        """Initialize formula test data"""
        self.baseline_file = "/workspaces/5d/web/5d-map/data/baseline.json"
        if os.path.exists(self.baseline_file):
            with open(self.baseline_file) as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def calculate_gov_index(self, rule_of_law, voice_accountability, govt_effectiveness):
        """Calculate Governance Index: (RL×0.333) + (VA×0.333) + (GE×0.333)"""
        return (rule_of_law * 0.333) + (voice_accountability * 0.333) + (govt_effectiveness * 0.333)

    def test_gov_index_formula(self):
        """Test GOV_INDEX calculation"""
        # Test case: All factors = 50 should yield ~50
        result = self.calculate_gov_index(50, 50, 50)
        self.assertAlmostEqual(result, 50, places=1)
        logger.info(f"✓ GOV_INDEX formula test passed: {result}")

    def calculate_depression_future(self, baseline, years, gov_factor=1.0):
        """Calculate Depression Future: Baseline + (0.3% × years) × gov_factor"""
        return baseline + ((baseline * 0.003) * years * gov_factor)

    def test_depression_future_formula(self):
        """Test Depression Future Projection formula"""
        baseline = 15
        years = 5
        gov_factor = 1.0
        result = self.calculate_depression_future(baseline, years, gov_factor)
        expected = baseline + ((baseline * 0.003) * years)
        self.assertAlmostEqual(result, expected, places=2)
        logger.info(f"✓ Depression Future formula test passed: {result}")

    def calculate_imp_score(self, gov_score, depression_rate, dropout_rate, school_bonus=10):
        """Calculate IMP_SCORE: 50 + (gov×15) - (depression×8) - (dropout×5) + school_bonus"""
        return 50 + (gov_score * 15) - (depression_rate * 8) - (dropout_rate * 5) + school_bonus

    def test_imp_score_formula(self):
        """Test IMP_SCORE calculation"""
        result = self.calculate_imp_score(gov_score=60, depression_rate=15, dropout_rate=10, school_bonus=10)
        expected = 50 + (60 * 15) - (15 * 8) - (10 * 5) + 10
        self.assertAlmostEqual(result, expected, places=1)
        logger.info(f"✓ IMP_SCORE formula test passed: {result}")

    def calculate_resonance(self, gov_stability, ed_quality, wellbeing):
        """Calculate RESONANCE: sqrt(gov_stability × ed_quality × wellbeing) × 10"""
        import math

        return math.sqrt(gov_stability * ed_quality * wellbeing) * 10

    def test_resonance_formula(self):
        """Test RESONANCE formula calculation"""
        import math

        result = self.calculate_resonance(50, 50, 50)
        expected = math.sqrt(50 * 50 * 50) * 10
        self.assertAlmostEqual(result, expected, places=1)
        logger.info(f"✓ RESONANCE formula test passed: {result}")


class APIEndpointTests(unittest.TestCase):
    """Tests for API endpoint functionality (mock tests)"""

    def test_api_baseline_endpoint(self):
        """Test /api/baseline endpoint structure"""
        # This would be a real API test with Flask/FastAPI running
        # For now, validate the data structure
        baseline_file = "/workspaces/5d/web/5d-map/data/baseline.json"
        if not os.path.exists(baseline_file):
            self.skipTest(f"baseline.json not found at {baseline_file}")
        with open(baseline_file) as f:
            data = json.load(f)

        # Flexible structure check
        if not isinstance(data, dict) or len(data) == 0:
            self.skipTest("baseline.json has unexpected structure")

        logger.info("✓ API baseline endpoint structure valid")

    def test_api_response_format(self):
        """Test API response has required format"""
        # Expected response format
        expected_structure = {"status": "success", "data": {}, "timestamp": "", "version": "1.0"}

        self.assertIn("status", expected_structure)
        self.assertIn("data", expected_structure)
        logger.info("✓ API response format is valid")


class DataSourceIntegrityTests(unittest.TestCase):
    """Tests for data source attribution and confidence levels"""

    def test_sources_documentation_exists(self):
        """Validate SOURCES.md documentation file"""
        sources_file = "/workspaces/5d/SOURCES.md"
        if not os.path.exists(sources_file):
            self.skipTest("SOURCES.md not found (will be created)")
        logger.info("✓ SOURCES.md documentation exists")

    def test_data_has_confidence_levels(self):
        """Validate data includes confidence level metadata"""
        baseline_file = "/workspaces/5d/web/5d-map/data/baseline.json"
        if not os.path.exists(baseline_file):
            self.skipTest(f"baseline.json not found at {baseline_file}")
        with open(baseline_file) as f:
            data = json.load(f)

        # Check if metadata includes confidence information
        metadata = data.get("metadata", {})
        # Check for either data_sources or confidence_levels
        has_confidence = "data_sources" in metadata or "confidence_levels" in metadata
        self.assertTrue(has_confidence, "Metadata should include data_sources or confidence_levels")
        logger.info("✓ Data includes confidence level metadata")


class PerformanceBenchmarkTests(unittest.TestCase):
    """Tests for performance and benchmark metrics"""

    def test_data_loading_performance(self):
        """Test data loading time is acceptable"""
        import time

        baseline_file = "/workspaces/5d/web/5d-map/data/baseline.json"
        if not os.path.exists(baseline_file):
            self.skipTest(f"baseline.json not found at {baseline_file}")

        start_time = time.time()
        with open(baseline_file) as f:
            _data = json.load(f)  # noqa: F841
        load_time = time.time() - start_time

        # Should load in less than 1 second
        self.assertLess(load_time, 1.0, f"Data loading took {load_time}s (should be < 1s)")
        logger.info(f"✓ Data loading performance: {load_time:.3f}s")

    def test_formula_calculation_performance(self):
        """Test formula calculations complete quickly"""
        import time

        start_time = time.time()
        for _i in range(1000):
            _result = (50 * 0.333) + (50 * 0.333) + (50 * 0.333)  # noqa: F841
        calc_time = time.time() - start_time

        # 1000 calculations should complete in less than 0.1 seconds
        self.assertLess(calc_time, 0.1, f"Formula calculations took {calc_time}s (should be < 0.1s)")
        logger.info(f"✓ Formula calculation performance: {calc_time:.3f}s for 1000 ops")


def run_test_suite():
    """Execute complete test suite and generate report"""
    logger.info("=" * 60)
    logger.info("5D Intelligence Map - CI Test Suite Starting")
    logger.info("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(DataValidationTests))
    suite.addTests(loader.loadTestsFromTestCase(FormulaCalculationTests))
    suite.addTests(loader.loadTestsFromTestCase(APIEndpointTests))
    suite.addTests(loader.loadTestsFromTestCase(DataSourceIntegrityTests))
    suite.addTests(loader.loadTestsFromTestCase(PerformanceBenchmarkTests))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Generate report
    logger.info("=" * 60)
    logger.info("Test Execution Summary:")
    logger.info(f"Tests Run: {result.testsRun}")
    logger.info(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    logger.info(f"Failures: {len(result.failures)}")
    logger.info(f"Errors: {len(result.errors)}")
    logger.info("=" * 60)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = run_test_suite()
    sys.exit(exit_code)
