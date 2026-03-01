# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2025-03-01 - Dynamic ARIA Labels on Icon Buttons
**Learning:** Icon-only toggle buttons (like dark mode or mobile menu toggles) often get overlooked for accessibility because the visual icon provides the context for sighted users. However, for screen readers, a static `aria-label` like "Toggle Dark Mode" is less helpful than a dynamic one that describes the *action* that will happen next (e.g., "Switch to light mode" when dark mode is currently active).
**Action:** Always implement dynamic `aria-label` values for stateful icon-only buttons that reflect the *next* state, rather than just describing the general function of the button.
