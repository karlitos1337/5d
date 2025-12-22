## 2025-10-27 - [Enforcing HTTPS on External APIs]
**Vulnerability:** The `ResearchScraper` was using cleartext HTTP (`http://export.arxiv.org`) to query the arXiv API.
**Learning:** Even when fetching public data, using HTTP allows for Man-in-the-Middle (MITM) attacks that could modify the response data (integrity risk) or leak the query parameters (confidentiality risk). Simple scripts often copy-paste old examples using HTTP.
**Prevention:** Always verify API endpoints use `https://`. Use tools like `grep` to scan for `http://` in codebase.
