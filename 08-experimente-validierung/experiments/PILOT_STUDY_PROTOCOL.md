# Quantum for Kids - Pilot Study Protocol 🧪

**Version:** 1.0  
**Last Updated:** 2025-12-03  
**Status:** Ready for execution (Week 2, Dec 2025)

---

## 🎯 Study Overview

**Goal:** Test whether interest-based quantum learning:
1. Increases engagement (IMP Score > 0.70)
2. Enables unconscious learning (kids explain concepts after)
3. Demonstrates 5D Framework in action

**Participants:** n=10 kids, age 8-14  
**Duration:** 30-45 minutes per kid  
**Location:** [TBD - School/Online]  

---

## 📋 Protocol (5 Phases)

### **Phase 1: Interest Survey (5 min)**

**Materials:** Cards with 5 icons (Minecraft, Pokemon, Soccer, Music, Hide & Seek)

**Instructions:**
1. Show all 5 cards to kid
2. "Welches magst du am liebsten?"
3. Kid chooses → **Autonomy = 1.0** ✅

**Recording:**
- Selected interest: _______
- Time to decide: _______s
- Hesitation? Yes / No

**IMP Dimension:** Autonomy (A)

---

### **Phase 2: Interactive Simulation (15-20 min)**

**Materials:** 
- Laptop with quantum simulation (Python + matplotlib OR web platform)
- Kid controls inputs (clicks blocks, heals Pokemon, etc.)

**Instructions:**
1. Run chosen simulation
2. "Du kannst klicken, probieren, experimentieren!"
3. Observe kid behavior

**Recording:**
- Time spent: _______min
- Interactions (clicks/keypresses): _______
- Retries after "failure": _______
- Hints requested: _______
- Completed? Yes / No (completion %)

**IMP Dimensions:**
- **Motivation (IM):** Time spent / expected (10 min) → IM = time/10 (max 2.0)
- **Resilience (R):** Retries / errors → R = 1 + (retries / 10) (max 2.0)
- **Authenticity (Au):** 1 - (hints / 5) → Au = 1 if no hints

---

### **Phase 3: Explanation Phase (5 min)**

**Instructions:**
1. "Das war Quantenmechanik! Kannst du's erklären?"
2. Kid explains in own words
3. Prompt: "Stell dir vor, du erzählst's einem Freund..."

**Recording (0-3 scale for each concept):**

| Concept | Explained? (0=no, 1=vague, 2=partial, 3=clear) |
|---------|-------------------------------------------------|
| Superposition / Entanglement / Wave / Interference / Tunneling | ___ |
| Real-world example | ___ |
| "Why quantum is weird" | ___ |

**Success Criterion:** ≥2 for all 3 → Unconscious learning ✅

---

### **Phase 4: Social Intent (2 min)**

**Instructions:**
1. "Möchtest du das mit Freunden teilen?"
2. Yes → SP = 1.0
3. No → SP = 0.5 (participated, but not sharing)

**Recording:**
- Wants to share? Yes / No
- Reason: _______

**IMP Dimension:** Social Participation (SP)

---

### **Phase 5: IMP Calculation (1 min)**

**Formula:**
```
IMP = A × IM × R × SP × Au
```

**Example:**
- A = 1.0 (chose freely)
- IM = 1.8 (18 min spent, expected 10)
- R = 1.5 (5 retries)
- SP = 1.0 (wants to share)
- Au = 0.8 (1 hint used)
- **IMP = 1.0 × 1.8 × 1.5 × 1.0 × 0.8 = 2.16** ✅

**Interpretation:**
- IMP > 0.70: High engagement ✅
- IMP 0.40-0.70: Moderate
- IMP < 0.40: Low (forced learning?)

---

## 📊 Data Collection

### **Per-Kid Data (Structured)**

```json
{
  "kid_id": "K001",
  "age": 10,
  "gender": "F",
  "interest": "minecraft",
  "timestamp": "2025-12-10T14:30:00Z",
  
  "phase1_autonomy": {
    "decision_time_s": 3.2,
    "hesitation": false,
    "autonomy_score": 1.0
  },
  
  "phase2_simulation": {
    "time_spent_min": 18.5,
    "interactions": 87,
    "retries": 5,
    "hints_used": 1,
    "completion_percent": 85,
    "motivation_score": 1.85,
    "resilience_score": 1.5,
    "authenticity_score": 0.8
  },
  
  "phase3_explanation": {
    "concept_1": 3,
    "concept_2": 2,
    "concept_3": 2,
    "avg_score": 2.33,
    "passed": true
  },
  
  "phase4_social": {
    "wants_to_share": true,
    "reason": "Looks cool!",
    "social_score": 1.0
  },
  
  "phase5_imp": {
    "A": 1.0,
    "IM": 1.85,
    "R": 1.5,
    "SP": 1.0,
    "Au": 0.8,
    "IMP": 2.22
  }
}
```

**Storage:** `08-experimente-validierung/experiments/pilot_data/kid_K001.json`

---

## 📈 Expected Results (Hypotheses)

