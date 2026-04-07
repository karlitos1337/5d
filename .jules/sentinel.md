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

## 2025-10-24 - [Unconstrained Upstream Response DoS and Info Leak in OWID Proxy]
**Vulnerability:** The `ProxyHandler` in `docs/5d-map/owid_proxy.py` read the entire upstream response into memory at once without any size limits, opening the server to DoS attacks. It also leaked raw exception strings to the client in the 502 error response.
**Learning:** Always use chunked reading and enforce `MAX_RESPONSE_SIZE` when proxying external data. Never expose raw internal exceptions or stack traces to the client, as they may leak sensitive information. Always add security headers like `X-Content-Type-Options: nosniff`.
**Prevention:** Implemented chunked reading with a 10MB limit and generic error messages in `docs/5d-map/owid_proxy.py`. Added the `X-Content-Type-Options: nosniff` header.
## 2026-03-22 - [Security Theater in Client-Side API Key Storage]
**Vulnerability:** The application used CryptoJS to encrypt a user-provided API key with a hardcoded passphrase before storing it in `localStorage`. This provides zero real security, as the passphrase is right there in the source code.
**Learning:** Avoid "security theater." If a client-side application needs to store an API key locally, trying to encrypt it with a hardcoded key only adds false confidence and complexity. Store user-provided keys directly in `localStorage` or `sessionStorage` (with warnings to the user about device security), or rely on a proper backend proxy to manage secrets.
**Prevention:** Removed CryptoJS and the hardcoded passphrase, storing the key plainly in `localStorage`. Added a guideline to avoid security theater for client-side secrets.
