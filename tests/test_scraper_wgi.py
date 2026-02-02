import importlib.util
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add root directory to path to import 5d_research_scraper
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# Import module starting with a number
spec = importlib.util.spec_from_file_location("module_5d", os.path.join(root_dir, "5d_research_scraper.py"))
module_5d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module_5d)
ResearchScraper = module_5d.ResearchScraper

class TestScraperWGI(unittest.TestCase):
    def setUp(self):
        self.scraper = ResearchScraper()

    @patch('requests.get')
    def test_fetch_world_bank_wgi_data(self, mock_get):
        # Mock response data for WGI (VA.EST)
        # Structure based on WB API: [metadata, data_list]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"page": 1, "pages": 1},
            [
                {
                    "countryiso3code": "USA",
                    "date": "2022",
                    "value": 1.5,
                    "indicator": {"id": "VA.EST", "value": "Voice and Accountability: Estimate"}
                },
                {
                    "countryiso3code": "DEU",
                    "date": "2022",
                    "value": 1.8,
                    "indicator": {"id": "VA.EST", "value": "Voice and Accountability: Estimate"}
                }
            ]
        ]
        mock_get.return_value = mock_response

        # Call the method
        # We pass a limited list of countries to verify batching logic isn't broken by small input
        # logic inside scraper handles default countries if None, or uses provided list
        result = self.scraper.fetch_world_bank_wgi_data(countries=["USA", "DEU"])

        self.assertIn("USA", result)
        self.assertIn("DEU", result)
        self.assertEqual(result["USA"]["Voice & Accountability"]["value"], 1.5)
        self.assertEqual(result["DEU"]["Voice & Accountability"]["value"], 1.8)

if __name__ == '__main__':
    unittest.main()
