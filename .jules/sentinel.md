## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.

## 2025-05-27 - [Weak Content Security Policy due to Inline Scripts]
**Vulnerability:** The `web/5d-map/index.html` file contained inline scripts and styles, necessitating `unsafe-inline` in the CSP `script-src` directive. This weakened protection against XSS attacks.
**Learning:** Extracting inline scripts into modules (e.g., `init.js`) enables a strict `script-src 'self'` policy. However, libraries like Leaflet still require `unsafe-inline` in `style-src` for dynamic positioning.
**Prevention:** Moved inline JS to `web/5d-map/init.js` and CSS to `web/5d-map/styles.css`. Updated CSP to remove `unsafe-inline` from `script-src` and allow specific connect sources.
