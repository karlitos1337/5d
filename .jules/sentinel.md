## 2024-05-23 - [Input Validation for API Parameters]
**Vulnerability:** The `fetch_who_mental_health_data` and `fetch_world_bank_education_data` methods in `5d_research_scraper.py` accepted raw country codes and used them directly in OData queries and URL paths without validation. While `requests` handles basic URL encoding, this could potentially allow for injection or malformed requests if user input were passed directly.
**Learning:** Even internal helper classes that fetch data from external APIs should treat their inputs as untrusted, especially when constructing complex query strings like OData filters.
**Prevention:** I added a `_validate_country_code` method to strictly check for 3-letter uppercase ISO3 codes and filter out any invalid inputs before they reach the API call logic.

## 2025-05-20 - [Denial of Service via Hanging Requests]
**Vulnerability:** The `GitHubAuth` class in `auth/github_oauth.py` made external HTTP requests using `requests.post` and `requests.get` without specifying a `timeout`.
**Learning:** Default behavior of the `requests` library is to wait indefinitely for a response. In an authentication flow, this can lead to a Denial of Service (DoS) if the external provider (GitHub) hangs or the network connection is dropped but not closed, tying up worker threads indefinitely.
**Prevention:** Added a `timeout=10` parameter to all `requests` calls in the authentication module to ensure connections fail fast (10 seconds) rather than hanging. Added a specific security regression test `tests/test_github_oauth_security.py` to enforce this pattern.
