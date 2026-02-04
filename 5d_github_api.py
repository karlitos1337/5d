#!/usr/bin/env python3
"""
5D GitHub API Integration
Live-Daten zu Education Tech, Open Source Bildungsprojekten
"""

import json
from datetime import datetime

import requests


class GitHubExplorer:
    def __init__(self, token=None):
        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.token = token
        if token:
            self.headers["Authorization"] = f"token {token}"

        self.search_queries = [
            "self-directed learning",
            "democratic education",
            "intrinsic motivation",
            "education autonomy",
            "open pedagogy",
        ]

        # Rate limit tracking
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
        self.last_rate_limit_check = None

    def _update_rate_limits(self, response):
        """Update rate limit information from response headers."""
        if response.headers:
            self.rate_limit_remaining = int(
                response.headers.get("X-RateLimit-Remaining", -1)
            )
            self.rate_limit_reset = int(response.headers.get("X-RateLimit-Reset", 0))

            if self.rate_limit_remaining is not None and self.rate_limit_remaining < 10:
                print(
                    f"⚠️  Rate limit low: {self.rate_limit_remaining} requests remaining"
                )
                if self.rate_limit_reset:
                    from datetime import datetime

                    reset_time = datetime.fromtimestamp(self.rate_limit_reset)
                    print(f"   Resets at: {reset_time.strftime('%H:%M:%S')}")

    def _check_and_refresh_token(self):
        """Check if token is still valid and refresh if needed."""
        if not self.token:
            return True  # No token to check

        try:
            url = f"{self.base_url}/rate_limit"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 401:
                print("❌ Token expired or invalid")
                # In production: implement token refresh logic here
                # For now, clear the token
                self.token = None
                if "Authorization" in self.headers:
                    del self.headers["Authorization"]
                return False

            if response.status_code == 200:
                data = response.json()
                resources = data.get("resources", {})
                core = resources.get("core", {})
                self.rate_limit_remaining = core.get("remaining")
                self.rate_limit_reset = core.get("reset")

                if self.rate_limit_remaining == 0:
                    import time

                    wait_time = self.rate_limit_reset - time.time()
                    if wait_time > 0:
                        print(f"⏳ Rate limit exhausted. Waiting {wait_time:.0f}s...")
                        time.sleep(min(wait_time, 60))  # Cap at 60s

                return True
        except Exception as e:
            print(f"⚠️  Token check failed: {e}")
            return True  # Continue anyway

    def search_repositories(self, query, max_results=10):
        """Sucht relevante GitHub Repositories mit Rate-Limit-Handling"""
        # Check token validity
        self._check_and_refresh_token()

        url = f"{self.base_url}/search/repositories"
        params = {"q": query, "sort": "stars", "order": "desc", "per_page": max_results}

        try:
            response = requests.get(
                url, headers=self.headers, params=params, timeout=10
            )

            # Update rate limits
            self._update_rate_limits(response)

            if response.status_code == 403:
                # Rate limit exceeded
                print(f"❌ Rate limit exceeded for query: {query}")
                import time

                if self.rate_limit_reset:
                    wait_time = self.rate_limit_reset - time.time()
                    if wait_time > 0 and wait_time < 3600:  # Max 1 hour
                        print(f"⏳ Waiting {wait_time:.0f}s for rate limit reset...")
                        time.sleep(wait_time + 1)
                        # Retry once
                        return self.search_repositories(query, max_results)
                return []

            response.raise_for_status()
            data = response.json()

            repos = []
            for item in data.get("items", []):
                repo = {
                    "name": item["name"],
                    "full_name": item["full_name"],
                    "description": item["description"],
                    "stars": item["stargazers_count"],
                    "forks": item["forks_count"],
                    "language": item["language"],
                    "url": item["html_url"],
                    "updated": item["updated_at"],
                }
                repos.append(repo)

            return repos
        except requests.exceptions.RequestException as e:
            print(f"❌ GitHub API Error: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []

    def get_trending_topics(self):
        """Holt trending education topics mit Rate-Limit-Handling"""
        topics = ["education", "learning", "pedagogy", "edtech"]
        trending = {}

        for topic in topics:
            # Check token before each request
            self._check_and_refresh_token()

            url = f"{self.base_url}/search/repositories"
            params = {
                "q": f"topic:{topic}",
                "sort": "updated",
                "order": "desc",
                "per_page": 5,
            }

            try:
                response = requests.get(
                    url, headers=self.headers, params=params, timeout=10
                )

                # Update rate limits
                self._update_rate_limits(response)

                if response.status_code == 403:
                    print(f"⚠️  Rate limit exceeded for topic: {topic}")
                    continue

                response.raise_for_status()
                data = response.json()
                trending[topic] = [
                    {
                        "name": item["name"],
                        "stars": item["stargazers_count"],
                        "url": item["html_url"],
                    }
                    for item in data.get("items", [])
                ]
            except requests.exceptions.RequestException as e:
                print(f"❌ Topic {topic} error: {e}")
            except Exception as e:
                print(f"❌ Unexpected error for {topic}: {e}")

        return trending

    def explore_all(self):
        """Sammelt alle GitHub Daten"""
        all_data = {
            "repositories": {},
            "trending": {},
            "timestamp": datetime.now().isoformat(),
        }

        print("🔍 GitHub API Exploration...")

        for query in self.search_queries:
            print(f"\n🔎 Query: {query}")
            repos = self.search_repositories(query, max_results=5)
            all_data["repositories"][query] = repos
            print(f"  ✅ {len(repos)} Repositories gefunden")

        print("\n📈 Trending Topics...")
        all_data["trending"] = self.get_trending_topics()

        return all_data

    def save_results(self, data, filename="5d_github_data.json"):
        """Speichert GitHub Daten"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Gespeichert: {filename}")


if __name__ == "__main__":
    # Optional: Setze GITHUB_TOKEN für höhere Rate Limits
    # export GITHUB_TOKEN=ghp_your_token_here
    import os

    token = os.getenv("GITHUB_TOKEN")

    explorer = GitHubExplorer(token=token)
    github_data = explorer.explore_all()
    explorer.save_results(github_data)

    total_repos = sum(len(repos) for repos in github_data["repositories"].values())
    print(f"\n📊 Total: {total_repos} Repositories analysiert")
