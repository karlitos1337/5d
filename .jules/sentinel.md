## 2024-05-22 - Local Proxy Security
**Vulnerability:** The local development proxy `owid_proxy.py` was binding to `0.0.0.0`, exposing it to the entire network and potentially allowing unauthorized access or SSRF if the whitelist wasn't strict.
**Learning:** Development tools often default to permissive bindings for convenience, but this creates security risks even in local environments.
**Prevention:** Always explicitly bind local servers and proxies to `127.0.0.1` unless external access is strictly required. Use environment variables to allow overrides.
