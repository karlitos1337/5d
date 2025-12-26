## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Dynamic Citation Accessibility
**Learning:** Dynamically injecting interactive elements (like `<sup>` citations) often bypasses standard component accessibility checks. These "invisible" elements are frequently missed by linters but create significant barriers for keyboard and screen reader users.
**Action:** When working with direct DOM manipulation in React (like `document.createElement`), explicit `setAttribute` calls for `role`, `tabIndex`, `aria-label`, and `onkeydown` handlers are mandatory to match the accessibility of standard React components.
