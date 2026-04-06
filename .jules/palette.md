## 2024-05-18 - [Accessibility] Fix missing target for "skip to main content" link
**Learning:** The "Zum Hauptinhalt springen" skip link was added to `App.jsx`, but the `<main>` tag was missing the corresponding `id="main-content"`, meaning the link was not functional. Furthermore, the `<main>` tag also needed `tabIndex="-1"` and `outline-none` so that it could receive programmatic focus after jumping, without leaving an unsightly default focus ring.
**Action:** When adding skip links, always verify that the target element actually has the corresponding `id`, `tabIndex="-1"`, and a hidden focus style (`outline-none` or equivalent) to ensure a complete and polished accessible interaction.

## 2024-05-23 - [Accessibility] Semantic DOM Insertion for Citations
**Learning:** When dynamically generating interactive elements in the DOM (like custom citations via `data-ref` attributes) within parsed markdown content, appending children directly to void HTML elements (like `<img>`) causes DOM exceptions. Furthermore, using non-semantic tags like `<sup>` with `onclick` handlers breaks keyboard navigability and screen reader support.
**Action:** Use sibling insertion (e.g., `el.parentNode.insertBefore(btn, el.nextSibling)`) instead of `appendChild` for custom logic around void elements. Always replace `onclick` spans/sups with semantic HTML tags (e.g., `<a>` with `href`, `target="_blank"`, and `aria-label`) to ensure proper keyboard navigability and accessibility.

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2024-05-24 - [Accessibility] Enhanced Icon-Only Buttons
**Learning:** When using custom dark mode implementations in React, standard `focus-visible` styles can lack contrast. Additionally, icon-only buttons need `title` attributes alongside `aria-label`s to assist mouse users with native tooltips.
**Action:** Always complement `aria-label` with a matching `title` on icon-only buttons. For focus rings in custom dark mode applications, conditionally apply offset colors (e.g., `${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'}`).
