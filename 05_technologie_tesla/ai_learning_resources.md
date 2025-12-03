# AI Learning Resources & Online Courses

**Dimension**: 05_technologie_tesla  
**Cross-Reference**: 01_bildung_education (OSSU), 07_daten_analysen (AI Research)  
**Date**: 2025-12-03  
**Status**: Sprint 1 - Microsoft AI Course Integration

---

## 🎓 Overview

AI/ML education has become democratized with free, high-quality online courses from universities and tech companies. This document curates the best resources for self-directed learners.

**Relevance for 5D Framework:**
- **Autonomie (A)**: Self-paced learning, no enrollment deadlines
- **Intrinsische Motivation (IM)**: Project-based learning (build real apps)
- **Authentizität (Au)**: Industry-relevant skills (not just theory)
- **Soziale Partizipation (SP)**: Community forums (GitHub Discussions, Discord)

---

## 🚀 Primary Resource: Microsoft Generative AI Course

### **Platform Details**
- **URL**: https://microsoft.github.io/generative-ai-for-beginners/
- **GitHub**: https://github.com/microsoft/generative-ai-for-beginners (80k+ stars)
- **Institution**: Microsoft Cloud Advocates
- **Duration**: 18 lessons (~20-30 hours total)
- **Languages**: Python + TypeScript
- **Prerequisites**: Basic programming knowledge

### **Course Structure**

#### **Module 1: Introduction (Lessons 1-3)**
1. **Introduction to Generative AI and LLMs**
   - What is Generative AI? (vs. Discriminative AI)
   - Large Language Models (GPTs, Claude, Llama)
   - Transformers Architecture (Attention mechanism)

2. **Exploring and Comparing Different LLMs**
   - OpenAI (GPT-4), Anthropic (Claude), Meta (Llama 4), Google (Gemini)
   - Benchmarks: MMLU, HumanEval, TruthfulQA
   - Choosing the right model (cost, latency, quality)

3. **Using Generative AI Responsibly**
   - Bias in training data
   - Hallucinations (fake citations, math errors)
   - Privacy concerns (data leakage)
   - Microsoft Responsible AI principles

#### **Module 2: Prompting (Lessons 4-6)**
4. **Understanding Prompt Engineering Fundamentals**
   - Zero-shot vs. Few-shot prompting
   - Chain-of-Thought (CoT) prompting
   - Temperature, Top-P, Max Tokens

5. **Creating Advanced Prompts**
   - System prompts (persona, tone, constraints)
   - Retrieval-Augmented Generation (RAG)
   - Agentic workflows (AutoGPT, BabyAGI)

6. **Building Text Generation Applications**
   - Hands-on: ChatBot with OpenAI API
   - Streaming responses (Server-Sent Events)
   - Error handling, rate limits

#### **Module 3: Building Apps (Lessons 7-12)**
7. **Building Chat Applications**
   - TypeScript/React frontend
   - Python/FastAPI backend
   - Conversation memory (session state)

8. **Building Search Applications with Vector Databases**
   - Embeddings (OpenAI `text-embedding-ada-002`)
   - Vector search (Pinecone, Weaviate, Chroma)
   - Semantic search vs. keyword search

9. **Building Image Generation Applications**
   - DALL-E 3, Stable Diffusion, Midjourney APIs
   - Prompt engineering for images
   - Ethical considerations (deepfakes)

10. **Building Low Code AI Applications**
    - Microsoft Power Platform
    - Azure AI Studio
    - No-code chatbots (Copilot Studio)

11. **Integrating External Applications with Function Calling**
    - GPT-4 Function Calling
    - Tool use (calculator, web search, database queries)
    - Multi-step agentic reasoning

12. **Designing UX for AI Applications**
    - Transparency (show AI uncertainty)
    - Feedback loops (thumbs up/down)
    - Guardrails (content filters, input validation)

#### **Module 4: Advanced Topics (Lessons 13-18)**
13. **Securing Your Generative AI Applications**
    - Prompt injection attacks
    - Data exfiltration
    - Azure AI Content Safety

14. **The Generative AI Application Lifecycle**
    - LLMOps (versioning, monitoring, A/B testing)
    - Evaluation metrics (BLEU, ROUGE, Human Eval)
    - Continuous improvement

15. **Retrieval Augmented Generation (RAG) and Vector Databases**
    - Advanced: Hybrid search (keyword + semantic)
    - Reranking (Cohere Rerank)
    - Citation generation

