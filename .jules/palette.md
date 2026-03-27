## 2024-05-18 - [Accessibility] Fix missing target for "skip to main content" link
**Learning:** The "Zum Hauptinhalt springen" skip link was added to `App.jsx`, but the `<main>` tag was missing the corresponding `id="main-content"`, meaning the link was not functional. Furthermore, the `<main>` tag also needed `tabIndex="-1"` and `outline-none` so that it could receive programmatic focus after jumping, without leaving an unsightly default focus ring.
**Action:** When adding skip links, always verify that the target element actually has the corresponding `id`, `tabIndex="-1"`, and a hidden focus style (`outline-none` or equivalent) to ensure a complete and polished accessible interaction.

## 2024-05-23 - [Accessibility] Semantic DOM Insertion for Citations
**Learning:** When dynamically generating interactive elements in the DOM (like custom citations via `data-ref` attributes) within parsed markdown content, appending children directly to void HTML elements (like `<img>`) causes DOM exceptions. Furthermore, using non-semantic tags like `<sup>` with `onclick` handlers breaks keyboard navigability and screen reader support.
**Action:** Use sibling insertion (e.g., `el.parentNode.insertBefore(btn, el.nextSibling)`) instead of `appendChild` for custom logic around void elements. Always replace `onclick` spans/sups with semantic HTML tags (e.g., `<a>` with `href`, `target="_blank"`, and `aria-label`) to ensure proper keyboard navigability and accessibility.

## 2025-03-27 - [Skip-To-Content Link Requires Proper Focus Handling]
**Learning:** Adding a "Zum Hauptinhalt springen" (skip to main content) link requires setting `id="main-content"` on the main container, along with `tabIndex="-1"` and an `outline-none` class to prevent an ugly focus ring when the skip link forces focus onto the main container. This is a common pattern for single-page applications where the focus needs to be programmatically shifted upon skip link activation.
**Action:** Always include `tabIndex="-1"` and `outline-none` on the target container when implementing skip links to ensure seamless and visually clean keyboard navigation.
