#!/usr/bin/env python3
"""
5D GitHub API Integration
Live-Daten zu Education Tech, Open Source Bildungsprojekten
"""

import requests
import json
from datetime import datetime

class GitHubExplorer:
    def __init__(self, token=None):
        self.base_url = 'https://api.github.com'
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
        
        self.search_queries = [
            'self-directed learning',
            'democratic education',
            'intrinsic motivation',
            'education autonomy',
            'open pedagogy'
        ]
    
    def search_repositories(self, query, max_results=10):
        """Sucht relevante GitHub Repositories"""
        url = f'{self.base_url}/search/repositories'
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': max_results
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            data = response.json()
            
            repos = []
            for item in data.get('items', []):
                repo = {
                    'name': item['name'],
                    'full_name': item['full_name'],
                    'description': item['description'],
                    'stars': item['stargazers_count'],
                    'forks': item['forks_count'],
                    'language': item['language'],
                    'url': item['html_url'],
                    'updated': item['updated_at']
                }
                repos.append(repo)
            
            return repos
        except Exception as e:
            print(f"❌ GitHub API Error: {e}")
            return []
    
    def get_trending_topics(self):
        """Holt trending education topics"""
        topics = ['education', 'learning', 'pedagogy', 'edtech']
        trending = {}
        
        for topic in topics:
            url = f'{self.base_url}/search/repositories'
            params = {
                'q': f'topic:{topic}',
                'sort': 'updated',
                'order': 'desc',
                'per_page': 5
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                data = response.json()
                trending[topic] = [
                    {
                        'name': item['name'],
                        'stars': item['stargazers_count'],
                        'url': item['html_url']
                    }
                    for item in data.get('items', [])
                ]
            except Exception as e:
                print(f"❌ Topic {topic} error: {e}")
        
        return trending
    
    def explore_all(self):
        """Sammelt alle GitHub Daten"""
        all_data = {
            'repositories': {},
            'trending': {},
            'timestamp': datetime.now().isoformat()
        }
        
        print("🔍 GitHub API Exploration...")
        
        for query in self.search_queries:
            print(f"\n🔎 Query: {query}")
            repos = self.search_repositories(query, max_results=5)
            all_data['repositories'][query] = repos
            print(f"  ✅ {len(repos)} Repositories gefunden")
        
        print("\n📈 Trending Topics...")
        all_data['trending'] = self.get_trending_topics()
        
        return all_data
    
    def save_results(self, data, filename='5d_github_data.json'):
        """Speichert GitHub Daten"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Gespeichert: {filename}")

if __name__ == "__main__":
    # Optional: Setze GITHUB_TOKEN für höhere Rate Limits
    # export GITHUB_TOKEN=ghp_your_token_here
    import os
    token = os.getenv('GITHUB_TOKEN')
    
    explorer = GitHubExplorer(token=token)
    github_data = explorer.explore_all()
    explorer.save_results(github_data)
    
    total_repos = sum(len(repos) for repos in github_data['repositories'].values())
    print(f"\n📊 Total: {total_repos} Repositories analysiert")
