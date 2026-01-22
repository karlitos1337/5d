## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-05-24 - Interactive Button Accessibility
**Learning:** Adding `aria-expanded` and `aria-controls` to mobile menu toggles not only helps screen readers but clarifies the relationship between the button and the content it reveals, preventing "what did that do?" moments.
**Action:** Always pair toggle buttons with `aria-expanded` and link them to their target container via `aria-controls` and `id`.
