## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Loading State Accessibility
**Learning:** Full-screen loading overlays interrupt the user flow and should be treated as alerts (`role="alert"` or `aria-live="assertive"`). Additionally, the main content should be marked with `aria-busy="true"` to indicate updates are happening.
**Action:** When implementing global loading states, ensure the overlay announces itself immediately and the underlying content signals it is busy.
