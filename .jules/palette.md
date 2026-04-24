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
## 2024-05-24 - Dynamic Focus Rings in Dark Mode
**Learning:** When improving keyboard accessibility in React applications that manage dark mode via state variables (like `darkMode`) rather than Tailwind's native `dark:` classes, static focus-visible offsets can cause contrast issues.
**Action:** Dynamically apply the appropriate focus ring offset colors using conditional template literals (e.g., `${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'}`) to ensure proper contrast in both light and dark themes.

## 2024-05-24 - [Accessibility] Consistent Focus Rings and Tooltips for Interactive Elements
**Learning:** React Single Page Applications often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons. Additionally, relying solely on `aria-label` without a `title` attribute for icon-only buttons hides functionality from mouse users who rely on tooltips. Furthermore, when managing dark mode via state rather than native classes, keyboard focus rings must explicitly offset against the dynamic background color.
**Action:** When adding screen-reader accessibility (`aria-label`) to icon-only buttons, complement it by adding matching `title` attributes. Improve keyboard accessibility by dynamically applying appropriate focus ring offset colors using conditional template literals (e.g., `${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'}`) to ensure proper contrast.
## 2025-04-03 - [Accessibility] Conditional Focus Ring Offsets
**Learning:** When adding `focus-visible` ring styles to interactive elements in a React application that manually manages dark mode via state (e.g., `const [darkMode, setDarkMode] = useState(false)`), using standard Tailwind `ring-offset` classes can cause contrast issues. Standard `dark:` prefixes do not work if the application does not utilize the standard class-based dark mode implementation.
**Action:** Always verify the dark mode implementation strategy of the application. If it relies on a manual state variable, dynamically apply the appropriate `focus-visible:ring-offset-*` color using conditional template literals (e.g., `${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'}`) to ensure proper contrast and accessibility for keyboard navigation.
## 2025-04-24 - Navigation Button Accessibility
**Learning:** Custom icon-only navigation buttons in React dashboards frequently lack aria-labels, title attributes, and clear keyboard focus states, hindering accessibility and navigation for screen readers and keyboard users.
**Action:** Always ensure interactive elements without visible text include `aria-label` and `title` attributes, and utilize styles like `focus-visible:ring` to provide clear keyboard focus indicators.
