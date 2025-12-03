# 🤖 AI Model Tracking – Comprehensive Benchmarks

**Dimension**: 05_technologie_tesla  
**Cross-Reference**: 02_neurobiologie_psychologie (AI ↔ Neuroscience)  
**Datum**: 2025-12-03  
**Status**: Sprint 2 - Life Architect Integration

---

## 📊 Übersicht

**Problem:** AI Models entwickeln sich schnell (GPT-4 → Claude 3.5 → Gemini 2.0), Vergleiche sind schwierig  
**Lösung:** Zwei komplementäre Tracking-Systeme nutzen

---

## 🔴 Artificial Analysis (Performance)

**URL**: https://artificialanalysis.ai/  
**Fokus:** **Live Performance Benchmarks** (Latenz, Preis, Qualität)  
**Update-Frequenz:** Wöchentlich  
**Status:** ✅ Bereits integriert in `ai_model_benchmarks.md`

### Key Metrics
- **Latency:** Response Time (ms)
- **Price:** $ pro 1M tokens
- **Quality:** MMLU, HumanEval, MT-Bench Scores
- **Context Window:** Max Token Limits

---

## 🟡 Life Architect AI Models Table

**URL**: https://lifearchitect.ai/models-table/  
**Fokus:** **Technical Specifications** (Parameters, Architecture, Training)  
**Update-Frequenz:** Monatlich  
**Score**: 7/10

### Features
- **Parameter Counts:** Genaue Modellgrößen (z.B. GPT-4: 1.76T params, Claude 3.5: ~250B params)
- **Context Windows:** Max Token Limits (z.B. Claude 3.5: 200k tokens, GPT-4 Turbo: 128k tokens)
- **Training Data Cutoffs:** Wann wurde Modell trainiert? (z.B. GPT-4: Sep 2021, Claude 3.5: Apr 2024)
- **Licensing:** Open Source vs. Proprietary (z.B. Llama 3.3: Open, GPT-4: Closed)
- **Architecture Details:** Transformer variants, MoE (Mixture of Experts), etc.

---

## 🔄 Vergleich: Artificial Analysis vs. Life Architect

| Kriterium | Artificial Analysis | Life Architect |
|-----------|---------------------|----------------|
| **Fokus** | Performance Benchmarks (Latenz, Preis) | Technical Specs (Params, Context) |
| **Update-Frequenz** | Wöchentlich | Monatlich |
| **Community** | Proprietary (aber transparent) | Open Source (GitHub Issues) |
| **Use Case** | Echtzeit-Entscheidungen (API-Wahl) | Technisches Verständnis (Architektur) |
| **Example Metrics** | Latenz: 50ms, Preis: $0.25/1M tokens | Params: 175B, Context: 32k tokens |

**Integration:** Beide Quellen **komplementär** → Artificial Analysis (Performance) + Life Architect (Architecture)

---

## 🎓 Use Cases

### 1. API-Auswahl (Realtime)
**Frage:** Welche API ist am schnellsten und günstigsten?  
**Quelle:** Artificial Analysis (Live Benchmarks)  
**Beispiel:** Claude 3.5 Haiku = 50ms Latenz, $0.25/1M tokens → beste Wahl für Chatbots

### 2. Architektur-Verständnis (Research)
**Frage:** Wie groß ist GPT-4 wirklich? Welche Context Window?  
**Quelle:** Life Architect (Technical Specs)  
**Beispiel:** GPT-4 = 1.76T params, 128k context → zu groß für lokales Hosting

### 3. Historische Entwicklung (Timeline)
**Frage:** Wie hat sich AI entwickelt (2022 → 2025)?  
**Quellen:** Beide (Life Architect für Timeline, Artificial Analysis für Performance-Trends)  
**Beispiel:** GPT-3 (2020, 175B) → GPT-3.5 (2022, 175B) → GPT-4 (2023, 1.76T) → GPT-4 Turbo (2024, 1.76T + 128k context)

---

## 📚 BibTeX-Referenzen

```bibtex
@misc{artificialanalysis2025,
  title = {Artificial Analysis: AI Model Performance Benchmarks},
  author = {{Artificial Analysis Team}},
  year = {2025},
  howpublished = {\url{https://artificialanalysis.ai/}},
  note = {Weekly updated benchmarks for latency, pricing, and quality of 100+ AI models}
}

@misc{lifearchitect2025,
  title = {Life Architect AI Models Table},
  author = {{Life Architect Community}},
  year = {2025},
  howpublished = {\url{https://lifearchitect.ai/models-table/}},
  note = {Comprehensive comparison of AI model parameters, context windows, and training dates}
}
```

---

## 🔗 Cross-Reference Map

| Thema | Verweis | Begründung |
|-------|---------|------------|
| **AI Benchmarks** | `05_technologie_tesla/ai_model_benchmarks.md` | Artificial Analysis (bereits integriert) |
| **AI Learning** | `05_technologie_tesla/ai_learning_resources.md` | Kurse, Tutorials, Roadmaps |
| **AI Research Tools** | `05_technologie_tesla/ai_research_tools.md` | Elicit, Perplexity, etc. |
| **Neuroscience ↔ AI** | `02_neurobiologie_psychologie/ai_neuroscience_parallels.md` | Transformer ↔ Attention (Hippocampus) |

---

## 🚀 Action Items

- [x] Life Architect dokumentiert
- [ ] BibTeX Batch 10 (lifearchitect2025) - Q1 2026
- [ ] AI Model Comparison Widget für 5d-dashboard (Page 4) - Q2 2026
- [ ] Historische Timeline (2020-2025) visualisieren - Q2 2026

---

**Last Updated:** 2025-12-03  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License:** CC BY 4.0
