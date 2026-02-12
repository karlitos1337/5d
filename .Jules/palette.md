## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-23 - Accessibility of Visual Toggle States
**Learning:** In the 5D-Map app, layer buttons used `.btn--primary` for active state but lacked `aria-pressed`. This creates a disconnect between visual and semantic state for screen reader users.
**Action:** Always pair visual state toggles (like `.active` or `.btn--primary`) with semantic attributes like `aria-pressed="true"` or `aria-current="true"` to ensure inclusivity.
