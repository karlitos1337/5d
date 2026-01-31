## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Accessible Loading Overlays
**Learning:** Single Page Applications often use `div` overlays for loading. Without ARIA roles, screen readers stay silent. `role="status"` + `aria-live="polite"` is the robust pattern.
**Action:** Ensure loading containers have `role="status"` and visual spinners have `aria-hidden="true"`.
