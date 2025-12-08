# TODO - Infrastructure & Deployment
**Last Updated:** 2025-12-09
**Progress:** 13/15 Complete (87%)

## 🎯 NEW: OPTIMIZATION ROADMAP (5 Phases)

### ✅ PHASE 0: COMPLETED (Foundation)
- [x] Streamlit Dashboard (10 pages, 100%)
- [x] GitHub Actions CI/CD
- [x] Research scraper (arXiv, PubMed, World Bank)
- [x] Testing framework setup

### 🔥 PHASE 1: Cleanup & Foundation (DIESE WOCHE - In Progress)
- [ ] Remove duplicate files (5d_research_scraper.py.backup)
- [ ] Consolidate dependencies (requirements.txt)
- [ ] Disable broken WHO API with TODO marker
- [ ] Remove unused files (empty '5d' file)
- [ ] Update documentation

### ⚡ PHASE 2: Caching Layer (DIESE WOCHE)
- [ ] Implement Redis/SQLite cache
- [ ] Cache TTL: 30 days for WHO/World Bank
- [ ] Cache metrics in dashboard

### 🚀 PHASE 3: Async & Speed (NÄCHSTE WOCHE)
- [ ] Migrate to aiohttp (5-10x speedup)
- [ ] Token bucket rate limiter
- [ ] Parallel API calls

### 💾 PHASE 4: Database Migration (WOCHE 3)
- [ ] SQLite schema design
- [ ] JSON → SQLite migration
- [ ] SQLAlchemy ORM

### 🧪 PHASE 5: Testing & Quality (WOCHE 3-4)
- [ ] 80%+ test coverage
- [ ] Bandit security scanning
- [ ] MyPy type checking
- [ ] Performance regression tests

---

## 📋 ORIGINAL TODO ITEMS (Keep for reference)

### Infrastructure (2 remaining)
- [ ] Set up monitoring/alerting (Sentry/DataDog)
- [ ] Production deployment on cloud platform

### Documentation
- [x] README.md
- [x] CONTRIBUTING.md
- [x] CODE_OF_CONDUCT.md
- [x] VISION.md
- [ ] API documentation (in progress)
- [ ] Architecture diagrams

### Testing
- [x] Basic test framework
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Load testing

### Security
- [x] Pre-commit hooks
- [ ] Dependency scanning (Dependabot)
- [ ] Secrets management (Vault/SOPS)

### Performance
- [ ] Profiling analysis
- [ ] Database query optimization
- [ ] Caching strategy
- [ ] CDN setup for static assets

---

**See TODO_MULTIPAGE.md** for dashboard-specific tasks (100% complete!)
**See TODO_RESEARCH.md** for scientific validation tasks (85+ items)
