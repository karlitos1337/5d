## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-10-24 - Initial State Synchronization
**Learning:** Reliance on JS to set initial ARIA states (like `aria-pressed`) creates a gap where screen readers report incorrect states during loading. Progressive enhancement isn't just for no-JS; it's for *slow* JS too.
**Action:** Always hardcode valid initial ARIA attributes in HTML that match the visual "default" state, rather than waiting for `init()` logic to apply them.
