# 🔒 Security Fundamentals – HackTricks & AweXplor

**Dimension**: 05_technologie_tesla  
**Cross-Reference**: ETHIK_MANIFEST.md (Ethics, Legal Use)  
**Datum**: 2025-12-03  
**Status**: Sprint 2 - Cybersecurity Education (with Ethics Disclaimer)

---

## 📊 Übersicht

**Ziel:** Cybersecurity-Bildung für Pentesting, Bug Bounty, Security Research  
**Scope:** **Nur legale Nutzung** (White Hat, keine Black Hat Aktivitäten)

---

## ⚠️ ETHIK-DISCLAIMER

### ✅ LEGALE Nutzung
- **Pentesting mit Erlaubnis** (White Hat, autorisiert von System-Owner)
- **Bug Bounty Programs** (HackerOne, Bugcrowd, Synack)
- **Security Research** (CVE-Disclosure, Responsible Disclosure)
- **Bildung** (Cybersecurity-Kurse, CTFs, Capture The Flag)

### ❌ ILLEGALE Nutzung
- **Unauthorized Access** (Black Hat, ohne Erlaubnis)
- **Data Theft** (Exfiltrieren von Daten)
- **Ransomware/Malware** (Distributed Denial of Service)
- **Hacking ohne Consent** (Strafbar nach StGB §202a-c, Deutschland)

**Referenz:** `ETHIK_MANIFEST.md` → "Technologie ist neutral, Nutzung bestimmt Ethik"

---

## 🟡 HackTricks (Pentesting Encyclopedia)

**URL**: https://book.hacktricks.xyz/  
**Score**: 8/10  
**Status**: ⚠️ Ethisch sensibel (nur legale Nutzung)

### Features
- **3,000+ Pentesting Techniques:** Linux, Windows, Web, Mobile, Cloud, Network
- **Community-maintained:** GitHub (3k+ Contributors)
- **Structure:** GitBook (Markdown, versioned, searchable)
- **Topics:**
  - **Web:** XSS, SQL Injection, CSRF, SSRF, XXE
  - **Linux:** Privilege Escalation, Kernel Exploits
  - **Windows:** Active Directory, NTLM, Kerberos
  - **Mobile:** Android, iOS, APK Reverse Engineering
  - **Cloud:** AWS, GCP, Azure Security Misconfigurations

### Use Cases (Legal)
1. **Bug Bounty:** HackerOne (Facebook, Google, Tesla), Bugcrowd
2. **Red Team:** Corporate Penetration Testing (mit Vertrag)
3. **CTFs:** Capture The Flag Competitions (Hack The Box, TryHackMe)
4. **Education:** Cybersecurity-Kurse (OSCP, CEH, CISSP)

### Integration in 5D-Framework
- **Autonomie (A):** Selbstgesteuertes Lernen (keine Zertifizierungszwang)
- **Intrinsische Motivation (IM):** Gamification (CTFs, Bug Bounty Rewards)
- **Resilienz (R):** Security = Resilienz gegen Angriffe

### BibTeX

```bibtex
@misc{hacktricks2025,
  title = {HackTricks: Pentesting Techniques Encyclopedia},
  author = {{HackTricks Community}},
  year = {2025},
  howpublished = {\url{https://book.hacktricks.xyz/}},
  note = {3,000+ pentesting techniques, educational use only, legal pentesting with permission}
}
```

---

## 🗂️ AweXplor (Awesome Lists Explorer)

**URL**: https://awe.xplor.ing/  
**Score**: 7/10  
**Typ**: Alternative zu GitHub Awesome

### Features
- **300+ Awesome Lists:** Aggregiert GitHub Awesome (Software, Data, ML, Security, etc.)
- **Search & Filter:** Tags, Kategorien, Sternzahl, Language
- **UI:** Bessere UX als GitHub Search (Grid View, Card Layout)
- **API:** JSON-Endpoints (für Integration in 5d-map)

### Integration in 5D-Framework
- **Architecture Study:** Wie organisiert AweXplor Knowledge Graphs? (Neo4j? PostgreSQL?)
- **Lessons für 5d-map:** 
  - Tag-System (multi-tag support)
  - Filterfunktionen (Boolean AND/OR)
  - API-Design (RESTful, JSON)
- **Cross-Reference:** `06_synthesen_kompilationen/learn_anything_competitor_analysis.md` → AweXplor als 3. Competitor

### BibTeX

```bibtex
@misc{awexplor2025,
  title = {AweXplor: Awesome Lists Explorer},
  author = {{AweXplor Team}},
  year = {2025},
  howpublished = {\url{https://awe.xplor.ing/}},
  note = {Aggregates 300+ GitHub Awesome lists, improved UX, JSON API}
}
```

---

## 🔄 Vergleich: HackTricks vs. Traditional Resources

| Kriterium | HackTricks | OWASP | NIST CVE | Offensive Security |
|-----------|------------|-------|----------|-------------------|
| **Fokus** | Praktisch (How-To) | Konzeptuell (Guidelines) | Database (CVEs) | Training (OSCP) |
| **Community** | ✅ Open (GitHub) | ✅ Open (OWASP) | ✅ Public (NIST) | ❌ Proprietary ($$$) |
| **Update-Frequenz** | Täglich | Monatlich | Täglich | Jährlich |
| **Cost** | $0 | $0 | $0 | $999+ |

**Empfehlung:** HackTricks (Praxis) + OWASP (Theorie) = kostenlose Alternative zu OSCP

---

## 📚 Cross-Reference Map

| Thema | Verweis | Begründung |
|-------|---------|------------|
| **Ethics** | `ETHIK_MANIFEST.md` | "Technologie ist neutral, Nutzung bestimmt Ethik" |
| **AI Security** | `05_technologie_tesla/ai_security.md` | AI-spezifische Angriffe (Prompt Injection, Model Stealing) |
| **Competitor Analysis** | `06_synthesen_kompilationen/learn_anything_competitor_analysis.md` | AweXplor als 3. Competitor (neben Learn Anything) |

---

## 🚀 Action Items

- [x] HackTricks, AweXplor dokumentiert
- [ ] BibTeX Batch 10 (hacktricks2025, awexplor2025) - Q1 2026
- [ ] ETHIK_MANIFEST erweitern (Security Ethics Sektion) - Q1 2026
- [ ] AI Security File erstellen (`05_technologie_tesla/ai_security.md`) - Q2 2026

---

**Last Updated:** 2025-12-03  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License:** CC BY 4.0
