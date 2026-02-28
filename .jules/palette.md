# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2025-02-28 - Dynamic React Elements Require Manual A11y
**Learning:** Dynamically created DOM elements in React using `document.createElement()` (like the citation buttons in `App.jsx`) bypass React's declarative accessibility features. They require manual implementation of `role="button"`, `tabIndex="0"`, `aria-label`, and custom keyboard event handlers (`onkeydown` checking for 'Enter' or 'Space') to be accessible to screen readers and keyboard users.
**Action:** Always verify that dynamic non-JSX elements have complete manual accessibility attributes and keyboard event handlers added directly via DOM manipulation (e.g., `setAttribute`).
