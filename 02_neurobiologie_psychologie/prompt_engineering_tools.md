# 🧠 Prompt Engineering Tools – SD Dynamic Prompts & Prompy

**Dimension**: 02_neurobiologie_psychologie  
**Cross-Reference**: 05_technologie_tesla (AI Tools)  
**Datum**: 2025-12-03  
**Status**: Sprint 3 - Medium-Priority Resources

---

## 📊 Übersicht

**Problem:** AI Prompts sind repetitiv, schwer zu optimieren  
**Lösung:** Tools für Prompt Generation, Testing, Marketplace

---

## 🟢 SD Dynamic Prompts (Stable Diffusion)

**URL**: https://github.com/adieyal/sd-dynamic-prompts  
**Score**: 6/10  
**Typ**: GitHub Tool (Stable Diffusion Extension)

### Features
- **Dynamic Wildcard Prompts:** `{red|blue|green} car` → randomisiert bei jedem Run
- **Combinatorial Generation:** Automatisch 100+ Variationen aus Template
- **File-based Wildcards:** `.txt` Files mit Listen (z.B. `colors.txt`, `styles.txt`)
- **Syntax:** `{option1|option2|option3}`, `{1-3$$blue|red}` (min-max range)

### Use Cases
- **Stable Diffusion:** Batch-Generation (1000 Images mit Variationen)
- **Research:** Systematisches Testen von Prompt-Variablen
- **Education:** Demonstrieren von Prompt-Engineering-Prinzipien

### Integration in 5D-Framework
- **Intrinsische Motivation (IM):** Spielerisches Experimentieren mit Prompts
- **Autonomie (A):** Keine vordefinierten Templates (User erstellt eigene Wildcards)

### BibTeX

```bibtex
@misc{sddynamicprompts2025,
  title = {SD Dynamic Prompts: Wildcard Prompt Generator for Stable Diffusion},
  author = {Adieyal},
  year = {2025},
  howpublished = {\url{https://github.com/adieyal/sd-dynamic-prompts}},
  note = {GitHub extension for Stable Diffusion, combinatorial prompt generation}
}
```

---

## 🟢 Prompy.me (Prompt Marketplace)

**URL**: https://www.prompy.me/  
**Score**: 5/10  
**Status**: ⚠️ Kritisch zu bewerten (Kommerzialisierung problematisch)

### Features
- **Prompt Marketplace:** Kaufen/Verkaufen von Prompts (GPT-4, DALL-E, etc.)
- **Preise:** $1-50 pro Prompt
- **Categories:** Marketing, Copywriting, Code, Art, Education
- **Quality:** Community-rated (5-Star System)

### Kritische Bewertung

**Probleme:**
- ❌ **Kommerzialisierung von Commons:** Prompts sind oft öffentlich verfügbar (Reddit, GitHub), aber hier kostenpflichtig
- ❌ **Quality unclear:** Keine Peer-Review, nur Community-Votes (anfällig für Manipulation)
- ❌ **Vendor Lock-In:** Prompt ist nur auf Prompy.me verfügbar (keine Portabilität)

**Alternative:** PromptBase (größer), PromptLayer (Open Source)

### Integration
- `04_oekonomie_governance/prompt_marketplace_critique.md` → Fallstudie: Wie Wissen kommerzialisiert wird
- Verweis auf Alternativen: Awesome ChatGPT Prompts (GitHub, kostenlos)

### BibTeX

```bibtex
@misc{prompy2025,
  title = {Prompy.me: Prompt Marketplace},
  author = {{Prompy Team}},
  year = {2025},
  howpublished = {\url{https://www.prompy.me/}},
  note = {Commercial prompt marketplace, \\$1-50 per prompt, problematic commodification of knowledge}
}
```

---

## 🔄 Vergleich: Free vs. Paid Prompt Resources

| Kriterium | Awesome ChatGPT Prompts (GitHub) | Prompy.me |
|-----------|-----------------------------------|-----------|
| **Kosten** | $0 | $1-50 |
| **Qualität** | ✅ Community-reviewed | ⚠️ Variabel |
| **Umfang** | 150+ Prompts | 1000+ Prompts |
| **Lizenz** | CC0 (Public Domain) | Proprietary |
| **Use Case** | Education, Research | Commercial (Marketing) |

**Empfehlung:** Awesome ChatGPT Prompts (kostenlos, qualitativ hochwertig) → Prompy nur als Backup

---

## 📚 Cross-Reference Map

| Thema | Verweis | Begründung |
|-------|---------|------------|
| **AI Tools** | `05_technologie_tesla/ai_research_tools.md` | Prompt Engineering als Research Tool |
| **Governance** | `04_oekonomie_governance/prompt_marketplace_critique.md` | Kommerzialisierung von Wissen (Critique) |
| **Free Resources** | `01_bildung_education/free_resources_mega_index.md` | Awesome ChatGPT Prompts als Alternative |

---

## 🚀 Action Items

- [x] SD Dynamic Prompts, Prompy dokumentiert
- [ ] BibTeX Batch 11 (sddynamicprompts2025, prompy2025) - Q1 2026
- [ ] Prompt Marketplace Critique File (`04_oekonomie_governance/prompt_marketplace_critique.md`) - Q2 2026
- [ ] Awesome ChatGPT Prompts integrieren (GitHub) - Q2 2026

---

**Last Updated:** 2025-12-03  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License:** CC BY 4.0
