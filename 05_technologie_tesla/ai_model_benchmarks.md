# 🤖 AI Model Benchmarks: Live Performance Tracking

**Dimension**: 05_technologie_tesla  
**Cross-Reference**: 07_daten_analysen (Data Visualization)  
**Datum**: 2025-12-02  
**Status**: Sprint 1 - Dashboard-Integration geplant

---

## 📊 Übersicht

Diese Seite aggregiert Live-Benchmarks für 100+ AI-Modelle von führenden Anbietern:
- **Artificial Analysis**: Real-time Intelligence, Performance, Price, Latency
- **Life Architect**: Parameter Count, Context Window, Training Details

**Zweck**: Objektive Technologie-Bewertung für 5D-Framework AI-Tool-Selection

---

## 🔴 KRITISCH: Artificial Analysis

### **Hauptressource**
- **URL**: https://artificialanalysis.ai/
- **Typ**: AI Model Comparison Platform
- **Update-Frequenz**: Real-time (Live Benchmarks)
- **Umfang**: 100+ Modelle

### **Benchmarked Models** (Stand Dezember 2025)

#### **OpenAI**
- GPT-5 (o3, o3-mini)
- GPT-4.5 Turbo
- GPT-4.0
- o1 (Reasoning Model)

#### **Anthropic**
- Claude 4 Opus
- Claude 4 Sonnet
- Claude 3.5 Sonnet

#### **Google**
- Gemini 2.5 Pro
- Gemini 2.0 Flash
- Gemini 1.5 Pro

#### **Meta**
- Llama 4 (405B, 70B)
- Llama 3.3 (70B)

#### **xAI**
- Grok 3
- Grok 2

#### **DeepSeek**
- DeepSeek V3
- DeepSeek-R1

#### **Andere**
- Mistral Large 2
- Qwen 2.5 (72B)
- Command R+ (Cohere)

---

## 📈 Benchmark-Kategorien

### **1. Intelligence Benchmarks**

#### **SWE-bench Verified** (Software Engineering)
- **Was**: Real-world GitHub Issues lösen
- **Best Performer** (Dezember 2025): GPT-5 o3 (71.7%)
- **Kontext**: Misst Code-Verständnis + Debugging-Fähigkeit

#### **AIME 2025** (Advanced Math)
- **Was**: American Invitational Mathematics Examination
- **Best Performer**: GPT-5 o3 (96.7%)
- **Kontext**: College-Level Math Problems

#### **GPQA (Diamond)** (Graduate-Level Science)
- **Was**: Physics, Chemistry, Biology Questions (PhD-Level)
- **Best Performer**: Claude 4 Opus (65.3%)
- **Kontext**: Wissenschaftliches Reasoning

#### **MMLU-Pro** (Multitask Language Understanding)
- **Was**: 57 Domains (Law, Medicine, History, etc.)
- **Best Performer**: Gemini 2.5 Pro (92.1%)

#### **VideoMME** (Video Understanding)
- **Was**: Multi-Frame Video Q&A
- **Best Performer**: Gemini 2.0 Flash (78.4%)

---

### **2. Performance Metrics**

#### **Latency** (Sekunden bis First Token)
- **Fastest**: Gemini 2.0 Flash (0.21s)
- **Slowest**: GPT-5 o3 (18.3s - wegen Reasoning)
- **Median**: Claude 4 Sonnet (1.2s)

#### **Throughput** (Tokens per Second)
- **Highest**: Llama 4 70B (152 tok/s)
- **Lowest**: GPT-5 o3 (12 tok/s)

#### **Context Window**
- **Largest**: Gemini 2.5 Pro (2M tokens)
- **Typical**: 128K-200K tokens (GPT-4.5, Claude 4)

---

### **3. Price Comparison** ($ per Million Tokens)

#### **Input Cost**
| Model | Price (Input) | Price (Output) |
|-------|---------------|----------------|
| GPT-5 o3 | $15.00 | $60.00 |
| Claude 4 Opus | $15.00 | $75.00 |
| Gemini 2.5 Pro | $1.25 | $5.00 |
| Llama 4 405B | $0.00 | $0.00 (Open Source) |
| Qwen 2.5 72B | $0.00 | $0.00 (Open Source) |

**Insight**: Open-Source-Modelle (Llama, Qwen) = kostenlos, aber self-hosting erforderlich.

---

### **4. Quality-Speed-Price Trade-offs**

**Artificial Analysis Interactive Charts**:
- **Quality vs. Speed**: Claude 4 Opus = High Quality, Medium Speed
- **Quality vs. Price**: Gemini 2.5 Pro = Best Value (High Quality, Low Price)
- **Speed vs. Price**: Gemini 2.0 Flash = Ultra-Fast, Ultra-Cheap

**Empfehlungen**:
- **Research/Academia**: Claude 4 Opus (GPQA-Leader)
- **Software Engineering**: GPT-5 o3 (SWE-bench-Leader)
- **High-Volume Apps**: Gemini 2.5 Pro (Best Price-Performance)
- **Real-time Apps**: Gemini 2.0 Flash (Lowest Latency)
- **Self-Hosting**: Llama 4 70B oder Qwen 2.5 72B

---

## 📊 Life Architect: AI Models Comparison Table

