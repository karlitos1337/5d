## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2026-02-15 - ARIA Live Regions for Loading States
**Learning:** Adding `role="alert"` and `aria-live="assertive"` to loading overlays is critical but insufficient; toggling `aria-busy="true"` on the main content area provides essential context for screen reader users to know *what* is busy.
**Action:** Always pair visual loading indicators with `aria-live` regions and `aria-busy` attributes on the affected container.
