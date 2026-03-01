## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.

## 2025-12-26 - [Uncontrolled Recursion in External API Integration]
**Vulnerability:** The `search_repositories` method in `5d_github_api.py` called itself recursively upon receiving a 403 Rate Limit response from GitHub, without tracking the retry count. This could lead to indefinite recursion and stack exhaustion (DoS) if the endpoint consistently returns a 403.
**Learning:** External API call retries, especially recursive ones, must always have a hard limit to prevent infinite loops and resource exhaustion when the external service is unavailable or rejecting requests.
**Prevention:** Added a `_retries` parameter to track retry count and limited recursive calls to a maximum of 1 retry.
