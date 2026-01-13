## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2024-10-24 - Streamlit Contextual Tooltips
**Learning:** Users unfamiliar with specific domain metrics (like ROI or IMP) need immediate context without leaving the dashboard.
**Action:** Use `help` parameter in `st.metric` and `st.download_button` to provide definitions and context inline. This reduces cognitive load and improves accessibility.
