## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-23 - Accessible Dynamic Content
**Learning:** Dynamic content injection (like citation bubbles in React) often bypasses standard accessibility patterns. Using `sup` elements for interactivity is semantically incorrect and inaccessible to keyboard users.
**Action:** Always ensure dynamic interactive elements are keyboard-accessible (tabindex="0", role="button", onKeyDown handler).
