## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2026-02-06 - [DoS Vulnerability in Custom HTTP Proxy]
**Vulnerability:** The `owid_proxy.py` used `urllib.request.urlopen(url).read()` inside a custom `BaseHTTPRequestHandler`, which loads the entire response into memory. This creates a Denial of Service (DoS) risk if the upstream server returns a large file.
**Learning:** Custom proxies using `BaseHTTPRequestHandler` and `urllib` must manually implement chunked reading and size limits (`MAX_RESPONSE_SIZE`) to prevent memory exhaustion.
**Prevention:** Refactored `owid_proxy.py` to use a 10MB limit and chunked reading. Added `tests/test_owid_proxy_security.py` to enforce this constraint and check for info leakage.