### **Ergänzende Ressource**
- **URL**: https://lifearchitect.ai/models-table/
- **Typ**: Umfassende Tabelle (Parameter, Training, Context)
- **Update**: Regelmäßig (manuell kuratiert)

### **Zusätzliche Metriken**

#### **Parameter Counts**
- **GPT-5 o3**: ~1.8 Trillion (estimated)
- **Claude 4 Opus**: ~500 Billion (estimated)
- **Llama 4 405B**: 405 Billion (confirmed)
- **Gemini 2.5 Pro**: ~1.5 Trillion (estimated)

#### **Training Data Cutoff**
- **GPT-5 o3**: Oktober 2024
- **Claude 4**: Dezember 2024
- **Gemini 2.5 Pro**: November 2024

#### **Context Window Comparison**
- **Longest**: Gemini 2.5 Pro (2M tokens)
- **Standard**: 128K-200K (GPT-4.5, Claude 4, Llama 4)
- **Shortest**: 32K (older models)

**Verwendung**: Life Architect für technische Details, Artificial Analysis für Live-Performance.

---

## 🚀 Dashboard-Integration (geplant)

### **Vision**: 5D AI Benchmark Dashboard

**Features**:
- **Live Data Scraping**: Artificial Analysis API (falls verfügbar)
- **Model Selector**: Filter by Use Case (Research, Coding, Chat, Creative)
- **Cost Calculator**: Input/Output Tokens → Estimated Cost
- **Benchmark Timeline**: Historical Performance (Track Model Improvements)

**Technologie-Stack**:
- **Frontend**: React + D3.js (Interactive Charts)
- **Backend**: Python + BeautifulSoup (Web Scraping)
- **Database**: PostgreSQL (Store Historical Benchmarks)
- **Deployment**: Vercel/Netlify (Serverless)

**Location**: `web/5d-map/ai-benchmarks/`

**BibTeX**: `artificialanalysis2025` in `07_daten_analysen/5d-relevant-sources.bib`

---

## 📊 Vergleichstabelle (Ressourcen)

| Ressource | Typ | Update-Frequenz | Umfang | Interactive Charts | API |
|-----------|-----|-----------------|--------|-------------------|-----|
| **Artificial Analysis** | Live Benchmarks | Real-time | 100+ Models | ✅ | ❌ (Web-Scraping) |
| **Life Architect** | Comparison Table | Manuell (weekly) | 50+ Models | ❌ | ❌ |
| **Hugging Face Leaderboard** | Open LLM Rankings | Daily | Open-Source Only | ✅ | ✅ |
| **LMSYS Chatbot Arena** | User Votes | Real-time | 80+ Models | ✅ | ✅ |

---

## 🧠 5D-Perspektive: AI Tool Selection

### **Dimensionen-Mapping**

#### **01_bildung_education**
- **Best Model**: Claude 4 Opus (GPQA, Academic Reasoning)
- **Use Case**: Tutoring, Erklärungen, Konzept-Visualisierung

#### **02_neurobiologie_psychologie**
- **Best Model**: GPT-5 o3 (Chain-of-Thought Reasoning)
- **Use Case**: Metakognition, Prompt Engineering Research

#### **03_philosophie_epistemologie**
- **Best Model**: Claude 4 Opus (Nuanced Reasoning)
- **Use Case**: Ethische Dilemmata, Epistemische Analysen

#### **04_oekonomie_governance**
- **Best Model**: Gemini 2.5 Pro (Multimodal, Data Analysis)
- **Use Case**: Wirtschaftsdaten-Visualisierung, Policy Analysis

#### **05_technologie_tesla**
- **Best Model**: GPT-5 o3 (SWE-bench)
- **Use Case**: Code-Generierung, Debugging, Architektur-Design

#### **07_daten_analysen**
- **Best Model**: Gemini 2.5 Pro (2M Context, Multimodal)
- **Use Case**: Large Document Analysis, Data Viz

---

## 🚀 Action Items (Sprint 1)

- [x] Artificial Analysis dokumentiert
- [x] Life Architect integriert
- [x] Benchmark-Kategorien erklärt
- [x] Dimensionen-Mapping erstellt
- [ ] **TODO Sprint 2**: Dashboard-Prototyp entwickeln
- [ ] **TODO Sprint 2**: Web-Scraping-Script für Artificial Analysis
- [ ] **TODO Sprint 3**: Hugging Face Leaderboard Integration
- [ ] **TODO Sprint 3**: LMSYS Chatbot Arena API

---

## 📚 Literatur & Referenzen

### **BibTeX-Einträge**:
- `artificialanalysis2025` (Artificial Analysis)
- `lifearchitect2025` (Life Architect AI Models Table)

### **Externe Benchmark-Quellen**:
- SWE-bench: https://www.swebench.com/
- AIME: https://artofproblemsolving.com/
- GPQA: https://arxiv.org/abs/2311.12022
- MMLU: https://arxiv.org/abs/2009.03300
- Hugging Face Leaderboard: https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard

---

**Version**: 1.0.0  
**Sprint**: 1  
**Autor**: 5D Intelligence Framework (karlitos1337)  
**Letzte Aktualisierung**: 2025-12-02  
**License**: Entspricht 5D-Repository-Lizenz
