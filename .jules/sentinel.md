## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.
## 2025-12-26 - [Insecure HTTP Usage in Research Scraper]
**Vulnerability:** The `5d_research_scraper.py` script used an insecure HTTP URL (`http://export.arxiv.org`) for the arXiv API. This could allow Man-in-the-Middle (MitM) attacks to intercept or modify research data.
**Learning:** Always verify if external APIs support HTTPS and enforce it. Even for public data, integrity is crucial.
**Prevention:** Changed the URL to `https://export.arxiv.org`. Added a test case to verify HTTPS usage for API endpoints.
## 2024-03-04 - [Command Injection Risk in sitedorks]
**Vulnerability:** The `external/sources/sitedorks-master/sitedorks.py` script used `subprocess.check_output` with `shell=True` and a string command. Although the specific command did not use unsanitized variables directly, `shell=True` poses a high risk of command injection if arguments are ever added dynamically, and is generally bad practice. Additionally, the subprocess did not have a timeout, which could hang indefinitely if `bbrecon` hangs.
**Learning:** Avoid `shell=True` wherever possible to follow the principle of least privilege and prevent command injection. External processes should have a timeout to prevent resource exhaustion and hanging execution.
**Prevention:** Replaced `shell=True` with `shell=False` by using a list of arguments (`["bbrecon", "get", "programs", "--type", "web", "-o", "json"]`). Added `timeout=60` to ensure the subprocess terminates if unresponsive.
