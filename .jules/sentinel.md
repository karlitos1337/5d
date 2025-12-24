## 2024-05-24 - [Missing Timeouts in GitHub OAuth]
**Vulnerability:** The `exchange_code_for_token` and `verify_user_exists` methods in `auth/github_oauth.py` used `requests.post` and `requests.get` without a `timeout` parameter. This could lead to indefinite hanging if the GitHub API becomes unresponsive (DoS risk).
**Learning:** Even in helper classes or "future use" code, external network calls must always have timeouts to prevent resource exhaustion.
**Prevention:** Added `timeout=10` to all `requests` calls in `auth/github_oauth.py`. Added a unit test to enforce this pattern.

## 2025-05-24 - [Insecure Dev Proxy Binding]
**Vulnerability:** The `web/5d-map/owid_proxy.py` development proxy bound to `0.0.0.0`, exposing an unauthenticated proxy to the entire network. It also leaked exception details in HTTP 500 responses and suppressed all access logs.
**Learning:** Development tools often default to insecure convenience (0.0.0.0) but can be easily scanned and exploited if running in a shared environment.
**Prevention:** Changed binding to `127.0.0.1` (localhost only). Replaced raw exception dump with generic 502 error message. Restored standard logging for auditability.
