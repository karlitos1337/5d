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
## 2024-05-24 - [DOM-based XSS when parsing Markdown]
**Vulnerability:** User input from the Gemini API was passed directly to `marked.parse(text)` and assigned to `innerHTML`. This causes a DOM-based Cross-Site Scripting (XSS) vulnerability, as an attacker controlling the API output could return malicious HTML/JavaScript tags that bypass Markdown escaping.
**Learning:** `marked.parse()` does not sanitize HTML by default. Directly injecting its output via `innerHTML` is inherently unsafe.
**Prevention:** Always use a dedicated sanitization library like DOMPurify when assigning external or user-provided data to `innerHTML`. Wrap the parser call, e.g., `DOMPurify.sanitize(marked.parse(text))`.
## 2026-01-29 - [Unsecured Development Proxy]
**Vulnerability:** The `owid_proxy.py` script lacked response size limits (DoS risk), leaked exception details in 502 responses (Info Leak), and missed `X-Content-Type-Options` headers.
**Learning:** Development tools (proxies) often bypass standard security checks but end up in production-like environments.
**Prevention:** Enforced 10MB limit with chunked reading and sanitized error messages in the proxy handler. Added regression tests `tests/test_owid_proxy_security.py`.
## 2026-03-24 - [Fix DOM-based XSS vulnerabilities in bewusstsein_evolution]
**Vulnerability:** The application used `innerHTML` to dynamically generate sliders and lists in `.streamlit/static/bewusstsein_evolution.html` and `web/bewusstsein_evolution.html` (e.g. `updateDimensionSliders`, `updateFutureExplanation`, and `updateExplanation`).
**Learning:** Using `innerHTML` to generate UI based on dynamic variables or calculations is vulnerable to DOM-based XSS attacks, even if the input seems partially controlled, because it lacks auto-escaping for HTML entities.
**Prevention:** Avoid `innerHTML` entirely for DOM element creation. Instead, use native DOM manipulation such as `document.createElement`, `textContent`, and `appendChild` which are inherently safer against code injection.
