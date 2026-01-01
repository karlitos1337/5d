## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2026-01-01 - [Insecure Proxy Configuration]
**Vulnerability:** The `web/5d-map/owid_proxy.py` development proxy was binding to `0.0.0.0` (all interfaces) and lacked a response size limit. This exposed the proxy to external network access and potential Denial of Service (DoS) via memory exhaustion if the upstream server returned a large response.
**Learning:** Development tools often default to insecure configurations (like binding to all interfaces) for convenience. Always restrict binding to `127.0.0.1` unless external access is explicitly required and secured.
**Prevention:** Changed binding to `127.0.0.1` and implemented a 10MB response size limit with chunked reading to prevent memory exhaustion.
