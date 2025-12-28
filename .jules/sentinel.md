## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2025-12-26 - [Insecure Proxy Binding and DoS Risk]
**Vulnerability:** The `web/5d-map/owid_proxy.py` development proxy was bound to `0.0.0.0`, exposing it to the local network or internet if not firewalled. Additionally, it read the full response content into memory without a size limit, posing a Memory Exhaustion Denial of Service (DoS) risk.
**Learning:** Development tools often default to permissive settings (`0.0.0.0`) which can be dangerous if leakage occurs. Always explicitly bind to `127.0.0.1` unless external access is required. Unbounded reads from external sources are a classic DoS vector.
**Prevention:** Changed the bind address to `127.0.0.1` to restrict access to the local machine. Implemented a `MAX_RESPONSE_SIZE` (10MB) limit on the proxy's `read()` operation.
