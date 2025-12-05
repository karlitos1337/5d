---
title: Quellen & Zitieren – Kurzguide
author: Repo Maintainers
date: 2025-12-05
domain: docs
license: CC-BY-4.0
evidence: ✅
bibtex_keys: [deci1985intrinsic, ryan2000sdt]
---

Ziel: Einheitliche Zitierpraxis mit BibTeX‐Single‐Source `07_daten_analysen/5d-relevant-sources.bib`.

Empfehlungen:
- Verwende prägnante Keys wie `deci1985intrinsic`, `ryan2000sdt`.
- Verweise im Fließtext knapp: `[Ryan & Deci, 2000]` und trage den BibTeX‐Key ins Frontmatter (`bibtex_keys`).
- Bei neuen Behauptungen: Evidence‐Label setzen (✅ Fakt, ⚠️ Hypothese, 🔮 Spekulation) und Quelle ergänzen.

Mini‐Beispiel (Markdown + Frontmatter):

```markdown
---
title: Intrinsische Motivation – Überblick
author: Karl
date: 2025-12-05
domain: 01_bildung_education
license: CC-BY-4.0
evidence: ✅
bibtex_keys: [ryan2000sdt]
---

Die SDT zeigt, dass Autonomie zentrale Voraussetzung ist [Ryan & Deci, 2000].
```

Hinweis: BibTeX‐Datei pflegen unter `07_daten_analysen/5d-relevant-sources.bib`. Bei fehlenden Einträgen, Key vorschlagen und Eintrag ergänzen.
