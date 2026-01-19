## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Imperative DOM and Accessibility
**Learning:** When using `document.createElement` inside React `useEffect` (e.g., for citation bubbles), accessibility features like `tabindex`, `role`, and keyboard handlers are often forgotten because they aren't part of the declarative JSX flow.
**Action:** Audit any manual DOM manipulation code for missing a11y attributes. Explicitly add `role='button'`, `tabindex='0'`, and `onkeydown` handlers for interactive elements created via JS.
