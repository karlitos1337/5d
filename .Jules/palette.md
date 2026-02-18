## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2026-02-18 - Accessibility Testing with Async Data
**Learning:** In applications where UI interactivity depends on heavy async data loading (like `web/5d-map`), Playwright tests must explicitly wait for the loading state to clear (e.g., `body.loading` class removal) before interacting with elements. Standard `waitForSelector` on the element itself is insufficient if event listeners are attached late. Firefox headless environment seems particularly sensitive to this timing or resource constraint.
**Action:** Always include a dedicated wait for "application ready" state (beyond just element visibility) in E2E tests for data-heavy apps. Use `aria-pressed` for toggle buttons to provide semantic state that is also easily testable.
