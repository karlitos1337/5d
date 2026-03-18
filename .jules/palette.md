# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2026-03-18 - [Skip-to-Content Focus Management]
**Learning:** When creating a 'Skip to main content' link that targets a `<main>` container element rather than an interactive element like a link or button, the target container must have `tabIndex="-1"` to properly receive programmatic focus from the skip link. Otherwise, keyboard users will jump back to the top of the page on their next tab press. Additionally, applying `outline-none` to the container prevents an ugly default browser focus ring from appearing around the entire main content area when it receives focus.
**Action:** Always ensure skip-to-content target containers have both `tabIndex="-1"` and appropriate focus styling (e.g., `outline-none`) to provide a seamless and accessible keyboard navigation experience.
