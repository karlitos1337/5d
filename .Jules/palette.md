## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2026-02-26 - [ARIA Attributes for Dynamic State]
**Learning:** Application state changes (like "loading" overlays or "active" layer buttons) are often invisible to screen readers without explicit ARIA attributes like `aria-busy` and `aria-pressed`.
**Action:** When toggling visual classes (e.g., `btn--primary`, `loading`), always toggle the corresponding ARIA attribute (`aria-pressed`, `aria-busy`) in the same function.
