# 5D Intelligence Framework – API Documentation

**Version:** 2.0  
**Last Updated:** December 2, 2025

Diese Dokumentation beschreibt die JSON-Schnittstellen, externe API-Integrationen und Datenformate des 5D-Projekts.

## 📋 Inhaltsverzeichnis

- [Überblick](#überblick)
- [JSON Data Contracts](#json-data-contracts)
- [Pipeline Outputs](#pipeline-outputs)
- [External APIs](#external-apis)
- [Pydantic Schemas](#pydantic-schemas)
- [Configuration](#configuration)
- [Rate Limiting](#rate-limiting)
- [Authentication](#authentication)
- [Error Handling](#error-handling)

## 🔍 Überblick

### Architektur

```
5d_extractor.py → 5d_solutions.json
                      ↓
5d_research_scraper.py → 5d_research_data.json
                      ↓
5d_github_api.py → 5d_github_data.json
                      ↓
              5d_dashboard.py (Streamlit)
              web/5d-map/ (Leaflet.js)
```

**Prinzip:** JSON-Dateien sind die stabilen Verträge zwischen Pipeline-Stages. Keys dürfen **nicht** ohne Team-Genehmigung umbenannt werden.

## 📄 JSON Data Contracts

### 1. 5d_solutions.json

**Producer:** `5d_extractor.py`  
**Schema:** `models/schemas.py::ProjectSolution`

```json
{
  "solutions": [
    {
      "name": "Example School",
      "category": "Alternative Education",
      "dimensions": {
        "A": 0.75,
        "IM": 0.70,
        "R": 0.65,
        "SP": 0.80,
        "Au": 0.68
      },
      "imp_score": 0.179,
      "description": "Short description",
      "location": "Berlin, Germany",
      "coordinates": {
        "lat": 52.5200,
        "lon": 13.4050
      },
      "source_file": "manifest/01_bildung_education/example.md",
      "references": [
        "https://example.org",
        "doi:10.1234/example"
      ]
    }
  ],
  "metadata": {
    "extraction_date": "2025-12-02T10:30:00",
    "total_solutions": 42,
    "manifest_version": "2.1",
    "extractor_version": "1.0.0"
  }
}
```

**Key Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Unique solution name |
| `category` | string | ✅ | Classification (e.g., "Alternative Education") |
| `dimensions` | object | ✅ | 5D scores (A, IM, R, SP, Au) normalized [0,1] |
| `imp_score` | float | ✅ | Multiplicative IMP = A × IM × R × SP × Au |
| `location` | string | ❌ | Human-readable location |
| `coordinates` | object | ❌ | `{lat: float, lon: float}` |
| `source_file` | string | ✅ | Path to manifest file |
| `references` | array | ❌ | URLs, DOIs, BibTeX keys |

### 2. 5d_research_data.json

**Producer:** `5d_research_scraper.py`  
**Schema:** `models/schemas.py::ResearchPaper`

```json
{
  "papers": [
    {
      "title": "The Impact of Intrinsic Motivation on Learning",
      "authors": ["Smith, J.", "Doe, A."],
      "abstract": "This study examines...",
      "publication_date": "2024-03-15",
      "doi": "10.1234/example.2024.001",
      "arxiv_id": "2403.12345",
      "pubmed_id": "38123456",
      "url": "https://arxiv.org/abs/2403.12345",
      "keywords": ["intrinsic motivation", "education", "flow"],
      "dimension_relevance": {
        "IM": 0.95,
        "A": 0.60,
        "R": 0.30
      },
      "citation_count": 42,
      "source": "arXiv"
    }
  ],
  "metadata": {
    "scrape_date": "2025-12-02T11:00:00",
    "total_papers": 156,
    "sources": ["arXiv", "PubMed"],
    "scraper_version": "1.0.0"
  }
}
```

**Key Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | ✅ | Paper title |
| `authors` | array | ✅ | List of author names |
| `abstract` | string | ❌ | Paper abstract |
| `doi` | string | ❌ | Digital Object Identifier |
| `arxiv_id` | string | ❌ | arXiv identifier |
| `pubmed_id` | string | ❌ | PubMed ID |
| `dimension_relevance` | object | ❌ | Relevance scores per dimension [0,1] |
| `citation_count` | integer | ❌ | Number of citations |
| `source` | string | ✅ | "arXiv", "PubMed", "WHO", "World Bank" |

### 3. 5d_github_data.json

**Producer:** `5d_github_api.py`  
**Schema:** `models/schemas.py::GitHubRepo`

```json
{
  "repositories": [
    {
      "name": "edtech-platform",
      "full_name": "organization/edtech-platform",
      "description": "Open source education platform",
      "url": "https://github.com/organization/edtech-platform",
      "stars": 1234,
      "forks": 567,
      "watchers": 890,
      "language": "Python",
      "created_at": "2023-01-15T10:30:00Z",
      "updated_at": "2025-11-30T14:20:00Z",
      "topics": ["education", "open-source", "learning"],
      "license": "MIT",
      "dimension_tags": ["A", "IM"],
      "is_active": true
    }
  ],
  "metadata": {
    "fetch_date": "2025-12-02T12:00:00",
    "total_repositories": 89,
    "api_version": "v3",
    "rate_limit_remaining": 4950
  }
}
```

**Key Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Repository name |
| `full_name` | string | ✅ | `owner/repo` |
| `url` | string | ✅ | GitHub URL |
| `stars` | integer | ✅ | Star count |
| `language` | string | ❌ | Primary language |
| `topics` | array | ❌ | Repository topics |
| `dimension_tags` | array | ❌ | Related 5D dimensions |
| `is_active` | boolean | ✅ | Updated in last 12 months |

### 4. baseline.json (5D-Map)

**Location:** `web/5d-map/data/baseline.json`  
**Purpose:** Fallback data for time-travel feature

```json
{
  "version": "2.1",
  "last_updated": "2025-12-01",
  "countries": {
    "DEU": {
      "name": "Germany",
      "depression_rate": 5.2,
      "dropout_rate": 10.3,
      "wgi_governance": 1.57,
      "imp_proxy": 0.68,
      "data_year": 2023,
      "confidence": "high",
      "sources": {
        "depression": "OWID/IHME GBD 2019",
        "dropout": "World Bank EdStats",
        "governance": "World Bank WGI"
      }
    }
  },
  "formulas": {
    "imp_proxy": "IMP_proxy = (1 - depression/15) × (1 - dropout/30) × ((wgi+2.5)/5)",
    "normalization": {
      "depression": "Max 15% (severe)",
      "dropout": "Max 30% (critical)",
      "wgi": "Range [-2.5, +2.5] → [0, 1]"
    }
  }
}
```

## 🌐 External APIs

### 1. arXiv API

**Endpoint:** `http://export.arxiv.org/api/query`  
**Rate Limit:** 1 request/3 seconds (recommended)  
**Authentication:** None required

```python
# Example usage in 5d_research_scraper.py
import time
import requests

BASE_URL = "http://export.arxiv.org/api/query"

params = {
    'search_query': 'all:intrinsic motivation education',
    'start': 0,
    'max_results': 10,
    'sortBy': 'relevance'
}

response = requests.get(BASE_URL, params=params)
time.sleep(3)  # Rate limiting
```

**Response Format:** XML (Atom feed)

### 2. PubMed/NCBI API

**Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`  
**Rate Limit:** 3 requests/second (without API key), 10/second (with key)  
**Authentication:** Optional API key

```python
# Example: Search PubMed
esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

params = {
    'db': 'pubmed',
    'term': 'flow state[Title/Abstract]',
    'retmax': 20,
    'retmode': 'json'
}

response = requests.get(esearch_url, params=params)
```

### 3. GitHub API

**Endpoint:** `https://api.github.com`  
**Rate Limit:** 60/hour (unauthenticated), 5000/hour (authenticated)  
**Authentication:** Bearer token

```python
# Example usage in 5d_github_api.py
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

url = 'https://api.github.com/search/repositories'
params = {
    'q': 'education topic:alternative-learning',
    'sort': 'stars',
    'per_page': 100
}

response = requests.get(url, headers=headers, params=params)
```

**Rate Limit Headers:**
- `X-RateLimit-Limit`: Total quota
- `X-RateLimit-Remaining`: Requests left
- `X-RateLimit-Reset`: Timestamp when quota resets

### 4. Our World in Data (OWID)

**Endpoint:** `https://ourworldindata.org/grapher/[indicator].json`  
**Rate Limit:** No official limit (use 1 req/sec as courtesy)  
**Authentication:** None

```javascript
// Example: Fetch depression data
const url = 'https://ourworldindata.org/grapher/depression-rates.json?tab=table';

fetch(url)
  .then(res => res.json())
  .then(data => {
    // data.variables contains indicator data
    // data.entityKey maps country codes
  });
```

### 5. World Bank API

**Endpoint:** `https://api.worldbank.org/v2/`  
**Rate Limit:** No official limit (use 1 req/sec)  
**Authentication:** None

```javascript
// Example: Fetch dropout rates
const url = 'https://api.worldbank.org/v2/country/DEU/indicator/SE.PRM.DROP.ZS?format=json&date=2020:2024';

fetch(url)
  .then(res => res.json())
  .then(data => {
    // data[1] contains indicator values
  });
```

## 🔒 Pydantic Schemas

**Location:** `models/schemas.py`

### DimensionScore

```python
from pydantic import BaseModel, Field, field_validator

class DimensionScore(BaseModel):
    dimension: str = Field(..., pattern=r'^(A|IM|R|SP|Au)$')
    score: float = Field(..., ge=0.0, le=1.0)
    source: str
    confidence: str = Field(default='medium', pattern=r'^(low|medium|high)$')
    
    @field_validator('score', mode='before')
    def parse_score(cls, v):
        """Normalize various score formats to [0, 1]."""
        if isinstance(v, str):
            if v.upper() == 'HIGH':
                return 0.75
            elif v.upper() == 'MEDIUM':
                return 0.50
            elif v.upper() == 'LOW':
                return 0.25
            else:
                v = float(v)
        
        # Clamp to [0, 1]
        return max(0.0, min(1.0, float(v)))
```

### ProjectSolution

```python
class ProjectSolution(BaseModel):
    name: str
    category: str
    dimensions: dict[str, float]
    imp_score: float = Field(..., ge=0.0, le=1.0)
    description: str | None = None
    location: str | None = None
    coordinates: dict[str, float] | None = None
    source_file: str
    references: list[str] = Field(default_factory=list)
    
    @field_validator('dimensions')
    def validate_dimensions(cls, v):
        required = {'A', 'IM', 'R', 'SP', 'Au'}
        if not required.issubset(v.keys()):
            raise ValueError(f'Missing dimensions: {required - set(v.keys())}')
        return v
```

## ⚙️ Configuration

**Location:** `config/default.yaml`

```yaml
extractor:
  manifest_dir: "manifest"
  output_file: "5d_solutions.json"
  keywords:
    - "5D Intelligence"
    - "Alternative Education"
    - "Flow State"

research_scraper:
  rate_limit_delay: 1.0  # seconds
  max_retries: 3
  backoff_factor: 2.0
  output_file: "5d_research_data.json"
  sources:
    - arxiv
    - pubmed

github_api:
  rate_limit_delay: 0.5
  max_results: 100
  output_file: "5d_github_data.json"
  search_queries:
    - "education alternative learning"
    - "edtech open source"

dashboard:
  cache_ttl: 300  # seconds
  default_port: 8501
```

**Loading Configuration:**

```python
from config.loader import load_config

config = load_config()
manifest_dir = config['extractor']['manifest_dir']
```

## 🚦 Rate Limiting

### Implementation Pattern

```python
import time
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, delay: float = 1.0, max_retries: int = 3):
        self.delay = delay
        self.max_retries = max_retries
        self.last_request_time = None
    
    def wait(self):
        """Enforce rate limit."""
        if self.last_request_time:
            elapsed = (datetime.now() - self.last_request_time).total_seconds()
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        
        self.last_request_time = datetime.now()
    
    def fetch_with_retry(self, url: str, **kwargs):
        """Fetch with exponential backoff."""
        for attempt in range(self.max_retries):
            try:
                self.wait()
                response = requests.get(url, **kwargs)
                
                if response.status_code == 429:
                    wait_time = self.delay * (2 ** attempt)
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                return response
            
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(self.delay * (2 ** attempt))
        
        return None
```

### API-Specific Limits

| API | Unauthenticated | Authenticated | Recommendation |
|-----|-----------------|---------------|----------------|
| arXiv | 1 req/3s | 1 req/3s | 1.0s delay |
| PubMed | 3 req/s | 10 req/s | 0.5s delay |
| GitHub | 60/hour | 5000/hour | Use token |
| OWID | No limit | No limit | 1.0s courtesy |
| World Bank | No limit | No limit | 1.0s courtesy |

## 🔐 Authentication

### GitHub Token

```bash
# Set environment variable
export GITHUB_TOKEN=ghp_your_personal_access_token

# In Python
import os
token = os.getenv('GITHUB_TOKEN')

if not token:
    print("Warning: No GitHub token, rate limits apply")
```

**Creating Token:**
1. GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Scopes: `public_repo`, `read:org`

### PubMed API Key (Optional)

```bash
export PUBMED_API_KEY=your_api_key

# In Python
api_key = os.getenv('PUBMED_API_KEY')
params = {'api_key': api_key} if api_key else {}
```

## ⚠️ Error Handling

### Standard Pattern

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def fetch_data(url: str) -> Optional[dict]:
    """Fetch data with comprehensive error handling."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.Timeout:
        logger.error(f"Timeout fetching {url}")
        return None
    
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"Resource not found: {url}")
        elif e.response.status_code == 429:
            logger.error(f"Rate limit exceeded: {url}")
        else:
            logger.error(f"HTTP error {e.response.status_code}: {url}")
        return None
    
    except requests.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return None
    
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON response from {url}")
        return None
```

### Pipeline Error Handling

```python
# 5d_extractor.py
try:
    solutions = extract_solutions(manifest_dir)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, indent=2, ensure_ascii=False)
except FileNotFoundError as e:
    logger.error(f"Manifest directory not found: {e}")
    sys.exit(1)
except UnicodeDecodeError as e:
    logger.error(f"Unicode error reading file: {e}")
    sys.exit(1)
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    sys.exit(1)
```

## 📊 Usage Examples

### Full Pipeline

```bash
# 1. Extract solutions from manifest
python 5d_extractor.py
# → Creates 5d_solutions.json

# 2. Scrape research papers
python 5d_research_scraper.py
# → Creates 5d_research_data.json

# 3. Fetch GitHub repositories
export GITHUB_TOKEN=ghp_your_token
python 5d_github_api.py
# → Creates 5d_github_data.json

# 4. Launch dashboard
streamlit run 5d_dashboard.py
```

### Loading Data in Python

```python
import json
from pathlib import Path

def load_json(filepath: str) -> dict:
    """Load JSON file with error handling."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"{filepath} not found")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Usage
solutions = load_json('5d_solutions.json')
print(f"Total solutions: {solutions['metadata']['total_solutions']}")

for solution in solutions['solutions']:
    print(f"{solution['name']}: IMP = {solution['imp_score']:.3f}")
```

### Loading Data in JavaScript

```javascript
// web/5d-map/js/data-loader.js
async function loadSolutions() {
  try {
    const response = await fetch('../../../5d_solutions.json');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return data.solutions;
  } catch (error) {
    console.error('Failed to load solutions:', error);
    return [];
  }
}

// Usage
const solutions = await loadSolutions();
console.log(`Loaded ${solutions.length} solutions`);
```

## 🔄 Schema Validation

### Validating Output

```python
from pydantic import ValidationError
from models.schemas import ProjectSolution

def validate_solutions(data: dict) -> bool:
    """Validate 5d_solutions.json structure."""
    try:
        for solution in data['solutions']:
            ProjectSolution(**solution)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False

# Usage
with open('5d_solutions.json') as f:
    data = json.load(f)

if validate_solutions(data):
    print("✓ Schema valid")
else:
    print("✗ Schema validation failed")
```

### CI/CD Validation

```bash
# tests/test_schemas.py
pytest tests/test_schemas.py -v
```

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/karlitos1337/5d/issues)
- **Discussions:** [GitHub Discussions](https://github.com/karlitos1337/5d/discussions)
- **Documentation:** [docs/](../docs/)

---

**Maintainer:** 5D Intelligence Team  
**License:** MIT  
**Last Reviewed:** December 2, 2025
