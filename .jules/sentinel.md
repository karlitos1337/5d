## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2024-05-23 - [OWID Proxy Server Hardening]
**Vulnerability:** The internal OWID Proxy script (`owid_proxy.py`) bound to `0.0.0.0` by default, lacked essential security headers (CSP, X-Frame-Options, NOSNIFF), and leaked raw exception messages directly to clients on errors (502).
**Learning:** Development tools and proxy servers often have overly permissive defaults which pose severe security risks if accidentally or intentionally exposed to external networks.
**Prevention:** Always bind proxy and development servers to `127.0.0.1` by default (allowing override via environment variables), log raw exceptions to `stderr`, return generic sanitized errors to clients, and explicitly set robust security headers regardless of the internal nature of the tool.