16. **Open Source Models and Hugging Face**
    - Llama 4, Mistral, Falcon
    - Fine-tuning (LoRA, QLoRA)
    - Model quantization (int8, int4)

17. **AI Agents**
    - AutoGPT, LangChain Agents
    - Tool selection, planning, execution
    - Multi-agent collaboration

18. **Fine-tuning LLMs**
    - Full fine-tuning vs. PEFT (Parameter-Efficient Fine-Tuning)
    - Dataset preparation (instruction-tuning)
    - Evaluation (perplexity, task-specific metrics)

---

## 🛠️ Hands-On Projects

Each lesson includes a project:
- **Lesson 6**: Build a recipe generator chatbot
- **Lesson 8**: Semantic search for company documents
- **Lesson 9**: Image generation app with prompt templates
- **Lesson 11**: Math problem solver with function calling
- **Lesson 15**: RAG app with citation links

**GitHub Codespaces**: All projects run in browser (no local setup)

---

## 📊 Comparison: AI/ML Courses

| Course | Institution | Duration | Difficulty | Cost | Cert | Hands-On |
|--------|-------------|----------|------------|------|------|----------|
| **Microsoft Gen AI** | Microsoft | 20h | Beginner | Free | ❌ | ✅ (18 projects) |
| **Fast.ai** | fast.ai | 40h | Intermediate | Free | ❌ | ✅ (7 projects) |
| **Andrew Ng ML** | Stanford/Coursera | 60h | Beginner | Free (audit) | $49 | ⚠️ (theory-heavy) |
| **DeepLearning.AI** | Andrew Ng | 30h | Intermediate | Free (audit) | $49 | ✅ (notebooks) |
| **Hugging Face NLP** | Hugging Face | 20h | Intermediate | Free | ❌ | ✅ (Transformers) |
| **OSSU AI Track** | OSSU | 600h | Advanced | Free | ❌ | ✅ (full CS degree) |

**Recommendation:** Start with **Microsoft Gen AI** (beginner-friendly), then **Fast.ai** (practical), then **OSSU** (theory).

---

## 🎓 Integration with 5D Framework

### **OSSU-Bridge: AI/ML Track**
Add Microsoft course as **supplementary** to OSSU Computer Science:

| OSSU Core Course | Microsoft Supplement |
|------------------|---------------------|
| **Intro to CS (Python)** | Lesson 1-3 (Basics) |
| **Algorithms** | Lesson 16 (Transformers Architecture) |
| **Databases** | Lesson 8 (Vector DBs) |
| **Software Engineering** | Lesson 12 (UX Design) |
| **Capstone Project** | Lesson 17-18 (AI Agents + Fine-Tuning) |

**See:** `06_synthesen_kompilationen/ossu_ib_bridge.md`

### **IB Computer Science HL**
- **Topic 7.1 (Abstraction)**: GPT architecture (black box → emergent behavior)
- **Topic 7.3 (Networking)**: API calls, rate limits, streaming
- **Internal Assessment**: Build chatbot with RAG (score: 20/20)

---

## 🚀 Future Directions

### **Sprint 2 (Q1 2026)**
- [ ] Add to `01_bildung_education/ossu_ib_bridge.md` (AI Track)
- [ ] Create Streamlit tutorial based on Lesson 7 (ChatBot)
- [ ] Test Microsoft course with 10 students (feedback survey)

### **Research Questions**
1. Does project-based learning (Microsoft course) improve retention vs. lecture-based (Coursera)?
2. What is the completion rate? (Typical MOOCs: 5-10%)
3. Can GitHub Codespaces reduce setup friction? (compare to local Python install)

---

## 📚 Scientific References

### **BibTeX**
```bibtex
@misc{microsoftai2024,
  author = {{Microsoft Cloud Advocates}},
  title = {Generative AI for Beginners},
  year = {2024},
  howpublished = {\\url{https://microsoft.github.io/generative-ai-for-beginners/}},
  note = {18-lesson course on generative AI with Python and TypeScript}
}
```

**See:** `07_daten_analysen/5d-relevant-sources.bib` (Batch 9)

### **Related Resources**
- **Fast.ai**: https://course.fast.ai/
- **DeepLearning.AI**: https://www.deeplearning.ai/courses/
- **Hugging Face NLP**: https://huggingface.co/learn/nlp-course/

---

**Version**: 1.0.0  
**Sprint**: 1 Complete  
**Last Updated**: 2025-12-03, 17:20 CET  
**Maintainer**: See [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License**: CC BY 4.0
