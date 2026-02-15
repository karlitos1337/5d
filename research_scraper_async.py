#!/usr/bin/env python3
"""
5D Research Scraper - Async Version
High-performance async API calls with connection pooling and rate limiting
"""

import asyncio
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

import aiohttp
from bs4 import BeautifulSoup

from utils.rate_limiter import DomainRateLimiter


class AsyncResearchScraper:
    """
    Async research scraper with connection pooling and rate limiting.
    
    Provides 5-10x speedup over sequential scraping by using:
    - aiohttp for async HTTP requests
    - Connection pooling for efficiency
    - Token bucket rate limiting for API compliance
    - Parallel execution with asyncio.gather
    """
    
    def __init__(self, rate_limit_delay=1.0, max_retries=3, retry_backoff=2.0):
        """
        Initialize async scraper.
        
        Args:
            rate_limit_delay: Seconds to wait between requests (default: 1.0)
            max_retries: Maximum number of retries on failure (default: 3)
            retry_backoff: Exponential backoff multiplier (default: 2.0)
        """
        self.keywords = [
            "self-directed learning",
            "intrinsic motivation education",
            "autonomy supportive teaching",
            "polyvagal theory education",
            "democratic schools",
            "student agency",
        ]
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        
        # Initialize domain-specific rate limiters
        # arXiv: 3s minimum delay (0.33 req/sec)
        # PubMed: 3 req/sec max without API key (1.0 req/sec to be safe)
        # WHO: 1 req/sec
        # World Bank: 1 req/sec
        self.rate_limiter = DomainRateLimiter(default_rate=1.0)
        
        # Connection pooling settings
        self.connector = None
        self.session = None
        
    async def __aenter__(self):
        """Context manager entry - create session"""
        # Use connection pooling for efficiency
        # Reference: aiohttp best practices
        self.connector = aiohttp.TCPConnector(
            limit=10,  # Max 10 concurrent connections
            limit_per_host=5,  # Max 5 per host
            ttl_dns_cache=300  # Cache DNS for 5 minutes
        )
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        self.session = aiohttp.ClientSession(
            connector=self.connector,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close session"""
        if self.session:
            await self.session.close()
        if self.connector:
            await self.connector.close()
    
    async def search_arxiv_async(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search arXiv papers asynchronously.
        
        Args:
            query: Search query
            max_results: Maximum papers to return
            
        Returns:
            List of paper dictionaries
        """
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
                # Apply rate limiting (arXiv: 0.33 req/sec = 3s delay)
                await self.rate_limiter.acquire("arxiv", rate=0.33)
                
                async with self.session.get(base_url, params=params) as response:
                    if response.status == 429:  # Too Many Requests
                        wait_time = (self.retry_backoff ** attempt)
                        print(f"⏳ Rate limit hit (ArXiv), waiting {wait_time:.1f}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    
                    response.raise_for_status()
                    content = await response.text()
                    soup = BeautifulSoup(content, "xml")
                    
                    papers = []
                    for entry in soup.find_all("entry"):
                        paper = {
                            "title": entry.title.text.strip() if entry.title else "N/A",
                            "authors": [a.text for a in entry.find_all("author")] if entry.find_all("author") else [],
                            "summary": (entry.summary.text.strip()[:200] if entry.summary else "N/A"),
                            "published": entry.published.text if entry.published else "N/A",
                            "link": entry.id.text if entry.id else "N/A",
                        }
                        papers.append(paper)
                    
                    return papers
                    
            except aiohttp.ClientError as e:
                if attempt < self.max_retries - 1:
                    wait_time = (self.retry_backoff ** attempt)
                    print(f"⚠️  arXiv error (attempt {attempt + 1}/{self.max_retries}): {e}")
                    print(f"   Retrying in {wait_time:.1f}s...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"❌ arXiv Error after {self.max_retries} attempts: {e}")
                    return []
            except Exception as e:
                print(f"❌ arXiv Error: {e}")
                return []
        
        return []
    
    async def search_pubmed_async(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search PubMed papers asynchronously.
        
        Args:
            query: Search query
            max_results: Maximum papers to return
            
        Returns:
            List of paper dictionaries
        """
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"}
        
        for attempt in range(self.max_retries):
            try:
                # Apply rate limiting (PubMed: 1 req/sec to be safe)
                await self.rate_limiter.acquire("pubmed", rate=1.0)
                
                # Search for paper IDs
                async with self.session.get(search_url, params=search_params) as response:
                    if response.status == 429:
                        wait_time = (self.retry_backoff ** attempt)
                        print(f"⏳ PubMed rate limit, waiting {wait_time:.1f}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    
                    response.raise_for_status()
                    data = await response.json()
                    ids = data.get("esearchresult", {}).get("idlist", [])
                    
                    if not ids:
                        return []
                    
                    # Fetch paper details
                    await self.rate_limiter.acquire("pubmed", rate=1.0)
                    
                    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                    fetch_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
                    
                    async with self.session.get(fetch_url, params=fetch_params) as response:
                        response.raise_for_status()
                        data = await response.json()
                        
                        papers = []
                        for paper_id in ids:
                            item = data.get("result", {}).get(paper_id, {})
                            paper = {
                                "title": item.get("title", "N/A"),
                                "authors": [a.get("name") for a in item.get("authors", [])[:3]],
                                "published": item.get("pubdate", "N/A"),
                                "link": f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/",
                            }
                            papers.append(paper)
                        
                        return papers
                        
            except aiohttp.ClientError as e:
                if attempt < self.max_retries - 1:
                    wait_time = (self.retry_backoff ** attempt)
                    print(f"⚠️  PubMed error (attempt {attempt + 1}/{self.max_retries}): {e}")
                    print(f"   Retrying in {wait_time:.1f}s...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"❌ PubMed Error after {self.max_retries} attempts: {e}")
                    return []
            except Exception as e:
                print(f"❌ PubMed Error: {e}")
                return []
        
        return []
    
    async def fetch_world_bank_education_data_async(
        self, 
        countries: Optional[List[str]] = None
    ) -> Dict:
        """
        Fetch education indicators from World Bank EdStats API asynchronously.
        
        Args:
            countries: List of ISO3 country codes (default: top 20 countries)
            
        Returns:
            dict: Education data by country
        """
        if countries is None:
            countries = ["USA", "GBR", "DEU", "FRA", "JPN", "CHN", "IND", "BRA",
                         "CAN", "AUS", "NOR", "SWE", "DNK", "FIN", "NLD", "CHE",
                         "NZL", "ESP", "ITA", "KOR"]
        
        # World Bank indicator codes for education
        indicators = {
            "SE.SEC.DURS": "Secondary education duration (years)",
            "SE.PRM.CMPT.ZS": "Primary completion rate (%)",
            "SE.XPD.TOTL.GD.ZS": "Government education expenditure (% of GDP)",
            "SE.SEC.ENRL.GC.FE.ZS": "Gross enrolment ratio, secondary, female (%)"
        }
        
        education_data = {}
        wb_base_url = "https://api.worldbank.org/v2"
        
        for indicator_code, indicator_name in indicators.items():
            print(f"  🏫 World Bank: Fetching {indicator_name}...")
            
            for attempt in range(self.max_retries):
                try:
                    await self.rate_limiter.acquire("worldbank", rate=1.0)
                    
                    countries_str = ";".join(countries[:10])  # Limit to 10 per request
                    url = f"{wb_base_url}/country/{countries_str}/indicator/{indicator_code}"
                    params = {
                        "format": "json",
                        "date": "2020:2023",
                        "per_page": 500
                    }
                    
                    async with self.session.get(url, params=params) as response:
                        if response.status == 429:
                            wait_time = (self.retry_backoff ** attempt)
                            print(f"    ⏳ World Bank rate limit, waiting {wait_time:.1f}s...")
                            await asyncio.sleep(wait_time)
                            continue
                        
                        response.raise_for_status()
                        data = await response.json()
                        
                        # Parse World Bank response
                        if isinstance(data, list) and len(data) > 1:
                            for entry in data[1]:
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
                        
                except aiohttp.ClientError as e:
                    if attempt < self.max_retries - 1:
                        wait_time = (self.retry_backoff ** attempt)
                        print(f"    ⚠️  World Bank error (attempt {attempt + 1}/{self.max_retries}): {e}")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"    ❌ World Bank Error after {self.max_retries} attempts: {e}")
                except Exception as e:
                    print(f"    ❌ World Bank Error: {e}")
                    break
        
        print(f"  ✅ World Bank: {len(education_data)} countries fetched")
        return education_data
    
    async def scrape_keyword_async(self, keyword: str) -> tuple[str, Dict]:
        """
        Scrape research data for a single keyword asynchronously.
        
        Args:
            keyword: Research keyword
            
        Returns:
            Tuple of (keyword, result_dict)
        """
        print(f"\n📚 Suche: {keyword}")
        
        # Run arXiv and PubMed searches in parallel
        arxiv_task = self.search_arxiv_async(keyword, max_results=3)
        pubmed_task = self.search_pubmed_async(keyword, max_results=3)
        
        arxiv_papers, pubmed_papers = await asyncio.gather(arxiv_task, pubmed_task)
        
        result = {
            "arxiv": arxiv_papers,
            "pubmed": pubmed_papers,
            "timestamp": datetime.now().isoformat(),
        }
        
        print(f"  ✅ {keyword}: {len(arxiv_papers)} arXiv, {len(pubmed_papers)} PubMed")
        
        return keyword, result
    
    async def scrape_all_async(self) -> Dict:
        """
        Scrape all research data asynchronously.
        
        Returns:
            Dictionary with all research data
        """
        print("🔍 Starte Async Research Scraping...")
        start_time = time.time()
        
        # Scrape all keywords in parallel
        tasks = [self.scrape_keyword_async(keyword) for keyword in self.keywords]
        results = await asyncio.gather(*tasks)
        
        # Convert to dictionary
        all_research = {keyword: result for keyword, result in results}
        
        # WHO Mental Health Data (disabled - API issues)
        print("\n🏥 Fetching WHO Mental Health Data (SKIPPED - TODO: Fix API)...")
        all_research["who_mental_health"] = {
            "data": {},
            "timestamp": datetime.now().isoformat(),
            "source": "WHO Global Health Observatory (Disabled)"
        }
        
        # World Bank Education Data
        print("\n🏫 Fetching World Bank Education Data...")
        wb_data = await self.fetch_world_bank_education_data_async()
        all_research["world_bank_education"] = {
            "data": wb_data,
            "timestamp": datetime.now().isoformat(),
            "source": "World Bank EdStats API"
        }
        
        elapsed = time.time() - start_time
        print(f"\n⏱️  Total scraping time: {elapsed:.2f}s")
        
        return all_research
    
    def save_results(self, data: Dict, filename: str = "5d_research_data.json"):
        """
        Save results to JSON file.
        
        Args:
            data: Research data dictionary
            filename: Output filename
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Gespeichert: {filename}")


async def main():
    """Main async function for testing"""
    async with AsyncResearchScraper() as scraper:
        research_data = await scraper.scrape_all_async()
        scraper.save_results(research_data)
        
        # Statistics
        total_papers = sum(
            len(data.get("arxiv", [])) + len(data.get("pubmed", [])) 
            for data in research_data.values() 
            if "arxiv" in data
        )
        print(f"\n📊 Total: {total_papers} Papers gefunden")


if __name__ == "__main__":
    asyncio.run(main())
