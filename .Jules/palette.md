## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Dynamic Accessibility in React Effects
**Learning:** React `useEffect` hooks that manually inject DOM elements (like citation superscripts) often bypass standard JSX accessibility props. These dynamically created elements are invisible to screen readers and keyboard users unless explicitly enhanced with `role="button"`, `tabIndex="0"`, `aria-label`, and `onkeydown` handlers.
**Action:** When auditing React codebases, specifically look for `document.createElement` inside `useEffect` hooks. Always retrofit these with full ARIA and keyboard support to match the accessibility of standard JSX components.
