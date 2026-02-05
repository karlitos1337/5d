## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2025-05-15 - Accessible Loading States
**Learning:** Adding `role="status"` and `aria-live="polite"` to loading overlays is standard, but pairing it with `aria-busy="true"` on the main content area provides a more robust signal to assistive technologies that the current context is updating.
**Action:** When implementing global loading states, always toggle `aria-busy` on the main container in addition to showing the visual spinner.
