# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2026-03-17 - Skip Link main wrapper target
**Learning:** For a skip link to securely pass focus, the target (`<main>`) must have an `id`, `tabIndex="-1"` (to accept programmatic focus), and `outline-none` (so navigating via keyboard doesn't create an ugly ring on the entire document).
**Action:** When updating "Skip to content" links, verify that the target has these properties, instead of simply pointing to the first visible anchor tag on the page.
