## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Custom Map Controls Accessibility
**Learning:** Dynamically created map controls (like Leaflet legends) are often simple `div`s that lack accessibility. They need explicit `tabindex="0"`, `role="button"`, and `keydown` handlers to be usable by keyboard.
**Action:** When creating custom Leaflet controls, always wrap them in an accessible container or add proper ARIA attributes and keyboard listeners to interactive elements.
