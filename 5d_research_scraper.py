#!/usr/bin/env python3
"""
5D Research Scraper - ResearchGate & Academic Papers
Holt Live-Daten zu Bildung, Autonomie, Self-Directed Learning
"""

import json
import time
import re
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

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
            "self-directed learning",
            "intrinsic motivation education",
            "autonomy supportive teaching",
            "polyvagal theory education",
            "democratic schools",
            "student agency",
        ]
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

        # Domain-specific rate limiting
        self.last_request_times = defaultdict(float)

        # WHO API settings
        self.who_base_url = "https://ghoapi.azureedge.net/api"

        # World Bank API settings
        self.wb_base_url = "https://api.worldbank.org/v2"

    def _validate_country_code(self, code):
        """Validates that the country code is a 3-letter uppercase ISO3 string."""
        if not isinstance(code, str):
            return False
        return bool(re.match(r"^[A-Z]{3}$", code))

    def _rate_limit(self, domain="default"):
        """Enforce rate limiting between requests per domain."""
        current_time = time.time()
        last_time = self.last_request_times[domain]
        elapsed = current_time - last_time
        if elapsed < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - elapsed
            time.sleep(sleep_time)
        self.last_request_times[domain] = time.time()

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
                self._rate_limit("arxiv")  # Apply rate limiting for arXiv
                response = requests.get(base_url, params=params, timeout=10)

                if response.status_code == 429:  # Too Many Requests
                    wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                    print(f"⏳ Rate limit hit (arXiv), waiting {wait_time:.1f}s...")
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
                self._rate_limit("pubmed")
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
                self._rate_limit("pubmed")
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

    def fetch_who_mental_health_data(self, countries=None):
        """
        Fetch mental health indicators from WHO Global Health Observatory.
        """
        if countries is None:
            # Top 20 countries for baseline
            countries = ["USA", "GBR", "DEU", "FRA", "JPN", "CHN", "IND", "BRA",
                         "CAN", "AUS", "NOR", "SWE", "DNK", "FIN", "NLD", "CHE",
                         "NZL", "ESP", "ITA", "KOR"]

        # Filter out invalid country codes
        valid_countries = [c for c in countries if self._validate_country_code(c)]
        if len(valid_countries) < len(countries):
            print(f"⚠️  Filtered out {len(countries) - len(valid_countries)} invalid country codes")
        countries = valid_countries

        if not countries:
            print("❌ No valid countries provided for WHO data fetch")
            return {}

        # WHO indicator codes for mental health
        indicators = {
            "MH_12": "Depression prevalence (%)",  # Depressive disorders
            "MH_1": "Mental health workers (per 100,000)",
            "MH_17": "Suicide mortality rate"
        }

        mental_health_data = {}

        for indicator_code, indicator_name in indicators.items():
            print(f"  🏥 WHO: Fetching {indicator_name}...")

            for attempt in range(self.max_retries):
                try:
                    self._rate_limit("who")

                    # WHO API endpoint
                    url = f"{self.who_base_url}/{indicator_code}"
                    # OData requires string values to be single-quoted
                    quoted_countries = [f"'{c}'" for c in countries]
                    params = {"": "SpatialDim in ({})".format(",".join(quoted_countries))}

                    response = requests.get(url, params=params, timeout=15)

                    if response.status_code == 429:
                        wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                        print(f"    ⏳ WHO rate limit, waiting {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        continue

                    if response.status_code == 404:
                        print(f"    ⚠️  Indicator {indicator_code} not found")
                        break

                    response.raise_for_status()
                    data = response.json()

                    # Parse WHO response
                    if "value" in data:
                        for entry in data["value"]:
                            country = entry.get("SpatialDim")
                            value = entry.get("NumericValue")
                            year = entry.get("TimeDim")

                            if country and value is not None:
                                if country not in mental_health_data:
                                    mental_health_data[country] = {}

                                mental_health_data[country][indicator_name] = {
                                    "value": value,
                                    "year": year
                                }

                    break  # Success

                except requests.exceptions.RequestException as e:
                    if attempt < self.max_retries - 1:
                        wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                        print(f"    ⚠️  WHO error (attempt {attempt + 1}/{self.max_retries}): {e}")
                        time.sleep(wait_time)
                    else:
                        print(f"    ❌ WHO Error after {self.max_retries} attempts: {e}")
                except Exception as e:
                    print(f"    ❌ WHO Error: {e}")
                    break

        print(f"  ✅ WHO: {len(mental_health_data)} countries fetched")
        return mental_health_data

    def fetch_world_bank_education_data(self, countries=None):
        """
        Fetch education indicators from World Bank EdStats API.
        """
        if countries is None:
            countries = ["USA", "GBR", "DEU", "FRA", "JPN", "CHN", "IND", "BRA",
                         "CAN", "AUS", "NOR", "SWE", "DNK", "FIN", "NLD", "CHE",
                         "NZL", "ESP", "ITA", "KOR"]

        # Filter out invalid country codes
        valid_countries = [c for c in countries if self._validate_country_code(c)]
        if len(valid_countries) < len(countries):
            print(f"⚠️  Filtered out {len(countries) - len(valid_countries)} invalid country codes")
        countries = valid_countries

        if not countries:
            print("❌ No valid countries provided for World Bank data fetch")
            return {}

        # World Bank indicator codes for education
        indicators = {
            "SE.SEC.DURS": "Secondary education duration (years)",
            "SE.PRM.CMPT.ZS": "Primary completion rate (%)",
            "SE.XPD.TOTL.GD.ZS": "Government education expenditure (% of GDP)",
            "SE.SEC.ENRL.GC.FE.ZS": "Gross enrolment ratio, secondary, female (%)"
        }

        education_data = {}

        for indicator_code, indicator_name in indicators.items():
            print(f"  🏫 World Bank: Fetching {indicator_name}...")

            for attempt in range(self.max_retries):
                try:
                    self._rate_limit("worldbank")

                    # World Bank API endpoint
                    # Optimization: Fetch all countries in one request (up to 260 supported, we have 20)
                    countries_str = ";".join(countries)
                    url = f"{self.wb_base_url}/country/{countries_str}/indicator/{indicator_code}"
                    params = {
                        "format": "json",
                        "date": "2020:2023",  # Recent years
                        "per_page": 500
                    }

                    response = requests.get(url, params=params, timeout=15)

                    if response.status_code == 429:
                        wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                        print(f"    ⏳ World Bank rate limit, waiting {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        continue

                    response.raise_for_status()
                    data = response.json()

                    # Parse World Bank response
                    if isinstance(data, list) and len(data) > 1:
                        for entry in data[1]:  # Data is in second element
                            country_code = entry.get("countryiso3code")
                            value = entry.get("value")
                            year = entry.get("date")

                            if country_code and value is not None:
                                if country_code not in education_data:
                                    education_data[country_code] = {}

                                # Keep most recent data
                                if indicator_name not in education_data[country_code]:
                                    education_data[country_code][indicator_name] = {
                                        "value": value,
                                        "year": year
                                    }

                    break  # Success

                except requests.exceptions.RequestException as e:
                    if attempt < self.max_retries - 1:
                        wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                        print(f"    ⚠️  World Bank error (attempt {attempt + 1}/{self.max_retries}): {e}")
                        time.sleep(wait_time)
                    else:
                        print(f"    ❌ World Bank Error after {self.max_retries} attempts: {e}")
                except Exception as e:
                    print(f"    ❌ World Bank Error: {e}")
                    break

        print(f"  ✅ World Bank: {len(education_data)} countries fetched")
        return education_data

    def _fetch_all_arxiv(self):
        """Helper to fetch arXiv results for all keywords."""
        results = {}
        for keyword in self.keywords:
            print(f"📚 arXiv Suche: {keyword}")
            results[keyword] = self.search_arxiv(keyword, max_results=3)
            print(f"  ✅ arXiv ({keyword}): {len(results[keyword])} papers")
        return results

    def _fetch_all_pubmed(self):
        """Helper to fetch PubMed results for all keywords."""
        results = {}
        for keyword in self.keywords:
            print(f"📚 PubMed Suche: {keyword}")
            results[keyword] = self.search_pubmed(keyword, max_results=3)
            print(f"  ✅ PubMed ({keyword}): {len(results[keyword])} papers")
        return results

    def scrape_all(self):
        """Sammelt Papers zu allen Keywords + WHO/World Bank Daten (Parallelized)"""
        all_research = {}
        print("🔍 Starte Research Scraping (Parallelized)...")

        # Use ThreadPoolExecutor to run independent scraping tasks in parallel
        # Tasks:
        # 1. arXiv (iterate over keywords)
        # 2. PubMed (iterate over keywords)
        # 3. WHO Data
        # 4. World Bank Data

        with ThreadPoolExecutor(max_workers=4) as executor:
            future_arxiv = executor.submit(self._fetch_all_arxiv)
            future_pubmed = executor.submit(self._fetch_all_pubmed)
            # future_who = executor.submit(self.fetch_who_mental_health_data) # Skipped in original
            future_wb = executor.submit(self.fetch_world_bank_education_data)

            # Retrieve results
            arxiv_results = future_arxiv.result()
            pubmed_results = future_pubmed.result()
            wb_data = future_wb.result()
            # who_data = future_who.result()

        # Merge results into the expected structure
        for keyword in self.keywords:
            all_research[keyword] = {
                "arxiv": arxiv_results.get(keyword, []),
                "pubmed": pubmed_results.get(keyword, []),
                "timestamp": datetime.now().isoformat(),
            }

        # Add WHO Data (Skipped/Mocked)
        print("\n🏥 Fetching WHO Mental Health Data (SKIPPED - TODO: Fix API)...")
        all_research["who_mental_health"] = {
            "data": {}, # who_data if enabled
            "timestamp": datetime.now().isoformat(),
            "source": "WHO Global Health Observatory (Disabled)"
        }

        # Add World Bank Data
        all_research["world_bank_education"] = {
            "data": wb_data,
            "timestamp": datetime.now().isoformat(),
            "source": "World Bank EdStats API"
        }

        return all_research

    def save_results(self, data, filename="5d_research_data.json"):
        """Speichert Ergebnisse"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Gespeichert: {filename}")


if __name__ == "__main__":
    scraper = ResearchScraper()
    research_data = scraper.scrape_all()
    scraper.save_results(research_data)

    # Statistik
    total_papers = sum(len(data.get("arxiv", [])) + len(data.get("pubmed", [])) for data in research_data.values() if isinstance(data, dict) and "arxiv" in data)
    print(f"\n📊 Total: {total_papers} Papers gefunden")
