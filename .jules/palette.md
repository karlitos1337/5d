# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2025-02-23 - Manual DOM Manipulation Risks
**Learning:** The citation system uses `document.createElement` within `useEffect`, creating interactive elements that bypass React's accessibility checks. These dynamically injected buttons lacked ARIA labels and keyboard focus management.
**Action:** When inspecting code that manually injects DOM elements (common in legacy integrations or specific visualizations), explicitly audit the injected elements for accessibility attributes.
