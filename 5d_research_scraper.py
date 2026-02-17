#!/usr/bin/env python3
"""
5D Research Scraper - ResearchGate & Academic Papers
Holt Live-Daten zu Bildung, Autonomie, Self-Directed Learning
"""

import json
import time
import re
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

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
        self.locks = defaultdict(threading.Lock)

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
        """Enforce rate limiting between requests for a specific domain."""
        with self.locks[domain]:
            current_time = time.time()
            last_time = self.last_request_times[domain]
            elapsed = current_time - last_time
            if elapsed < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - elapsed
                time.sleep(sleep_time)
            self.last_request_times[domain] = time.time()

    def search_arxiv(self, query, max_results=5):
        """Sucht wissenschaftliche Papers auf arXiv mit Rate-Limiting und Retries"""
        base_url = "https://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        for attempt in range(self.max_retries):
            try:
                self._rate_limit("arxiv")  # Apply rate limiting for ArXiv
                response = requests.get(base_url, params=params, timeout=10)

                if response.status_code == 429:  # Too Many Requests
                    wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                    print(f"⏳ Rate limit hit (ArXiv), waiting {wait_time:.1f}s...")
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

        Args:
            countries: List of ISO3 country codes (default: top 20 countries)

        Returns:
            dict: Mental health data by country
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
                    params = {"$filter": "SpatialDim in ({})".format(",".join(quoted_countries))}

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

        Args:
            countries: List of ISO3 country codes (default: top 20 countries)

        Returns:
            dict: Education data by country
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

            # Iterate over countries in chunks of 10
            for i in range(0, len(countries), 10):
                chunk = countries[i:i + 10]
                countries_str = ";".join(chunk)

                for attempt in range(self.max_retries):
                    try:
                        self._rate_limit("worldbank")

                        # World Bank API endpoint
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

    def fetch_world_bank_wgi_data(self, countries=None):
        """
        Fetch Worldwide Governance Indicators (WGI) from World Bank.
        Source 3: Worldwide Governance Indicators
        Indicators:
            VA.EST: Voice and Accountability: Estimate
            RL.EST: Rule of Law: Estimate
            GE.EST: Government Effectiveness: Estimate
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
            print("❌ No valid countries provided for World Bank WGI data fetch")
            return {}

        # World Bank indicator codes for WGI
        indicators = {
            "VA.EST": "Voice and Accountability",
            "RL.EST": "Rule of Law",
            "GE.EST": "Government Effectiveness"
        }

        wgi_data = {}

        for indicator_code, indicator_name in indicators.items():
            print(f"  🏛️ World Bank WGI: Fetching {indicator_name}...")

            # Iterate over countries in chunks of 10
            for i in range(0, len(countries), 10):
                chunk = countries[i:i + 10]
                countries_str = ";".join(chunk)

                for attempt in range(self.max_retries):
                    try:
                        self._rate_limit("worldbank")

                        # World Bank API endpoint
                        url = f"{self.wb_base_url}/country/{countries_str}/indicator/{indicator_code}"
                        params = {
                            "format": "json",
                            "date": "2020:2023",  # Recent years
                            "per_page": 500,
                            "source": 3  # Source 3 = Worldwide Governance Indicators
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
                                    if country_code not in wgi_data:
                                        wgi_data[country_code] = {}

                                    # Keep most recent data
                                    if indicator_name not in wgi_data[country_code]:
                                        wgi_data[country_code][indicator_name] = {
                                            "value": value,
                                            "year": year
                                        }

                        break  # Success

                    except requests.exceptions.RequestException as e:
                        if attempt < self.max_retries - 1:
                            wait_time = self.rate_limit_delay * (self.retry_backoff**attempt)
                            print(f"    ⚠️  World Bank WGI error (attempt {attempt + 1}/{self.max_retries}): {e}")
                            time.sleep(wait_time)
                        else:
                            print(f"    ❌ World Bank WGI Error after {self.max_retries} attempts: {e}")
                    except Exception as e:
                        print(f"    ❌ World Bank WGI Error: {e}")
                        break

        print(f"  ✅ World Bank WGI: {len(wgi_data)} countries fetched")
        return wgi_data

    def _scrape_single_keyword(self, keyword):
        """Helper to scrape a single keyword (runs in thread)."""
        print(f"\n📚 Suche: {keyword}")

        # Requests are synchronous here, but run in parallel threads
        arxiv_papers = self.search_arxiv(keyword, max_results=3)
        pubmed_papers = self.search_pubmed(keyword, max_results=3)

        return keyword, {
            "arxiv": arxiv_papers,
            "pubmed": pubmed_papers,
            "timestamp": datetime.now().isoformat(),
        }

    def scrape_all(self):
        """Sammelt Papers zu allen Keywords + WHO/World Bank Daten"""
        all_research = {}

        print("🔍 Starte Research Scraping...")

        # Academic papers - Parallel execution
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_keyword = {
                executor.submit(self._scrape_single_keyword, keyword): keyword
                for keyword in self.keywords
            }

            for future in as_completed(future_to_keyword):
                keyword, result = future.result()
                all_research[keyword] = result
                print(f"  ✅ {keyword}: {len(result['arxiv'])} arXiv, {len(result['pubmed'])} PubMed")

        # WHO Mental Health Data
        # TODO: WHO API is currently considered broken/flaky. Re-enable after fixing or replacing.
        print("\n🏥 Fetching WHO Mental Health Data (SKIPPED - TODO: Fix API)...")
        # who_data = self.fetch_who_mental_health_data()
        all_research["who_mental_health"] = {
            "data": {},
            "timestamp": datetime.now().isoformat(),
            "source": "WHO Global Health Observatory (Disabled)"
        }

        # World Bank Education Data
        print("\n🏫 Fetching World Bank Education Data...")
        wb_data = self.fetch_world_bank_education_data()
        all_research["world_bank_education"] = {
            "data": wb_data,
            "timestamp": datetime.now().isoformat(),
            "source": "World Bank EdStats API"
        }

        # World Bank WGI Data
        print("\n🏛️ Fetching World Bank WGI Data...")
        wgi_data = self.fetch_world_bank_wgi_data()
        all_research["world_bank_wgi"] = {
            "data": wgi_data,
            "timestamp": datetime.now().isoformat(),
            "source": "World Bank Worldwide Governance Indicators"
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
    total_papers = sum(len(data.get("arxiv", [])) + len(data.get("pubmed", [])) for data in research_data.values() if "arxiv" in data)
    print(f"\n📊 Total: {total_papers} Papers gefunden")
