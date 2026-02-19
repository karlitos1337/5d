## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.

## 2026-02-19 - Insecure Default Proxy Binding
**Vulnerability:** The `owid_proxy.py` script was binding to `0.0.0.0` by default, exposing the proxy service to all network interfaces.
**Learning:** Development tools often default to "convenient" bindings (0.0.0.0) which are insecure. The code explicitly used `("0.0.0.0", port)`.
**Prevention:** Always bind to `127.0.0.1` (localhost) by default for local development tools. Use environment variables to override if external access is strictly necessary.

## 2026-02-19 - CI Failure Remediation
**Vulnerability:** Inconsistent CI environment configuration and improper submodule handling caused build failures. Invalid escape sequences in strings were deprecated.
**Learning:**
1.  Git submodules must be properly configured or removed from the index to avoid  errors in CI.
2.   files are essential for Python package discovery, even in root-level directories like .
3.  Strings containing backslashes (e.g., LaTeX formulas , escaped characters ) must be raw strings () to avoid  (which can become errors).
**Prevention:**
1.  Use  for directories that should not be submodules.
2.  Ensure  exists in all Python source directories.
3.  Use raw strings for regex and LaTeX-heavy docstrings.

## 2026-02-19 - CI Failure Remediation
**Vulnerability:** Inconsistent CI environment configuration and improper submodule handling caused build failures. Invalid escape sequences in strings were deprecated.
**Learning:**
1.  Git submodules must be properly configured or removed from the index to avoid `fatal: No url found` errors in CI.
2.  `__init__.py` files are essential for Python package discovery, even in root-level directories like `storage`.
3.  Strings containing backslashes (e.g., LaTeX formulas `\sigma`, escaped characters `\&`) must be raw strings (`r"..."`) to avoid `SyntaxWarning` (which can become errors).
**Prevention:**
1.  Use `git rm --cached` for directories that should not be submodules.
2.  Ensure `__init__.py` exists in all Python source directories.
3.  Use raw strings for regex and LaTeX-heavy docstrings.
