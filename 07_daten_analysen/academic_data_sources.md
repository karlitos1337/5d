# 💾 Academic Data Sources – P2P Science (Academic Torrents)

**Dimension**: 07_daten_analysen  
**Cross-Reference**: 04_oekonomie_governance (Commons Science, Ostrom)  
**Datum**: 2025-12-03  
**Status**: Sprint 2 - Academic Torrents Integration

---

## 📊 Übersicht

**Problem:** Wissenschaftliche Daten zentral hosten ist teuer (S3 = $0.023/GB → 1TB = $23/Monat → 100TB = $2,300/Monat)  
**Lösung:** Academic Torrents = **P2P Commons** (Bandbreite wird geteilt, keine Server-Kosten)

---

## 🟡 Academic Torrents (P2P Science)

**URL**: https://academictorrents.com/  
**Score**: 8/10  
**Status**: ✅ LEGAL Peer-to-Peer for Science

### Features
- **TB-große Datasets via BitTorrent:** ImageNet (1.2TB), Wikipedia Dumps (20GB), arXiv Papers (1TB), MNIST (50MB), Common Crawl (800TB)
- **Akademisch legal:** Alle Datasets haben Lizenzen (CC, Public Domain, Academic Use)
- **Infrastruktur-Ersparnis:** P2P reduziert Server-Kosten (keine AWS S3 Rechnungen)
- **Community-driven:** Wie arXiv, aber dezentral (keine zentrale Autorität)

---

## 🎓 Commons-Perspektive (Ostrom)

### Problem
Wissenschaftliche Daten zentral hosten = **Common Pool Resource Problem**:
- Hohe Kosten (S3, Azure Blob)
- Vendor Lock-In (AWS kontrolliert Zugang)
- Single Point of Failure (Server down → Daten weg)

### Lösung: Academic Torrents = P2P Commons
- **Ressourcen:** Bandbreite wird geteilt (jeder Downloader wird Uploader)
- **Governance:** Community moderiert Datasets (ähnlich Wikipedia)
- **Monitoring:** Peer-Review vor Upload (keine Fake-Daten)

---

## 📋 Ostrom's 8 Prinzipien (Applied)

**Elinor Ostrom (1990):** 8 Prinzipien für nachhaltige Commons-Governance

| Prinzip | Academic Torrents | Status |
|---------|-------------------|--------|
| 1. **Clearly Defined Boundaries** | Nur wissenschaftliche Datasets (keine Piraterie) | ✅ |
| 2. **Proportional Equivalence** | Download = Upload (BitTorrent-Ratio) | ✅ |
| 3. **Collective-Choice Arrangements** | Community Vote für neue Datasets (GitHub Issues) | ✅ |
| 4. **Monitoring** | Peer-Review + MD5-Checksums (keine Korruption) | ✅ |
| 5. **Graduated Sanctions** | Fake-Uploads → Ban (Community Moderators) | ✅ |
| 6. **Conflict-Resolution** | GitHub Issues für Disputes | ✅ |
| 7. **Minimal Recognition** | Community anerkannt von arXiv, Nature | ✅ |
| 8. **Nested Enterprises** | Integration mit Zenodo, figshare, OSF | ✅ |

**Diagnose:** Academic Torrents ist **echtes Commons** (alle 8 Prinzipien erfüllt)

---

## 🔄 Vergleich: Academic Torrents vs. Zenodo

| Kriterium | Academic Torrents | Zenodo (CERN) |
|-----------|-------------------|---------------|
| **Hosting** | P2P (dezentral, Community) | Zentralserver (CERN) |
| **Kosten** | $0 (Community Bandbreite) | €100k+/Jahr (CERN Infrastructure) |
| **Max Size** | Unbegrenzt (TB+) | 50GB pro Dataset |
| **Speed** | Skaliert mit Peers (mehr Downloader = schneller) | Begrenzt durch Server (10 Gbps) |
| **Persistence** | ⚠️ Abhängig von Seeders (Gefahr: Dataset stirbt) | ✅ CERN Garantie (99.9% Uptime) |
| **DOI** | ❌ Keine permanenten Identifiers | ✅ DOIs für Zitation |

**Integration:** Beide **komplementär** → Zenodo (kleine Datasets, DOI) + Academic Torrents (TB-große Datasets)

---

## 📊 Popular Datasets

| Dataset | Size | Downloads | Use Case |
|---------|------|-----------|----------|
| **ImageNet** | 1.2TB | 500k+ | Computer Vision (CNN Training) |
| **Wikipedia Dumps** | 20GB | 100k+ | NLP (Language Models) |
| **arXiv Papers** | 1TB | 50k+ | Research (Meta-Analysis) |
| **Common Crawl** | 800TB | 10k+ | Web Scraping (LLM Training) |
| **MNIST** | 50MB | 1M+ | ML Education (Beginner Datasets) |

---

## 🎓 Integration in 5D-Framework

### 4. Ökonomie/Governance
- **Commons Science:** Academic Torrents als Ostrom-Beispiel (alle 8 Prinzipien)
- **Decentralization:** P2P vs. Zentralisierung (AWS, Google Cloud)

### 7. Datenanalysen
- **Data Sources:** Academic Torrents als primäre Quelle für TB-Datasets
- **Reproducibility:** Permanent Seeding = langfristige Verfügbarkeit (vs. Server Shutdown)

---

## 📚 BibTeX-Referenzen

```bibtex
@misc{academictorrents2025,
  title = {Academic Torrents: Distributed Scientific Data Sharing},
  author = {{Academic Torrents Community}},
  year = {2025},
  howpublished = {\url{https://academictorrents.com/}},
  note = {BitTorrent-based platform for sharing large scientific datasets, legal P2P, Ostrom Commons model}
}

@book{ostrom1990governing,
  title = {Governing the Commons: The Evolution of Institutions for Collective Action},
  author = {Ostrom, Elinor},
  year = {1990},
  publisher = {Cambridge University Press},
  note = {Foundational work on commons governance, 8 principles for sustainable commons}
}

@misc{zenodo2025,
  title = {Zenodo: Research Sharing Platform},
  author = {{CERN}},
  year = {2025},
  howpublished = {\url{https://zenodo.org/}},
  note = {CERN-hosted platform, DOIs for datasets, 50GB limit, €100k+/year infrastructure costs}
}
```

---

## 🔗 Cross-Reference Map

| Thema | Verweis | Begründung |
|-------|---------|------------|
| **Commons Governance** | `04_oekonomie_governance/commons_science.md` | Academic Torrents = P2P Commons (Ostrom) |
| **Data Sources** | `07_daten_analysen/data_sources.md` | Academic Torrents als primäre Quelle |
| **Decentralization** | `04_oekonomie_governance/decentralization.md` | P2P vs. AWS/Google Cloud |
| **Ostrom's 8 Principles** | `04_oekonomie_governance/ostrom_principles.md` | Academic Torrents erfüllt alle 8 |

---

## 🚀 Action Items

- [x] Academic Torrents dokumentiert
- [ ] BibTeX Batch 10 (academictorrents2025, zenodo2025) - Q1 2026
- [ ] Commons Science File erstellen (`04_oekonomie_governance/commons_science.md`) - Q1 2026
- [ ] Dashboard-Widget: Dataset Explorer (Top 20 Datasets visualisieren) - Q2 2026

---

**Last Updated:** 2025-12-03  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License:** CC BY 4.0
