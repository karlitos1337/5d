## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2024-05-24 - DOM-based XSS via Unsanitized Markdown Parsing
**Vulnerability:** Client-side Cross-Site Scripting (XSS) in `web/templates/5d_forschungsplanung.html` where AI responses (Google Gemini) were parsed by `marked` and directly injected via `innerHTML`.
**Learning:** External or AI-generated content returned via API calls was implicitly trusted by the frontend, allowing potential malicious payloads to be executed in the user's browser context.
**Prevention:** Always treat API and AI responses as untrusted input. Use a dedicated HTML sanitization library like DOMPurify (e.g., `DOMPurify.sanitize(marked.parse(text))`) before assigning to `innerHTML`, or use safer DOM APIs like `textContent`.
