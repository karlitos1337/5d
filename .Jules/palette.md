## 2024-05-23 - Micro-UX in Streamlit
**Learning:** Streamlit metrics lack built-in explanations by default, making dashboards confusing for new users. Adding `help` tooltips to `st.metric` is a high-impact, low-effort micro-UX win.
**Action:** When working on Streamlit dashboards, always check if metrics are self-explanatory. If not, add context via the `help` parameter. Also, `st.toast` is great for feedback on long-running processes.

## 2025-05-23 - Dynamic DOM in React & Accessibility
**Learning:** React applications that manipulate the DOM directly (e.g., in `useEffect`) often bypass React's declarative accessibility features. Specifically, dynamically created buttons (like citation superscripts) are completely invisible to keyboard users (no `tabindex`, no `onkeydown`) and screen readers (no `aria-label`, no `role`) unless explicitly handled.
**Action:** When seeing `document.createElement` in React, immediately audit for accessibility: add `tabIndex="0"`, `role="button"`, `aria-label`, and `onkeydown` (Enter/Space) handlers to ensure parity with native buttons.
