## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Loading State Accessibility
**Learning:** For full-screen loading overlays in SPAs, simply showing the overlay is insufficient for screen readers. Using `aria-busy="true"` on the main content container (e.g., `<main>`) effectively communicates that the application is processing, while `role="alert"` on the overlay announces the state change.
**Action:** When implementing global loading states, always toggle `aria-busy` on the primary content region and ensure the overlay has `role="alert"` or `aria-live`.
