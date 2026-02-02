## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Loading State Accessibility
**Learning:** Loading overlays often lack semantic meaning for screen readers. Using `role="status"` and `aria-live="polite"` transforms a silent visual wait into an announced state change, significantly improving the non-visual experience.
**Action:** Audit all loading spinners/overlays for ARIA attributes. Ensure purely visual spinners are hidden with `aria-hidden="true"` to prevent navigation noise.
