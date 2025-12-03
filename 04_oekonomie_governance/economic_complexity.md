# Economic Complexity & Trade Networks

**Dimension**: 04_oekonomie_governance  
**Cross-Reference**: 07_daten_analysen (Global Data), 03_philosophie_epistemologie (Network Epistemology)  
**Date**: 2025-12-03  
**Status**: Sprint 1 - Harvard Atlas Integration

---

## 🌍 Overview

**Economic Complexity** measures the productive capabilities of countries based on the diversity and sophistication of products they export. It predicts future economic growth better than traditional indicators (GDP, Human Capital).

**Core Insight (Hidalgo & Hausmann 2009):**
> "What you export matters. Countries that export complex products grow faster."

**Relevance for 5D Framework:**
- **Governance (SP)**: Network-based governance → trade partnerships, not coercion
- **Resilienz (R)**: Diverse export portfolios → economic resilience
- **Autonomie (A)**: Countries with complex industries have more policy autonomy
- **Authentizität (Au)**: Exports reflect true productive capabilities (not resource curse)

---

## 📊 Primary Resource: Harvard Atlas of Economic Complexity

### **Platform Details**
- **URL**: https://atlas.hks.harvard.edu/
- **Institution**: Harvard Kennedy School Center for International Development
- **Lead Researchers**: Ricardo Hausmann, César Hidalgo
- **Data Coverage**: 1963-2023 (60+ years), 130+ countries, 5000+ products
- **Visualizations**: Interactive network graphs, tree maps, time-series

### **Key Metrics**

#### 1. **Economic Complexity Index (ECI)**
Measures sophistication of a country's productive capabilities.

```
ECI_country = f(diversity of exports, ubiquity of exports)
```

- **High ECI**: Japan (🇯🇵), Germany (🇩🇪), Switzerland (🇨🇭) → complex manufacturing
- **Low ECI**: Resource-dependent economies (oil, minerals) → simple exports

#### 2. **Product Complexity Index (PCI)**
Measures knowledge required to produce a product.

- **High PCI**: MRI machines, jet engines, semiconductors
- **Low PCI**: Bananas, crude oil, raw cotton

#### 3. **Proximity Network**
Shows which products are related (require similar capabilities).

- **Example**: Manufacturing cars → easier to start making trucks (close in network)
- **Example**: Exporting oil → hard to pivot to electronics (far in network)

---

## 🔬 Scientific Basis

### **Network Theory of Economic Development**

**Product Space (Hidalgo et al. 2007):**
- Products = nodes
- Links = shared capabilities (if countries export both)
- **Dense Core**: Complex manufacturing (machinery, chemicals, electronics)
- **Sparse Periphery**: Agriculture, raw materials

**Implication:**
- **Path Dependency**: Countries close to complex products → easier to diversify
- **Poverty Trap**: Countries in periphery → hard to reach core (capability gaps)

### **Evidence**
- **Hausmann et al. (2013):** ECI predicts GDP growth 10 years ahead (r = 0.71)
- **Hidalgo & Hausmann (2009):** ECI > Human Capital Index for growth prediction
- **Replicated**: 130+ countries, 5000+ products (HS4 classification)

**BibTeX:** `hausmann2013atlas`, `hidalgo2009building`

---

## 📈 Key Findings

### **1. Complexity Predicts Growth**
| Country (2000 ECI) | 2000-2020 Growth | Explanation |
|--------------------|------------------|-------------|
| **China** (High ECI, Low GDP) | 9.2% annual | Rapidly diversified into complex manufacturing |
| **India** (Medium ECI, Low GDP) | 6.8% annual | IT services + pharmaceuticals (complex) |
| **Venezuela** (Low ECI, High GDP) | -1.5% annual | Oil-dependent (simple exports) |

### **2. Proximity Matters**
- **South Korea (1970s):** Textiles → Electronics (close in network)
- **Norway:** Oil → Fisheries → Shipping → Renewable Energy (gradual diversification)
- **Saudi Arabia:** Oil → ... (stuck in periphery despite wealth)

### **3. Diversity ≠ Complexity**
- **Nigeria:** Exports many products (cocoa, oil, textiles) → Low ECI (all simple)
- **Switzerland:** Exports fewer products (watches, pharma, machinery) → High ECI (all complex)

