## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2026-01-14 - [Unbounded Read in OWID Proxy]
**Vulnerability:** The `owid_proxy.py` script read upstream responses entirely into memory using `resp.read()` without a size limit. This exposed the service to memory exhaustion DoS attacks via large files.
**Learning:** Proxy services must always assume upstream content is untrusted in size. Streaming or chunked reading with explicit limits is mandatory.
**Prevention:** Implemented a chunked read loop with a 10MB `MAX_RESPONSE_SIZE` limit. Added a test case simulating infinite streams.
