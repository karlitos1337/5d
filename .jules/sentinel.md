## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.

## 2024-06-25 - [DOM-based XSS in Markdown Parsing]
**Vulnerability:** The `web/templates/5d_forschungsplanung.html` file used `marked.parse(text)` directly assigned to `element.innerHTML`. This allowed any malicious markdown (like `<img src=x onerror=alert(1)>`) from the AI response or user input to execute arbitrary JavaScript.
**Learning:** Client-side markdown renderers do not sanitize output by default. Trusting AI responses or user inputs to be safe HTML is a common pitfall.
**Prevention:** Always wrap markdown parser outputs with a sanitizer like `DOMPurify.sanitize()` before injecting into the DOM, and prefer `textContent` for plain text error messages.

## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.

## 2026-02-22 - [Information Leakage in Proxy Service]
**Vulnerability:** The `web/5d-map/owid_proxy.py` script (and its documentation counterpart) leaked detailed exception messages in HTTP responses, potentially exposing internal configuration or network details. It also lacked essential security headers and bound to `0.0.0.0` by default.
**Learning:** Simple proxy scripts often overlook security headers and error sanitization, becoming an easy target for reconnaissance.
**Prevention:** Sanitized error messages to generic "Upstream fetch error". Added `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy`, and `Referrer-Policy` headers. Changed default binding to `127.0.0.1`.
