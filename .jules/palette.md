# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2026-03-06 - Dynamic ARIA labels and Focus Styles
**Learning:** For React toggle buttons (e.g., dark mode, mobile menu), static ARIA labels are insufficient. The `aria-label` must dynamically reflect the *next* state or action (e.g., "Switch to light mode" when dark mode is active) rather than a static description. Additionally, default browser focus outlines may fail on rounded Tailwind elements, requiring explicit `focus-visible:ring-2 focus-visible:outline-none` styles to ensure keyboard navigation is visually obvious.
**Action:** Always verify that state-dependent icon-only toggles use dynamic `aria-label` strings and explicitly define `focus-visible` styles on custom or rounded interactive components.
