## 2024-05-22 - Skip Link & ARIA Labels in React/Vite
**Learning:** Modern SPAs often miss basic navigation aids. Adding a "Skip to content" link requires `sr-only focus:not-sr-only` styles to be usable. Also, `aria-label` is essential for icon-only buttons (like Dark Mode toggles) which are invisible to screen readers otherwise.
**Action:** Always check for `aria-label` on icon buttons and ensure a `#main-content` target exists for skip links.
