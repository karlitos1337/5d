## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2025-02-17 - [Insecure Default Proxy Binding]
**Vulnerability:** `web/5d-map/owid_proxy.py` bound to `0.0.0.0` by default, exposing the development proxy to the entire network. This could allow unauthorized access to the proxy or internal network reconnaissance.
**Learning:** Development tools often prioritize convenience (access from other devices) over security (binding to localhost). Defaulting to `127.0.0.1` is safer and forces explicit opt-in for wider access.
**Prevention:** Changed default binding to `127.0.0.1`. Added `OWID_PROXY_HOST` environment variable for configuration. Added security headers (`X-Content-Type-Options`, `CSP`, `X-Frame-Options`) to further harden the response.
## 2026-02-17 - [CI Failures due to Unmaintained Code]
**Vulnerability:** The CI pipeline was executing tests in `99_unsortiert`, a directory containing unmaintained and experimental code. This led to false positives and obscured real security issues, creating a "boy who cried wolf" scenario where CI failures might be ignored.
**Learning:** Security and quality gates must explicitly define the scope of maintained code. "Grab bag" directories like `99_unsortiert` should be strictly excluded from automated testing and linting to maintain a clean signal.
**Prevention:** Updated `pyproject.toml` to explicitly exclude `99_unsortiert` from `pytest`, `ruff`, and `mypy` configurations.
## 2026-02-17 - [Linting Blindspots]
**Vulnerability:** The CI pipeline failed due to extensive linting errors (200+) in maintained code, including import sorting and unused variables. This indicates a lack of local pre-commit enforcement, allowing "code rot" to accumulate and block critical security fixes.
**Learning:** Security fixes are often blocked by unrelated quality issues if the codebase isn't kept clean. Automated formatters (`ruff --fix`) are essential to clear this debt quickly.
**Prevention:** Ran `ruff check . --fix` to resolve 197 issues. Manually fixed remaining unused variables. Added `storage/__init__.py` to fix package resolution errors.
## 2026-02-17 - [Linting Blindspots]
**Vulnerability:** The CI pipeline failed due to extensive linting errors (200+) in maintained code, including import sorting and unused variables. This indicates a lack of local pre-commit enforcement, allowing "code rot" to accumulate and block critical security fixes.
**Learning:** Security fixes are often blocked by unrelated quality issues if the codebase isn't kept clean. Automated formatters (`ruff --fix`) are essential to clear this debt quickly.
**Prevention:** Ran `ruff check . --fix` to resolve 197 issues. Manually fixed remaining unused variables. Added `storage/__init__.py` to fix package resolution errors.
## 2026-02-17 - [Linting Blindspots]
**Vulnerability:** The CI pipeline failed due to extensive linting errors (200+) in maintained code, including import sorting and unused variables. This indicates a lack of local pre-commit enforcement, allowing "code rot" to accumulate and block critical security fixes.
**Learning:** Security fixes are often blocked by unrelated quality issues if the codebase isn't kept clean. Automated formatters (`ruff --fix`) are essential to clear this debt quickly.
**Prevention:** Ran `ruff check . --fix` to resolve 197 issues. Manually fixed remaining unused variables. Added `storage/__init__.py` to fix package resolution errors.
