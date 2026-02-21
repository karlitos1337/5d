## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2026-02-21 - [Unsafe Default Binding in Dev Proxy]
**Vulnerability:** The `owid_proxy.py` development server bound to `0.0.0.0` by default, potentially exposing the proxy to external networks if the developer's machine is directly connected to the internet. It also leaked raw exception messages to the client.
**Learning:** Development tools often default to convenience (binding to all interfaces) over security. "It's just a dev tool" is a common justification for lax security that can lead to real-world exposure.
**Prevention:** Changed default bind to `127.0.0.1` with an optional env var override. Implemented generic error messages for the client while logging details to stderr.