### **Hypothesis 1: Interest-based → High IMP**

**Prediction:** IMP > 0.70 for ≥80% of kids (n≥8/10)

**Statistical Test:** One-sample t-test (H₀: μ = 0.50, H₁: μ > 0.70)

**Success Criterion:** p < 0.05

---

### **Hypothesis 2: Unconscious Learning**

**Prediction:** ≥70% of kids can explain quantum concept after (n≥7/10)

**Measurement:** Phase 3 avg score ≥2.0

**Statistical Test:** Proportion test (H₀: p = 0.50, H₁: p > 0.70)

**Success Criterion:** p < 0.05

---

### **Hypothesis 3: Retention After 1 Week**

**Follow-up (1 week later):**
1. Did kid come back? (Yes/No)
2. Did kid share with friends? (Yes/No)
3. Retention test: "Can you still explain quantum?"

**Prediction:** ≥70% retention (n≥7/10)

---

## 🚨 Ethical Considerations

### **Informed Consent**

**Parents/Guardians:**
- Written consent form (German + English)
- Explanation: Educational study, no risks, data anonymized
- Right to withdraw anytime

**Kids:**
- Verbal assent: "Möchtest du Quantenmechanik durch Spiele lernen?"
- Can stop anytime without reason

---

### **Data Privacy (GDPR-compliant)**

**Anonymous:**
- Kid IDs: K001, K002, ... (no names)
- No photos/videos (unless explicit consent for publication)

**Storage:**
- Encrypted JSON files (AES-256)
- Stored locally (no cloud)
- Deleted after publication (3 years max)

**Access:**
- Only research team
- No third parties

---

### **Potential Risks**

**Low-Risk Study:**
- No physical harm
- No psychological stress (it's a game!)
- Screen time: 30-45 min (within WHO guidelines)

**Mitigation:**
- Kid can pause/stop anytime
- Breaks every 10 min
- Parent present (optional)

---

## 📅 Timeline

### **Week 2 (Dec 9-16, 2025)**

**Day 1-2 (Dec 9-10):** Recruitment
- Contact 20 families (expecting 50% response → 10 participants)
- Send consent forms

**Day 3-5 (Dec 11-13):** Pilot sessions
- 3-4 kids/day
- 30-45 min/kid + 15 min setup

**Day 6-7 (Dec 14-16):** Data analysis
- Calculate IMP scores
- Visualize results
- Write report

**Week 3 (Dec 17-18):** Follow-up
- Retention test (1 week later)
- Final analysis

---

## 📊 Success Metrics

**Study is SUCCESSFUL if:**

| Metric | Target | Rationale |
|--------|--------|-----------|
| **IMP Score** | Mean > 0.70 (n≥8/10) | High engagement |
| **Unconscious Learning** | ≥70% can explain (n≥7/10) | Kids internalized concept |
| **Retention** | ≥70% remember after 1 week | Long-term learning |
| **Social Sharing** | ≥60% want to share (n≥6/10) | Social dimension validated |
| **No Dropouts** | 0 kids quit mid-study | No aversive experience |

**If ALL 5 metrics met → Hypothesis CONFIRMED** ✅

---

## 🔬 Meta-Proof (5D Framework in Action)

**The pilot study ITSELF demonstrates 5D Framework:**

| Dimension | In Study | In Learning Platform |
|-----------|----------|---------------------|
| **Autonomy (A)** | Kid chooses interest freely | Kid chooses simulation freely |
| **Motivation (IM)** | Time spent > expected | Engaged, not forced |
| **Resilience (R)** | Retries after errors | Can retry, no punishment |
| **Social (SP)** | Wants to share | Can share with friends |
| **Authenticity (Au)** | No hints needed | Learns what they want |

**Study design = Framework application** = **Recursively consistent** 🔁

---

## 📝 Next Steps (After Pilot)

### **If Successful (IMP > 0.70):**
1. **Scale up:** n=100 kids (Survey, Q2 2026)
2. **Web platform:** HTML/JS version (Q1 2026)
3. **Publication:** "Quantum Learning via Interest-Based Metaphors" (Q4 2026)

### **If Failed (IMP < 0.70):**
1. **Analyze:** Which dimension failed? (A, IM, R, SP, Au?)
2. **Iterate:** Improve simulation (more interactive? better visuals?)
3. **Retest:** Pilot 2.0 with n=10 new kids

---

## 📚 References

**Pedagogical Framework:**
- Deci & Ryan (1985): Self-Determination Theory
- Csíkszentmihályi (1990): Flow Theory
- Papert (1980): Constructionism

**Quantum Education:**
- Zollman et al. (2008): PhET Interactive Simulations
- Singh (2008): Quantum Mechanics Learning

**5D Framework:**
- This project (2025): Interest-based learning, IMP measurement

---

**Prepared by:** 5D Intelligence Framework Team  
**Contact:** See CONTRIBUTING.md  
**License:** CC BY 4.0

---

## ✅ Ready to Execute!

**Next action:** Contact 20 families (Week 2, Dec 9-16) 🚀
