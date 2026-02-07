## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2025-02-18 - [SPA Loading State Accessibility]
**Learning:** Loading overlays that are toggled via CSS classes (e.g., `body.loading`) are often invisible to screen readers, leaving users unaware of the state change.
**Action:** Always add `role="alert"` and `aria-live="assertive"` to loading overlays, and toggle `aria-busy="true"` on the main content area during async operations.
