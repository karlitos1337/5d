## 2026-02-19 - Accessibility State Management
**Learning:** Toggle buttons that switch between mutually exclusive layers on a single view (map) benefit significantly from `aria-pressed` to communicate state, rather than just relying on visual class changes (like `btn--primary`).
**Action:** When implementing custom toggle groups that aren't native radio buttons, always ensure `aria-pressed` or `aria-current` is updated programmatically alongside visual classes.
