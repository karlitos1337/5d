## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2025-12-26 - [DOM-based XSS Vulnerability in 5D Research Planning Dashboard]
**Vulnerability:** The `web/templates/5d_forschungsplanung.html` script used `marked.parse` to convert markdown from the Gemini AI API response and injected it directly into the DOM using `innerHTML` without sanitization. This is a severe Cross-Site Scripting (XSS) vulnerability.
**Learning:** Never trust the output of an external API, and never use `innerHTML` to inject parsed markdown (or any user-controllable input) without explicitly sanitizing it first.
**Prevention:** Included DOMPurify via CDN (`purify.min.js`) and wrapped the markdown parsing with `DOMPurify.sanitize(marked.parse(text))` before injecting it via `innerHTML`.
