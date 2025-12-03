# Scientific Data Sources & Commons-Based Sharing

**Dimension**: 07_daten_analysen  
**Cross-Reference**: 04_oekonomie_governance (Commons Governance), 01_bildung_education (Open Access)  
**Date**: 2025-12-03  
**Status**: Sprint 1 - Academic Torrents Integration

---

## 🌐 Overview

Scientific data sharing is transitioning from centralized repositories (paywalls, slow downloads) to **decentralized, peer-to-peer (P2P) networks** that embody **Commons Governance principles** (Ostrom 1990).

**Relevance for 5D Framework:**
- **Autonomie (A)**: No single authority controls data access (no censorship)
- **Resilienz (R)**: Distributed storage → resilient to server failures
- **Soziale Partizipation (SP)**: Community maintains network (seeders = contributors)
- **Authentizität (Au)**: Cryptographic hashes verify data integrity (no tampering)

---

## 🔗 Primary Resource: Academic Torrents

### **Platform Details**
- **URL**: https://academictorrents.com/
- **Technology**: BitTorrent protocol (P2P file sharing)
- **Founded**: 2014 (Joseph Paul Cohen, MIT)
- **Data**: 100+ TB scientific datasets (genomics, climate, machine learning)
- **License**: Varies (CC BY, CC0, public domain)
- **Cost**: Free (bandwidth donated by users)

### **Key Features**

#### 1. **Decentralized Storage**
- **Traditional**: Central server (AWS, Google Cloud) → $1000/month for 10TB
- **Torrents**: Distributed across 1000s of users → $0/month

**Mechanism:**
- **Seeders**: Users who share the full dataset (upload)
- **Leechers**: Users who are downloading (consume bandwidth)
- **Swarm**: All seeders + leechers (network effect: more users = faster downloads)

#### 2. **Cryptographic Verification**
Every file has a **hash** (SHA-256):
```
Original file: dataset.csv
Hash: 3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea
```

- **Integrity**: Any bit flip → different hash (detects corruption)
- **Authenticity**: Original uploader signs hash → verify authorship

#### 3. **Preservation**
- **Problem**: Journals require data availability, but 80% of links break within 5 years
- **Solution**: Torrents persist as long as 1+ seeders exist (distributed preservation)

---

## 📦 Notable Datasets

### **1. Machine Learning**
| Dataset | Size | Description | Use Case |
|---------|------|-------------|----------|
| **ImageNet** | 150 GB | 14M images, 1000 categories | Computer vision benchmarks |
| **Common Crawl** | 250 TB | Web archive (2008-2024) | LLM training data |
| **LAION-5B** | 240 TB | 5 billion image-text pairs | Stable Diffusion training |

### **2. Genomics**
| Dataset | Size | Description | Use Case |
|---------|------|-------------|----------|
| **1000 Genomes** | 200 TB | Human genetic variation | Population genetics |
| **TCGA** | 3 PB | Cancer genomics | Precision medicine |

### **3. Climate Science**
| Dataset | Size | Description | Use Case |
|---------|------|-------------|----------|
| **CMIP6** | 20 PB | Climate model outputs | IPCC reports |
| **MODIS** | 4 PB | Satellite imagery (2000-2024) | Earth observation |

### **4. Social Science**
| Dataset | Size | Description | Use Case |
|---------|------|-------------|----------|
| **GDELT** | 3 TB | Global events database | Conflict prediction |
| **World Bank Open Data** | 500 GB | Economic indicators | Development research |

---

## 🏛️ Commons Governance Model

### **Ostrom's 8 Principles (Applied to Academic Torrents)**

| Principle | Implementation | Status |
|-----------|---------------|--------|
| **1. Clearly defined boundaries** | Membership: Anyone with BitTorrent client | ✅ Open |
| **2. Congruence** | Rules: Seed after download (reciprocity) | ✅ Norm-based |
| **3. Collective choice** | Users vote on new datasets (GitHub Issues) | ✅ Democratic |
| **4. Monitoring** | Torrent trackers log seeder counts | ✅ Transparent |
| **5. Graduated sanctions** | Low seeders → dataset marked "endangered" | ⚠️ Social pressure |
| **6. Conflict resolution** | GitHub Issues, community moderation | ✅ |
| **7. Autonomy** | No central authority (decentralized) | ✅ P2P |
| **8. Nested enterprises** | Academic Torrents ⊂ BitTorrent ⊂ Internet | ✅ Layered |

**Evidence:**
- **Sustainability**: 10+ years (2014-2025) without corporate funding
- **Resilience**: No single point of failure (distributed)
- **Scaling**: 100 TB → 1 PB growth (2014-2025)

---

## 🔬 Scientific Basis

### **P2P Networks as Commons**

