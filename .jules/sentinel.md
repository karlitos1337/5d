## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2025-01-08 - [XSS via Third-Party Markdown Parsing]
**Vulnerability:** The Gemini API response parsing in `web/templates/5d_forschungsplanung.html` used `marked.parse(text)` directly injected via `innerHTML`. This exposes the application to DOM-based XSS if the AI returns malicious HTML.
**Learning:** Never trust inputs from external APIs, including LLMs. Always sanitize Markdown output before inserting it into the DOM, especially when using `innerHTML`.
**Prevention:** Imported `DOMPurify` and wrapped `marked.parse(text)` with `DOMPurify.sanitize()` prior to DOM injection.
## 2025-02-14 - [DoS Risk in OWID Proxy via Unconstrained Response Reads]
**Vulnerability:** The proxy in `docs/5d-map/owid_proxy.py` read upstream responses into memory using `resp.read()` without any limit, exposing the server to Denial-of-Service (DoS) via OOM errors. It also leaked upstream exception details.
**Learning:** Python's `urllib` defaults to reading the whole response into memory if size limits are not explicitly enforced. Error details should also not be sent in the response body.
**Prevention:** Implemented a chunked read approach with a 10MB `MAX_RESPONSE_SIZE` limit and scrubbed error messages.
