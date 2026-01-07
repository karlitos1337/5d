# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2026-01-07 - Dynamic Citation Accessibility
**Learning:** Interactive elements generated dynamically (like citation superscripts) are often overlooked in accessibility audits. Replacing semantic but non-interactive tags (like `<sup>`) with interactive ones (`<button>`) significantly improves keyboard navigability without sacrificing visual design if styled correctly.
**Action:** Always verify that dynamically injected "clickable" elements are actual buttons or links, not just stylized spans or sups.