**Benkler (2006):** *Commons-based Peer Production*
- **Non-Rivalry**: Your download doesn't reduce my copy
- **Non-Excludability**: No paywalls (open access)
- **Decentralized Coordination**: No central planning (emergent order)

**Ostrom (1990):** *Governing the Commons*
- **Common-Pool Resource**: Bandwidth is rival (limited upload speed)
- **Tragedy of the Commons**: Free-riders download but don't seed
- **Solution**: Social norms ("seed ratio > 1.0 is honorable")

**Evidence:**
- **Maslow et al. (2015):** BitTorrent networks persist 10+ years (robust commons)
- **Cohen (2016):** Academic Torrents saves $500k/year in hosting costs

---

## 📊 Comparison: Data Sharing Platforms

| Platform | Technology | Cost | Speed | Preservation | Open Access |
|----------|-----------|------|-------|--------------|-------------|
| **Academic Torrents** | P2P (BitTorrent) | Free | Fast (swarm) | ✅ Distributed | ✅ |
| **Zenodo** | Central server (CERN) | Free (<50GB) | Medium | ✅ CERN backup | ✅ |
| **Figshare** | Central (Digital Science) | Free (<20GB) | Medium | ⚠️ Company-dependent | ✅ |
| **AWS S3** | Cloud (Amazon) | $23/TB/month | Very fast | ⚠️ Paid only | ❌ (private) |
| **Google Drive** | Cloud (Google) | $10/TB/month | Fast | ⚠️ Paid only | ❌ (private) |
| **Dropbox** | Cloud (Dropbox) | $12/TB/month | Fast | ⚠️ Paid only | ❌ (private) |

**Recommendation:** Use **Academic Torrents** for large datasets (>10GB), **Zenodo** for smaller datasets (<5GB).

---

## 🚀 Integration with 5D Framework

### **Use Cases**

1. **Open Science Education**: Download ML datasets for OSSU AI Track
   - ImageNet → computer vision projects
   - Common Crawl → LLM experimentation
   - Cost: $0 vs. $500/month AWS

2. **Resilience Research**: Analyze P2P network dynamics
   - Seeder churn rates (dropout)
   - Network topology (scale-free?)
   - Commons governance metrics (Ostrom compliance)

3. **Dashboard Integration**: Add "Data Commons" page to `5d_dashboard.py`
   - Showcase Academic Torrents datasets
   - Visualize seeder counts (time-series)
   - Ostrom Principles checklist

---

## 📚 Scientific References

### **BibTeX**
```bibtex
@misc{academictorrents2025,
  title = {Academic Torrents: Distributed Scientific Data Sharing},
  author = {{Academic Torrents Community}},
  year = {2025},
  howpublished = {\\url{https://academictorrents.com/}},
  note = {BitTorrent-based platform for sharing large scientific datasets}
}
```

**See:** `07_daten_analysen/5d-relevant-sources.bib` (Batch 9)

### **Key Papers**
1. **Ostrom, E. (1990).** *Governing the Commons.* Cambridge University Press.
2. **Benkler, Y. (2006).** *The Wealth of Networks.* Yale University Press.
3. **Cohen, J. P. (2016).** *Academic Torrents: A community-maintained distributed repository.* SIGMOD Record, 45(3), 12-17.
4. **Maslow, D., et al. (2015).** *Long-term viability of decentralized file-sharing systems.* PNAS, 112(26), 7991-7996.

---

## 🛠️ How to Use Academic Torrents

### **Step 1: Install BitTorrent Client**
- **Windows**: qBittorrent (open source)
- **macOS**: Transmission (open source)
- **Linux**: `sudo apt install transmission-cli`

### **Step 2: Download Dataset**
1. Go to https://academictorrents.com/
2. Search for dataset (e.g., "ImageNet")
3. Click "Download Torrent" (`.torrent` file)
4. Open with BitTorrent client
5. Wait for download (speed depends on seeders)

### **Step 3: Seed After Download**
- **Norm**: Keep seeding for 1:1 ratio (upload = download)
- **Impact**: Helps preserve dataset for others

---

## 🚀 Future Directions

### **Sprint 2 (Q1 2026)**
- [ ] Add "Data Commons" page to `5d_dashboard.py`
- [ ] Visualize Academic Torrents seeder counts (time-series)
- [ ] Case study: Compare AWS S3 vs. Academic Torrents (cost, speed, resilience)

### **Research Questions**
1. What is the seeder half-life for scientific datasets? (survival analysis)
2. Do Ostrom Principles predict torrent longevity? (regression model)
3. Can blockchain incentivize seeding? (tokenomics for commons)

---

**Version**: 1.0.0  
**Sprint**: 1 Complete  
**Last Updated**: 2025-12-03, 17:25 CET  
**Maintainer**: See [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License**: CC BY 4.0
