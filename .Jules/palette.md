## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2025-02-04 - Accessible Loading States
**Learning:** Loading overlays often lack ARIA attributes, leaving screen reader users in the dark. Adding `role="status"` and `aria-live="polite"` is crucial for announcing state changes without interrupting.
**Action:** Always audit loading states for `role="status"` and `aria-live` attributes. Use `aria-hidden="true"` for purely visual spinners.
