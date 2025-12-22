## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-06-05 - Accessibility in Dynamic DOM
**Learning:** React's virtual DOM doesn't automatically manage accessibility for elements created via vanilla JS (like our citation system).
**Action:** Always manually add `role`, `tabIndex`, and `aria-label` when injecting interactive elements, and mirror `onmouseenter` with `onfocus` for keyboard users.
