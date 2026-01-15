## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-10-25 - Accessibility in Icon-Only Buttons
**Learning:** Icon-only buttons (like Dark Mode or Mobile Menu toggles) often get overlooked for accessibility. React frameworks like Vite/Tailwind make it easy to create them visually, but they default to being invisible to screen readers. Adding `aria-label` is critical. For menus, `aria-expanded` and `aria-controls` provide essential context about state and relationship.
**Action:** Always audit icon-only buttons. Add `aria-label` describing the action. For toggles, use dynamic labels (e.g., "Switch to dark mode" vs "Switch to light mode") or state attributes (`aria-expanded`).
