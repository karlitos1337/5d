#!/usr/bin/env python3
"""
5D Research Scraper - Science Superquelle Extraction
Fetches validated data for Autonomy, Motivation, and Resilience
"""

import json
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class ResearchScraper:
    def __init__(self, rate_limit_delay=1.0, max_retries=3, retry_backoff=2.0):
        """Initialize scraper with configurable rate limiting.

        Args:
            rate_limit_delay: Seconds to wait between requests (default: 1.0)
            max_retries: Maximum number of retries on failure (default: 3)
            retry_backoff: Exponential backoff multiplier (default: 2.0)
        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.keywords = [
            "self-determination theory meta-analysis",
            "intrinsic motivation measurement",
            "autonomy support effectiveness",
            "psychological resilience scales",
            "social capital and well-being",
            "authenticity and mental health",
        ]
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.last_request_time = 0

        # WHO API settings
        self.who_base_url = "https://ghoapi.azureedge.net/api"

        # World Bank API settings
        self.wb_base_url = "https://api.worldbank.org/v2"

    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - elapsed
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def search_arxiv(self, query, max_results=5):
        """Sucht wissenschaftliche Papers auf arXiv mit Rate-Limiting und Retries"""
        base_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        for attempt in range(self.max_retries):
            try:
                self._rate_limit()  # Apply rate limiting
                response = requests.get(base_url, params=params, timeout=10)

                if response.status_code == 429:  # Too Many Requests
                    wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                    print(f"⏳ Rate limit hit, waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                soup = BeautifulSoup(response.content, "xml")

                papers = []
                for entry in soup.find_all("entry"):
                    paper = {
                        "title": entry.title.text.strip(),
                        "authors": [a.text for a in entry.find_all("author")],
                        "summary": entry.summary.text.strip()[:200],
                        "published": entry.published.text,
                        "link": entry.id.text,
                    }
                    papers.append(paper)

                return papers
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                    print(f"⚠️  arXiv error (attempt {attempt + 1}/{self.max_retries}): {e}")
                    print(f"   Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ arXiv Error after {self.max_retries} attempts: {e}")
                    return []
            except Exception as e:
                print(f"❌ arXiv Error: {e}")
                return []

        return []

    def search_pubmed(self, query, max_results=5):
        """Sucht medizinische/psychologische Papers auf PubMed mit Rate-Limiting"""
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"}

        for attempt in range(self.max_retries):
            try:
                # Search with rate limiting
                self._rate_limit()
                response = requests.get(base_url, params=params, timeout=10)

                if response.status_code == 429:
                    wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                    print(f"⏳ PubMed rate limit, waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()
                ids = data.get("esearchresult", {}).get("idlist", [])

                if not ids:
                    return []

                # Fetch details with rate limiting
                self._rate_limit()
                fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                fetch_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}

                response = requests.get(fetch_url, params=fetch_params, timeout=10)
                response.raise_for_status()
                data = response.json()

                papers = []
                for id in ids:
                    item = data.get("result", {}).get(id, {})
                    paper = {
                        "title": item.get("title", "N/A"),
                        "authors": [a.get("name") for a in item.get("authors", [])[:3]],
                        "published": item.get("pubdate", "N/A"),
                        "link": f"https://pubmed.ncbi.nlm.nih.gov/{id}/",
                    }
                    papers.append(paper)

                return papers
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                    print(f"⚠️  PubMed error (attempt {attempt + 1}/{self.max_retries}): {e}")
                    print(f"   Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ PubMed Error after {self.max_retries} attempts: {e}")
                    return []
            except Exception as e:
                print(f"❌ PubMed Error: {e}")
                return []

        return []

    def fetch_governance_data(self, countries=None):
        """
        Fetch Worldwide Governance Indicators (WGI) for Autonomy/Voice & Accountability.

        Args:
            countries: List of ISO3 country codes (default: top 20 countries)

        Returns:
            dict: Governance data by country
        """
        if countries is None:
            countries = ["USA", "GBR", "DEU", "FRA", "JPN", "CHN", "IND", "BRA",
                         "CAN", "AUS", "NOR", "SWE", "DNK", "FIN", "NLD", "CHE",
                         "NZL", "ESP", "ITA", "KOR"]

        # World Bank WGI indicators
        # Voice and Accountability: Estimate (VA.EST)
        indicators = {
            "VA.EST": "Voice and Accountability: Estimate",
            "PV.EST": "Political Stability and Absence of Violence/Terrorism: Estimate",
            "GE.EST": "Government Effectiveness: Estimate",
            "RQ.EST": "Regulatory Quality: Estimate",
            "RL.EST": "Rule of Law: Estimate",
            "CC.EST": "Control of Corruption: Estimate"
        }

        # Note: WGI data is often under 'wgi' source or specific indicators in WB API
        # Using standard WB API with specific indicator codes might work if mapped,
        # otherwise we might need a specific WGI dataset ID.
        # WGI indicators in WB API usually look like 'WGI.VA.EST' or similar, but
        # often 'VA.EST' works if the source is specified or if it's in the main index.
        # Let's try standard indicators.

        # Actually, WGI indicators in WB API are often like 'VA.EST'.
        # Let's test with 'VA.EST'.

        governance_data = {}

        for indicator_code, indicator_name in indicators.items():
            print(f"  🏛️ Governance: Fetching {indicator_name}...")

            for attempt in range(self.max_retries):
                try:
                    self._rate_limit()

                    countries_str = ";".join(countries[:10])
                    # WGI indicators are often accessible via the main API
                    url = f"{self.wb_base_url}/country/{countries_str}/indicator/{indicator_code}"
                    params = {
                        "format": "json",
                        "date": "2020:2023",
                        "per_page": 500,
                        "source": 3  # Source 3 is often WGI, but let's try without first or default
                    }

                    response = requests.get(url, params=params, timeout=15)

                    if response.status_code == 429:
                        wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                        print(f"    ⏳ World Bank rate limit, waiting {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        continue

                    if response.status_code != 200:
                        # Try without source param if failed
                        pass

                    # Parse response
                    try:
                        data = response.json()
                    except ValueError:
                        print("    ❌ Invalid JSON response")
                        break

                    if isinstance(data, list) and len(data) > 1 and data[1] is not None:
                        for entry in data[1]:
                            country_code = entry.get("countryiso3code")
                            value = entry.get("value")
                            year = entry.get("date")

                            if country_code and value is not None:
                                if country_code not in governance_data:
                                    governance_data[country_code] = {}

                                if indicator_name not in governance_data[country_code]:
                                    governance_data[country_code][indicator_name] = {
                                        "value": value,
                                        "year": year
                                    }
                    else:
                        print(f"    ⚠️  No data found for {indicator_code}")

                    break

                except Exception as e:
                    print(f"    ❌ Error fetching {indicator_code}: {e}")
                    break

        print(f"  ✅ Governance: {len(governance_data)} countries fetched")
        return governance_data

    def scrape_all(self):
        """Sammelt Papers zu allen Keywords + WHO/World Bank Daten"""
        all_research = {}

        print("🔍 Starte Research Scraping (Science Superquelle Protocol)...")

        # Academic papers
        for keyword in self.keywords:
            print(f"\n📚 Query: {keyword}")

            arxiv_papers = self.search_arxiv(keyword, max_results=3)
            pubmed_papers = self.search_pubmed(keyword, max_results=3)

            all_research[keyword] = {
                "arxiv": arxiv_papers,
                "pubmed": pubmed_papers,
                "timestamp": datetime.now().isoformat(),
            }

            print(f"  ✅ arXiv: {len(arxiv_papers)} papers")
            print(f"  ✅ PubMed: {len(pubmed_papers)} papers")

        # Governance Data (WGI)
        print("\n🏛️ Fetching WGI Governance Data (Autonomy/Voice)...")
        gov_data = self.fetch_governance_data()
        all_research["governance_wgi"] = {
            "data": gov_data,
            "timestamp": datetime.now().isoformat(),
            "source": "World Bank Worldwide Governance Indicators"
        }

        return all_research

    def save_results(self, data, filename="5d_research_data.json"):
        """Speichert Ergebnisse"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Saved to: {filename}")


if __name__ == "__main__":
    scraper = ResearchScraper()
    research_data = scraper.scrape_all()
    scraper.save_results(research_data)

    # Statistik
    total_papers = sum(len(data.get("arxiv", [])) + len(data.get("pubmed", [])) for k, data in research_data.items() if k not in ["governance_wgi", "who_mental_health"])
    print(f"\n📊 Total Papers Found: {total_papers}")
