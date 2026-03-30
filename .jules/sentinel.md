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
## 2025-05-24 - [DoS Risk from Unconstrained Upstream Proxy Fetches]
**Vulnerability:** The OWID CSV proxy server (`docs/5d-map/owid_proxy.py`) fetched entire remote files using `resp.read()` without any file size limits. A malicious or compromised upstream server could respond with an infinite stream of data, exhausting the proxy server's memory and crashing the application (Denial of Service). It also leaked internal fetch error details directly to the client.
**Learning:** Never assume upstream APIs will always return data of a reasonable size. All network proxies must enforce strict bounds on the amount of data they buffer into memory before sending it downstream.
**Prevention:** Implemented a chunked read loop (`resp.read(CHUNK_SIZE)`) with a strict `MAX_RESPONSE_SIZE` limit of 10MB in `docs/5d-map/owid_proxy.py` and `web/5d-map/owid_proxy.py`. Replaced detailed error messages with generic client responses while logging exact details internally.
