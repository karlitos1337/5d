## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2026-02-25 - JS Class Toggling vs. ARIA State
**Learning:** In the `5d-map` vanilla JS app, state changes (like active layers) were managed solely by toggling CSS classes (`btn--primary`), leaving assistive technology unaware of the change. This pattern requires manual synchronization of ARIA attributes (`aria-pressed`).
**Action:** When observing `classList.toggle` or `add/remove` for stateful UI elements, immediately check if a corresponding ARIA attribute (like `aria-pressed`, `aria-expanded`, or `aria-selected`) needs to be updated in parallel.
