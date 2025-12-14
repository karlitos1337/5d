## 2024-05-23 - Missing Timeouts in External Requests
**Vulnerability:** External HTTP requests in authentication flow lacked timeouts.
**Learning:** Default behavior of `requests` library is to hang indefinitely, which can lead to DoS if external services (like GitHub) are unresponsive.
**Prevention:** Always enforce timeouts on all external network calls using `timeout=N` parameter.
