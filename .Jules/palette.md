## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2026-02-16 - Accessible Toggle Buttons in Leaflet Maps
**Learning:** Layer switcher controls often rely purely on visual cues (like `btn--primary` classes). This leaves screen reader users unaware of the active state. Adding `aria-pressed` dynamically via JS is a critical, invisible fix for toggle buttons.
**Action:** Always verify that state changes (active/inactive) are communicated semantically, not just visually. Use `aria-pressed` for toggle buttons and `aria-busy` for loading overlays.
