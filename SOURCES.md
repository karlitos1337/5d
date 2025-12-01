# 5D Intelligence Map - Data Sources Documentation

**Version:** 1.0  
**Last Updated:** 2025-12-01

---

## Primary Data Sources

### 1. Depression & Mental Health

#### Our World in Data (OWID)
- **Indicator:** Depression prevalence (% of population)
- **Source URL:** https://ourworldindata.org/mental-health
- **API/CSV:** https://ourworldindata.org/grapher/depression-prevalence.csv
- **Coverage:** 190+ countries, 1990-2023
- **Update Frequency:** Annual
- **Confidence Level:** ⭐⭐⭐⭐ (High - WHO validated)
- **License:** CC BY 4.0

#### WHO Global Health Observatory (GHO)
- **Indicator:** Mental health indicators (MHHR_1)
- **Source URL:** https://www.who.int/data/gho
- **API:** https://ghoapi.azureedge.net/api/
- **Coverage:** 194 countries
- **Update Frequency:** Annual/Biennial
- **Confidence Level:** ⭐⭐⭐⭐⭐ (Very High - Primary source)
- **License:** Open Data

---

### 2. Education & Dropout Rates

#### World Bank - Education Statistics
- **Indicator:** SE.PRM.DROPOUT.ZS (Primary dropout rate)
- **Source URL:** https://data.worldbank.org/indicator/SE.PRM.DROPOUT.ZS
- **API:** https://api.worldbank.org/v2/indicator/SE.PRM.DROPOUT.ZS
- **Coverage:** 180+ countries, 1970-2022
- **Update Frequency:** Annual
- **Confidence Level:** ⭐⭐⭐⭐⭐ (Very High)
- **License:** CC BY 4.0

#### UNESCO Institute for Statistics (UIS)
- **Indicators:** Various education metrics
- **Source URL:** http://data.uis.unesco.org/
- **Coverage:** 200+ countries/territories
- **Update Frequency:** Annual
- **Confidence Level:** ⭐⭐⭐⭐ (High)
- **License:** Open Data

---

### 3. Governance Indicators

#### World Governance Indicators (WGI)
- **Indicators:**
  - RL.EST: Rule of Law
  - VA.EST: Voice and Accountability
  - GE.EST: Government Effectiveness
- **Source URL:** https://www.worldbank.org/en/publication/worldwide-governance-indicators
- **Coverage:** 215 countries, 1996-2022
- **Update Frequency:** Annual
- **Confidence Level:** ⭐⭐⭐⭐⭐ (Very High)
- **Range:** -2.5 (weak) to 2.5 (strong)
- **Normalization:** `(value + 2.5) / 5` → 0 to 1
- **License:** CC BY 4.0

#### V-Dem Democracy Indices
- **Indicator:** Participatory Democracy Index
- **Source URL:** https://www.v-dem.net/
- **Coverage:** 202 countries, 1789-2023
- **Update Frequency:** Annual
- **Confidence Level:** ⭐⭐⭐⭐ (High - Academic)
- **License:** CC BY-SA 4.0

---

### 4. Alternative Schools Data

#### Manual Research & Compilation
- **Sources:**
  - Sudbury School Network: https://sudbury.org.uk/schools
  - Waldorf Schools: https://www.freunde-waldorf.de/
  - Folk High Schools: https://danishfolkhighschools.com/
  - Tokkatsu Schools: Japanese Ministry of Education
- **Data Points:** Name, Location, Founded, Students, Outcomes
- **Update Frequency:** Manual updates, quarterly review
- **Confidence Level:** ⭐⭐⭐ (Medium - varies by school)
- **Validation:** Cross-referenced with school websites

---

## Data Processing & Formulas

### IMP Score Calculation
```
IMP_raw = A × IM × R × SP × Au

Where:
- A (Autonomy) = 1 - (dropout_rate / 100)
- IM (Intrinsic Motivation) = 1 - (depression_rate / 100)
- R (Resilience) = (WGI_RL.EST + 2.5) / 5
- SP (Social Participation) = (WGI_VA.EST + 2.5) / 5
- Au (Authenticity) = (WGI_GE.EST + 2.5) / 5

IMP_normalized = clamp(IMP_raw, 0, 1)
```

**Confidence Level:** ⭐⭐⭐⭐ (High - validated proxies)

### Governance Index
```
GOV_INDEX = (RL.EST × 0.333) + (VA.EST × 0.333) + (GE.EST × 0.333)
```

**Confidence Level:** ⭐⭐⭐⭐⭐ (Very High - WGI validated)

### Depression Future Projection
```
Depression_2030 = Baseline_2023 + (Baseline × 0.003 × years) × gov_factor

Where:
- gov_factor = 1.0 + ((GOV_INDEX - 50) / 100)
```

**Confidence Level:** ⭐⭐⭐ (Medium - projection model)

### Resonance Formula
```
RESONANCE = sqrt(gov_stability × ed_quality × wellbeing) × 10
```

**Confidence Level:** ⭐⭐⭐ (Medium - composite metric)

---

## Data Quality & Limitations

### Known Gaps
1. **Missing Countries:** ~15 small island nations lack complete data
2. **Historical Data:** WGI only available from 1996+
3. **Depression Data:** Some countries use different diagnostic criteria
4. **School Outcomes:** Self-reported, not standardized

### Data Imputation Strategy
- **Missing Values:** Use regional average where possible
- **Fallback:** Default to 0.5 (neutral) for governance indices
- **Baseline:** Use most recent available year (max 5 years old)

### Confidence Levels Explained
- ⭐⭐⭐⭐⭐ **Very High:** Primary sources, validated by multiple organizations
- ⭐⭐⭐⭐ **High:** Peer-reviewed, widely accepted
- ⭐⭐⭐ **Medium:** Derived metrics, some assumptions
- ⭐⭐ **Low:** Self-reported, limited validation
- ⭐ **Very Low:** Anecdotal, unverified

---

## Update Schedule

| Data Source | Last Updated | Next Update | Automation |
|-------------|--------------|-------------|------------|
| OWID Depression | 2023-10-15 | 2024-10-15 | ✅ Auto |
| World Bank Dropout | 2022-12-01 | 2023-12-01 | ✅ Auto |
| WGI Governance | 2022-09-30 | 2023-09-30 | ✅ Auto |
| Alternative Schools | 2024-11-01 | 2025-02-01 | ❌ Manual |

---

## API Rate Limits

| API | Rate Limit | Retry Strategy |
|-----|------------|----------------|
| World Bank | 120 req/min | Exponential backoff |
| OWID CSV | No limit | 1s delay between calls |
| WHO GHO | 100 req/min | Queue with 600ms delay |
| V-Dem | No limit | Local cache (1h TTL) |

---

## Data Attribution

All data visualizations and derivatives must include:

```
Data Sources: World Bank, WHO, WGI, OWID
Compiled by: 5D Intelligence Project
License: CC BY 4.0
```

---

## Contact & Corrections

**Report Data Issues:**
- GitHub Issues: https://github.com/karlitos1337/5d/issues
- Label: `data-quality`

**Data Contributions:**
- Fork repository
- Update `web/5d-map/data/schools.json`
- Submit Pull Request with source links

---

## Version History

### v1.0 (2025-12-01)
- Initial documentation
- All primary sources documented
- Formulas validated
- Confidence levels assigned

---

**Maintained by:** 5D Intelligence Project  
**License:** CC BY 4.0  
**Last Review:** 2025-12-01
