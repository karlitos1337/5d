## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.

## 2026-02-18 - [Insecure Default Proxy Binding]
**Vulnerability:** The local development proxy `owid_proxy.py` was binding to `0.0.0.0` by default, exposing it to the network. It also leaked exception details in error responses and lacked security headers.
**Learning:** Default configurations for development tools often prioritize convenience (access from anywhere) over security, creating risks if deployed or run in shared environments.
**Prevention:** Always bind to `127.0.0.1` by default for local tools. Sanitize all error messages sent to clients. Enforce security headers even in dev tools to match production expectations.
