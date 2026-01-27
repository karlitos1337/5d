## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.

## 2026-01-27 - [Unbounded Read in Proxy Handler]
**Vulnerability:** The `owid_proxy.py` script used `resp.read()` on an external URL without a size limit. This allows a malicious or misconfigured upstream server to cause a Denial of Service (DoS) via memory exhaustion (OOM) by sending a very large response.
**Learning:** Never trust the size of a response from an external source. Standard libraries like `urllib` often default to reading the entire stream into memory.
**Prevention:** Implemented a chunked read loop with a strict `MAX_RESPONSE_SIZE` (10MB) limit. Also enforced `X-Content-Type-Options: nosniff` and sanitized error messages to prevent information leakage.
