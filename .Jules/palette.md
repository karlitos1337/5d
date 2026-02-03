## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-10-24 - Accessible Loading Overlays
**Learning:** Single-page app loading overlays are often invisible to screen readers. Adding `role="status"` and `aria-live="polite"` makes them announced without interrupting the user aggressively.
**Action:** Ensure all `.loading-overlay` or similar blocking states include these attributes and hide decorative spinners with `aria-hidden="true"`.
