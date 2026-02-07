import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Load module dynamically because it starts with a digit
file_path = Path(__file__).parent.parent / "5d_research_scraper.py"
spec = importlib.util.spec_from_file_location("research_scraper", file_path)
research_scraper = importlib.util.module_from_spec(spec)
sys.modules["research_scraper"] = research_scraper
spec.loader.exec_module(research_scraper)

ResearchScraper = research_scraper.ResearchScraper


class TestWGIScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = ResearchScraper()

    @patch("requests.get")
    def test_fetch_world_bank_wgi_data(self, mock_get):
        """Test fetching WGI data successfully."""
        # Mock response data for World Bank API
        # Structure: [metadata, data_list]
        mock_data = [
            {"page": 1, "pages": 1, "per_page": 50, "total": 2},
            [
                {
                    "indicator": {"id": "VA.EST", "value": "Voice and Accountability: Estimate"},
                    "country": {"id": "US", "value": "United States"},
                    "countryiso3code": "USA",
                    "date": "2023",
                    "value": 1.5,
                    "unit": "",
                    "obs_status": "",
                    "decimal": 2,
                },
                {
                    "indicator": {"id": "VA.EST", "value": "Voice and Accountability: Estimate"},
                    "country": {"id": "DE", "value": "Germany"},
                    "countryiso3code": "DEU",
                    "date": "2023",
                    "value": 1.8,
                    "unit": "",
                    "obs_status": "",
                    "decimal": 2,
                },
            ],
        ]

        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        # Call method with specific countries
        countries = ["USA", "DEU"]
        result = self.scraper.fetch_world_bank_wgi_data(countries=countries)

        # Assertions
        self.assertIn("USA", result)
        self.assertIn("DEU", result)

        # Check specific values
        self.assertEqual(result["USA"]["Voice & Accountability (Autonomy)"]["value"], 1.5)
        self.assertEqual(result["DEU"]["Voice & Accountability (Autonomy)"]["value"], 1.8)
        self.assertEqual(result["USA"]["Voice & Accountability (Autonomy)"]["year"], "2023")


if __name__ == "__main__":
    unittest.main()
