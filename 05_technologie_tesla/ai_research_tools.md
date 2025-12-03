# AI Research Tools & Automation

**Dimension**: 05_technologie_tesla  
**Cross-Reference**: 07_daten_analysen (Research Methods), 01_bildung_education (OSSU AI Track)  
**Date**: 2025-12-03  
**Status**: Sprint 1 - Elicit Integration

---

## 🤖 Overview

AI-powered research tools automate literature review, paper summarization, and hypothesis generation. They reduce time-to-insight from hours to minutes.

**Relevance for 5D Framework:**
- **Autonomie (A)**: Researchers control search queries, no algorithmic censorship
- **Intrinsische Motivation (IM)**: Focus on ideas, not tedious tasks (reading 100+ abstracts)
- **Resilienz (R)**: Faster iteration → more experiments → robust findings
- **Authentizität (Au)**: AI as assistant, not replacement (human still validates)

---

## 🎯 Primary Resource: Elicit

### **Platform Details**
- **URL**: https://elicit.com/
- **Developer**: Elicit, Inc. (AI Safety startup)
- **Technology**: GPT-4 + custom fine-tuning on academic papers
- **Pricing**: Free (5 credits/day), Pro ($10/month, unlimited)
- **Data**: 200M+ papers (Semantic Scholar, PubMed, arXiv)

### **Key Features**

#### 1. **Literature Review Automation**
- **Input**: Natural language question (e.g., "Does meditation reduce anxiety?")
- **Output**: Table with papers, key findings, sample sizes, effect sizes
- **Speed**: 30 seconds vs. 2 hours manual search

**Example Query:**
```
"What is the relationship between autonomy and intrinsic motivation in educational settings?"
```

**Output Table:**
| Paper | Finding | Sample | Effect Size |
|-------|---------|--------|-------------|
| Deci & Ryan (1985) | Autonomy → IM | Meta-analysis (128 studies) | r = 0.65 |
| Reeve et al. (2004) | Autonomy-supportive teaching → IM | 200 students | d = 0.82 |

#### 2. **Paper Summarization**
- **Input**: PDF upload or DOI
- **Output**: 1-paragraph summary + key takeaways
- **Multilingual**: Summarize German paper → English output

#### 3. **Hypothesis Generation**
- **Input**: Research question + existing papers
- **Output**: Novel hypotheses based on gaps in literature
- **Use Case**: Identify untested combinations (e.g., "Does IMP-Score predict burnout risk?")

#### 4. **Citation Graph Exploration**
- **Input**: Seed paper
- **Output**: Papers that cite it, papers it cites
- **Visualization**: Network graph (similar to Connected Papers)

---

## 🔬 Scientific Validation

### **Accuracy Tests (Elicit Team 2024)**
- **Precision**: 92% (correct answers / all answers)
- **Recall**: 78% (found papers / all relevant papers)
- **Hallucination Rate**: 3% (fake citations)
- **Human Benchmark**: PhD students achieve 85% precision, 65% recall

**Caveats:**
- Not peer-reviewed tool (startup, not academic lab)
- Bias toward English-language papers (95% of corpus)
- Recent papers underrepresented (indexing lag: 3-6 months)

---

## 🎓 Use Cases for 5D Framework

### **1. Literature Review for IMP-Score Validation**
**Query:**
```
"Correlation between autonomy, intrinsic motivation, and life satisfaction in longitudinal studies"
```

**Expected Output:**
- Deci & Ryan (2000): SDT meta-analysis
- Sheldon & Elliot (1999): Self-Concordance Model
- Knee et al. (2002): Autonomy vs. Contingent Self-Esteem

**Action:** Add findings to `docs/CLAIMS_EVIDENCE_MATRIX.md`

### **2. Hypothesis Generation**
**Input:**
- IMP-Score components (A, IM, R, SP, Au)
- Outcome: Life Satisfaction (OECD Better Life Index)
- Gap: No study tests all 5 dimensions simultaneously

**Elicit Output:**
- "Hypothesis: IMP-Score (multiplicative) predicts Life Satisfaction better than additive model"
- "Rationale: Weak-link logic (one dimension = 0 → total collapse)"
- "Methodology: Survey (n > 100), regression analysis"

### **3. Competitive Analysis (Learn Anything)**
**Query:**
```
"Knowledge graph platforms for self-directed learning with prerequisite mapping"
```

**Output:**
- Papers on adaptive learning systems
- Comparison: Learn Anything vs. Coursera vs. Khan Academy
- Integration opportunities: API access, data formats

---

## 📊 Comparison: AI Research Tools

| Tool | Technology | Data Source | Key Feature | Pricing |
|------|-----------|-------------|-------------|--------|
| **Elicit** | GPT-4 | 200M papers | Literature review automation | Free (5/day), Pro ($10/mo) |
| **Consensus** | GPT-3.5 | 100M papers | Yes/no questions (e.g., "Does X cause Y?") | Free (20/mo), Pro ($10/mo) |
| **Semantic Scholar** | AllenAI | 200M papers | Citation graph, author profiles | Free |
| **Connected Papers** | Graph DB | Semantic Scholar | Visual citation network | Free (limited), Pro ($6/mo) |
| **Research Rabbit** | Graph DB | 100M papers | Discovery by seed paper | Free |
| **ChatGPT (GPT-4)** | OpenAI | Web search | General Q&A (not academic-specific) | Free (GPT-3.5), Plus ($20/mo) |

**Recommendation:** Use **Elicit** for literature review, **Connected Papers** for citation exploration.

---

## 🚀 Integration Workflow

### **Step 1: Research Question**
Define clear, testable question:
- "Does IMP-Score correlate with Life Satisfaction (r > 0.60)?"

### **Step 2: Elicit Search**
```
"Autonomy, intrinsic motivation, resilience, social participation, authenticity → life satisfaction"
```

### **Step 3: Export Results**
- Download CSV (papers, findings, sample sizes)
- Add to `07_daten_analysen/literature_review_imp.csv`

### **Step 4: Update Evidence Matrix**
- Add findings to `docs/CLAIMS_EVIDENCE_MATRIX.md`
- Label: ✅ Fakt (if replicated), ⚠️ Hypothese (if single study), 🔮 Spekulation (if no data)

### **Step 5: Pre-Registration**
- Use Elicit hypotheses for OSF pre-registration (Q2 2026)

---

## 📚 Scientific References

### **BibTeX**
```bibtex
@misc{elicit2025,
  title = {Elicit: AI Research Assistant},
  author = {{Elicit, Inc.}},
  year = {2025},
  howpublished = {\url{https://elicit.com/}},
  note = {GPT-powered literature review and paper summarization tool}
}
```

**See:** `07_daten_analysen/5d-relevant-sources.bib` (Batch 9)

### **Related Tools**
- **AllenAI Semantic Scholar**: https://www.semanticscholar.org/
- **Connected Papers**: https://www.connectedpapers.com/
- **Consensus**: https://consensus.app/

---

## 🚀 Future Directions

### **Sprint 2 (Q1 2026)**
- [ ] Run Elicit search for IMP-Score validation (export CSV)
- [ ] Compare Elicit vs. manual PubMed search (precision/recall)
- [ ] Integrate Elicit API into `5d_research_scraper.py` (if available)

### **Research Questions**
1. Can Elicit identify gaps in 5D-Framework literature?
2. What is the overlap between Elicit results and manual review?
3. Does AI-assisted research increase publication speed?

---

**Version**: 1.0.0  
**Sprint**: 1 Complete  
**Last Updated**: 2025-12-03, 17:15 CET  
**Maintainer**: See [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License**: CC BY 4.0
