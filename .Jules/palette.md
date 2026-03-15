## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Accessibility in Single Page Apps
**Learning:** Loading states in SPAs often go unnoticed by screen readers if they are just toggled divs. Adding role="status" and aria-live="polite" to the container ensures the "Loading..." message is announced when it appears.
**Action:** Always wrap loading spinners/overlays in a live region.
