#!/usr/bin/env python3
"""
5D Research Scraper - ResearchGate & Academic Papers
Holt Live-Daten zu Bildung, Autonomie, Self-Directed Learning
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

class ResearchScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.keywords = [
            'self-directed learning',
            'intrinsic motivation education',
            'autonomy supportive teaching',
            'polyvagal theory education',
            'democratic schools',
            'student agency'
        ]
    
    def search_arxiv(self, query, max_results=5):
        """Sucht wissenschaftliche Papers auf arXiv"""
        base_url = 'http://export.arxiv.org/api/query'
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            soup = BeautifulSoup(response.content, 'xml')
            
            papers = []
            for entry in soup.find_all('entry'):
                paper = {
                    'title': entry.title.text.strip(),
                    'authors': [a.text for a in entry.find_all('author')],
                    'summary': entry.summary.text.strip()[:200],
                    'published': entry.published.text,
                    'link': entry.id.text
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"❌ arXiv Error: {e}")
            return []
    
    def search_pubmed(self, query, max_results=5):
        """Sucht medizinische/psychologische Papers auf PubMed"""
        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json'
        }
        
        try:
            # Search
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
            ids = data.get('esearchresult', {}).get('idlist', [])
            
            if not ids:
                return []
            
            # Fetch details
            fetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(ids),
                'retmode': 'json'
            }
            
            response = requests.get(fetch_url, params=fetch_params, timeout=10)
            data = response.json()
            
            papers = []
            for id in ids:
                item = data.get('result', {}).get(id, {})
                paper = {
                    'title': item.get('title', 'N/A'),
                    'authors': [a.get('name') for a in item.get('authors', [])[:3]],
                    'published': item.get('pubdate', 'N/A'),
                    'link': f"https://pubmed.ncbi.nlm.nih.gov/{id}/"
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"❌ PubMed Error: {e}")
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
                'arxiv': arxiv_papers,
                'pubmed': pubmed_papers,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"  ✅ arXiv: {len(arxiv_papers)} papers")
            print(f"  ✅ PubMed: {len(pubmed_papers)} papers")
            
            time.sleep(1)  # Rate limiting
        
        return all_research
    
    def save_results(self, data, filename='5d_research_data.json'):
        """Speichert Ergebnisse"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Gespeichert: {filename}")

if __name__ == "__main__":
    scraper = ResearchScraper()
    research_data = scraper.scrape_all()
    scraper.save_results(research_data)
    
    # Statistik
    total_papers = sum(
        len(data['arxiv']) + len(data['pubmed']) 
        for data in research_data.values()
    )
    print(f"\n📊 Total: {total_papers} Papers gefunden")
