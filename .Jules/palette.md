## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Accessibility in React Single Page Apps
**Learning:** React Single Page Apps often use `button` for navigation scroll-spying. Without `aria-current`, screen reader users have no context on which section is active.
**Action:** Always add `aria-current` to navigation buttons/links in SPAs that highlight current section, and ensure icon-only toggle buttons have descriptive `aria-label`s.