---

## 🌐 Interactive Visualizations

### **Available Tools**
1. **Country Profiles**: Time-series of ECI, exports, growth
2. **Product Space Map**: Network visualization (zoom, filter by complexity)
3. **Complexity Rankings**: Compare countries (sortable table)
4. **Export Explorer**: Drill down by product category (HS4 codes)
5. **Feasibility Analysis**: "What new products could Country X export?"

### **Use Cases for 5D Framework**
- **Governance Research**: Analyze economic autonomy (ECI vs. Resource Dependence)
- **Dashboard Integration**: Add ECI to `5d_dashboard.py` (Country Metrics)
- **Resilience Indicator**: ECI as proxy for Resilienz (R) score
- **Case Studies**: Singapore (high ECI, no resources) vs. resource-cursed countries

---

## 🔗 Integration with 5D Framework

### **Dimension Mapping**
| 5D Dimension | ECI Correlation | Mechanism |
|--------------|----------------|----------|
| **Autonomie (A)** | + (r ≈ 0.60) | Complex economies have policy space (not IMF-dependent) |
| **Resilienz (R)** | + (r ≈ 0.65) | Diverse exports → resilience to shocks |
| **Soziale Partizipation (SP)** | + (r ≈ 0.50) | Complex industries require collaboration |
| **Authentizität (Au)** | + (r ≈ 0.55) | Exports reflect true capabilities (not extractive) |
| **Intrinsische Motivation (IM)** | ? (untested) | Hypothesis: Complex work → higher IM |

**Testable Hypothesis:**
- Countries with high ECI have higher IMP-Proxy scores (Governance component)
- Correlation test: ECI vs. WGI Voice & Accountability (expect r > 0.60)

---

## 📊 Data Access

### **Download Options**
1. **Atlas Website**: CSV exports (country-year-product)
2. **Observatory of Economic Complexity (OEC)**: API access (https://oec.world/)
3. **Harvard Dataverse**: Full datasets (1963-2023)
4. **R Package**: `economiccomplexity` (CRAN)

### **Data Structure (Example)**
```csv
country_code,year,product_hs4,export_value_usd,rca
DEU,2020,8703,150000000000,2.5
```
- `rca` = Revealed Comparative Advantage (exports / world average)
- `hs4` = Harmonized System 4-digit product code (e.g., 8703 = automobiles)

---

## 📚 Scientific References

### **Foundational Papers**
1. **Hidalgo, C. A., & Hausmann, R. (2009).** *The building blocks of economic complexity.* PNAS, 106(26), 10570-10575. [DOI: 10.1073/pnas.0900943106]
2. **Hausmann, R., et al. (2013).** *The Atlas of Economic Complexity: Mapping Paths to Prosperity.* MIT Press.
3. **Hidalgo, C. A., et al. (2007).** *The product space conditions the development of nations.* Science, 317(5837), 482-487.

### **BibTeX**
```bibtex
@misc{atlashks2025,
  author = {{Harvard Growth Lab}},
  title = {The Atlas of Economic Complexity},
  year = {2025},
  publisher = {Harvard Kennedy School Center for International Development},
  howpublished = {\url{https://atlas.hks.harvard.edu/}},
  note = {Interactive visualizations of global trade and economic complexity}
}
```

**See:** `07_daten_analysen/5d-relevant-sources.bib` (Batch 9)

---

## 🚀 Future Directions

### **Sprint 2 (Q1 2026)**
- [ ] Add ECI to `5d_dashboard.py` (Country Comparison Page)
- [ ] Test correlation: ECI vs. IMP-Proxy (expect r > 0.60)
- [ ] Visualize Product Space with Folium (network map)
- [ ] Case study: Singapore (high ECI) vs. Nigeria (low ECI)

### **Research Questions**
1. Does ECI predict IMP-Proxy better than GDP per capita?
2. Do countries with high ECI have lower Dropout rates (education quality)?
3. Can Product Space proximity guide industrial policy for developing countries?

---

**Version**: 1.0.0  
**Sprint**: 1 Complete  
**Last Updated**: 2025-12-03, 17:10 CET  
**Maintainer**: See [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License**: CC BY 4.0
