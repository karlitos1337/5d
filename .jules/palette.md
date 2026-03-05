# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.
\n## 2024-05-23 - Focus Visible Outline\n**Learning:** Relying on default browser outlines can sometimes fail on custom styled components (like Tailwind rounded buttons). Explicitly defining a focus-visible outline is a micro-UX pattern that makes keyboard navigation significantly more obvious.\n**Action:** Apply `focus-visible:ring` or similar styles to all interactive elements, especially icon-only buttons.
