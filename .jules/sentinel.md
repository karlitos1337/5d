## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2026-03-16 - [Fix DOM-based XSS vulnerabilities in 5d-map UI]
**Vulnerability:** Multiple instances of `innerHTML` assignment were used in `web/5d-map/app.js` and `web/5d-map/modules/layers.js` to dynamically generate map UI elements like legends and counters. This exposes the application to DOM-based XSS if user inputs or untrusted API responses are rendered without sanitization.
**Learning:** Even internal filtering mechanisms or simple map UI components are vulnerable when data flow isn't inherently safe.
**Prevention:** Avoid `innerHTML` for DOM element construction. Instead, use safe native DOM manipulation functions (`document.createElement`, `textContent`, `appendChild`) to build elements dynamically.
