## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.

## 2026-02-24 - [Insecure Default Binding and Headers in Proxy]
**Vulnerability:** The `web/5d-map/owid_proxy.py` script bound to `0.0.0.0` by default and leaked upstream error details in HTTP 502 responses. It also lacked standard security headers (CSP, HSTS, etc.).
**Learning:** Development proxies often prioritize convenience over security. Always bind to `127.0.0.1` by default and sanitize error messages to prevent information leakage.
**Prevention:** Changed default binding to localhost (configurable via env var). Added security headers and error sanitization to both web and docs versions of the proxy.
