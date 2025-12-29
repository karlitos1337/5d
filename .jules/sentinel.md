## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2025-12-29 - [Development Proxy Exposed to Network]
**Vulnerability:** The `web/5d-map/owid_proxy.py` bound the server to `0.0.0.0`, exposing the development proxy to the entire network. Additionally, it lacked a response size limit, making it vulnerable to DoS via memory exhaustion.
**Learning:** Development tools often default to convenient but insecure configurations. Explicitly bind to loopback addresses (`127.0.0.1`) and enforce limits on data processing even in dev tools.
**Prevention:** Changed binding to `127.0.0.1` and implemented a 10MB Content-Length check and read limit.
