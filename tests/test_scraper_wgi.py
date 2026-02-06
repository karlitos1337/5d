import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to sys.path so we can import 5d_research_scraper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Use importlib because the module name starts with a digit
import importlib.util
spec = importlib.util.spec_from_file_location("research_scraper", "5d_research_scraper.py")
research_scraper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research_scraper)
ResearchScraper = research_scraper.ResearchScraper

class TestWGIScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = ResearchScraper()
        # Speed up retry for tests
        self.scraper.rate_limit_delay = 0.01
        self.scraper.retry_backoff = 1.0

    @patch('requests.get')
    def test_fetch_wgi_data_success(self, mock_get):
        # Mock response data for two countries
        # The scraper calls the API once for a batch of countries
        mock_response = MagicMock()
        mock_response.status_code = 200
        # World Bank API structure: [metadata, data_list]
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "per_page": 50, "total": 2},
            [
                {"countryiso3code": "USA", "value": 1.5, "date": "2023"},
                {"countryiso3code": "DEU", "value": 1.8, "date": "2023"}
            ]
        ]
        mock_get.return_value = mock_response

        data = self.scraper.fetch_world_bank_wgi_data(countries=["USA", "DEU"])

        self.assertIn("USA", data)
        self.assertIn("DEU", data)
        self.assertIn("Voice & Accountability", data["USA"])
        self.assertEqual(data["USA"]["Voice & Accountability"]["value"], 1.5)
        self.assertEqual(data["DEU"]["Voice & Accountability"]["value"], 1.8)

    @patch('requests.get')
    def test_fetch_wgi_data_empty(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"page": 1}, []] # Empty data
        mock_get.return_value = mock_response

        data = self.scraper.fetch_world_bank_wgi_data(countries=["USA"])
        self.assertEqual(data, {})

    @patch('requests.get')
    def test_fetch_wgi_data_rate_limit(self, mock_get):
        # First call 429, second call 200
        response_429 = MagicMock()
        response_429.status_code = 429

        response_200 = MagicMock()
        response_200.status_code = 200
        response_200.json.return_value = [
            {"page": 1},
            [{"countryiso3code": "USA", "value": 1.5, "date": "2023"}]
        ]

        mock_get.side_effect = [response_429, response_200]

        data = self.scraper.fetch_world_bank_wgi_data(countries=["USA"])
        self.assertIn("USA", data)
        self.assertEqual(mock_get.call_count, 2)

    @patch('requests.get')
    def test_fetch_wgi_data_api_error(self, mock_get):
        # Helper to simulate requests.exceptions.RequestException
        mock_get.side_effect = Exception("Connection Error")

        # Should handle exception gracefully (log error and return partial/empty)
        # Assuming scraper catches exceptions and returns whatever it has
        data = self.scraper.fetch_world_bank_wgi_data(countries=["USA"])
        self.assertEqual(data, {})

if __name__ == "__main__":
    unittest.main()
