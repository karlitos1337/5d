#!/usr/bin/env python3
"""
5D Research Scraper - ResearchGate & Academic Papers
Holt Live-Daten zu Bildung, Autonomie, Self-Directed Learning
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
        self.last_request_time = 0

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
                    print(f"⚠️  arXiv error (attempt {attempt+1}/{self.max_retries}): {e}")
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
                    print(f"⚠️  PubMed error (attempt {attempt+1}/{self.max_retries}): {e}")
                    print(f"   Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ PubMed Error after {self.max_retries} attempts: {e}")
                    return []
            except Exception as e:
                print(f"❌ PubMed Error: {e}")
                return []

        return []

    def scrape_all(self):
        """Sammelt Papers zu allen Keywords"""
        all_research = {}

        print("🔍 Starte Research Scraping...")
        for keyword in self.keywords:
            print(f"\n📚 Suche: {keyword}")

            arxiv_papers = self.search_arxiv(keyword, max_results=3)
            pubmed_papers = self.search_pubmed(keyword, max_results=3)

            all_research[keyword] = {
                "arxiv": arxiv_papers,
                "pubmed": pubmed_papers,
                "timestamp": datetime.now().isoformat(),
            }

            print(f"  ✅ arXiv: {len(arxiv_papers)} papers")
            print(f"  ✅ PubMed: {len(pubmed_papers)} papers")

            # No additional sleep needed - _rate_limit() handles it

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
    total_papers = sum(len(data["arxiv"]) + len(data["pubmed"]) for data in research_data.values())
    print(f"\n📊 Total: {total_papers} Papers gefunden")
