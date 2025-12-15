## 2024-05-23 - [Input Validation for API Parameters]
**Vulnerability:** The `fetch_who_mental_health_data` and `fetch_world_bank_education_data` methods in `5d_research_scraper.py` accepted raw country codes and used them directly in OData queries and URL paths without validation. While `requests` handles basic URL encoding, this could potentially allow for injection or malformed requests if user input were passed directly.
**Learning:** Even internal helper classes that fetch data from external APIs should treat their inputs as untrusted, especially when constructing complex query strings like OData filters.
**Prevention:** I added a `_validate_country_code` method to strictly check for 3-letter uppercase ISO3 codes and filter out any invalid inputs before they reach the API call logic.
