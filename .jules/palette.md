# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2024-12-21 - Dynamic ARIA labels for Icon-Only Toggle Buttons
**Learning:** For React applications in this repository (like `web/validation_dashboard`), icon-only toggle buttons must use dynamic `aria-label` attributes that reflect the *next* state or action (e.g., 'Switch to light mode' when dark mode is active) rather than static descriptions to ensure proper screen-reader accessibility.
**Action:** When adding or auditing icon-only toggle buttons in React apps, ensure `aria-label` attributes dynamically change to communicate the action that will occur upon activation.
