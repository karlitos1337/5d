## 2025-02-17 - Unsecure Bind Address and Missing Security Headers in Python Proxy
**Vulnerability:** The `owid_proxy.py` script was binding to `0.0.0.0` by default, exposing the proxy service to the entire network. Additionally, it lacked security headers like `X-Content-Type-Options` and `Content-Security-Policy`.
**Learning:** Simple development proxies often default to permissive bindings (`0.0.0.0`) and lack security hardening, which can be risky if deployed or run in insecure environments.
**Prevention:** Always bind to `127.0.0.1` for local development tools unless external access is explicitly required. Implement basic security headers even for simple helper scripts.
