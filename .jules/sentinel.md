## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2025-05-27 - [DoS via Unbounded Reads in Proxy]
**Vulnerability:** The `owid_proxy.py` read the entire response body into memory using `resp.read()` without a size limit. This allows an attacker (or a misbehaving server) to cause a Denial of Service by sending a massive response, exhausting the server's memory.
**Learning:** Never trust the size of a response from an external source. Proxies must always stream data or enforce strict size limits.
**Prevention:** Implemented a 10MB `MAX_RESPONSE_SIZE` and used chunked reading (`resp.read(8192)`). If the size exceeds the limit, the connection is terminated securely.
