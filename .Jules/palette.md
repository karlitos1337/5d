## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Accessibility State Communication
**Learning:** Visual-only loading states (like spinners) and active states (like selected tabs) are invisible to screen readers without explicit ARIA attributes (`aria-live`, `aria-busy`, `aria-pressed`).
**Action:** Always pair visual state changes (like `display: none` -> `flex` or class changes) with corresponding ARIA attributes to ensure inclusive feedback.
