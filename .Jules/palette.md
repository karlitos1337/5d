## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-10-24 - Accessible Loading Overlays
**Learning:** In single-page applications, visual loading overlays are often invisible to screen readers. Adding `role="status"` and `aria-live="polite"` ensures users are aware of background data fetching.
**Action:** Always add these attributes to loading containers and hide decorative spinners with `aria-hidden="true"`.
