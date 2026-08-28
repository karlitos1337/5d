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
## 2025-02-28 - Accessibility and Keyboard Navigation
**Learning:** Interactive elements need clear visual states (focus-visible) and screen reader unfriendly content needs language definitions (lang="de").
**Action:** Always verify keyboard focus states and ensure language tags are accurate for non-English content during testing.
## 2025-04-24 - Navigation Button Accessibility
**Learning:** Custom icon-only navigation buttons in React dashboards frequently lack aria-labels, title attributes, and clear keyboard focus states, hindering accessibility and navigation for screen readers and keyboard users.
**Action:** Always ensure interactive elements without visible text include `aria-label` and `title` attributes, and utilize styles like `focus-visible:ring` to provide clear keyboard focus indicators.
## 2024-05-24 - Update Validation Dashboard
**Learning:** When modifying React applications with German content, it's crucial to verify and update the `<html lang="de">` attribute to ensure proper screen reader pronunciation.
**Action:** Added `<html lang="de">` in index.html and integrated framer-motion animations.

## 2025-04-14 - [Accessibility] Improve Keyboard Nav and Screen Reader Support
**Learning:** React Single Page Applications often miss basic accessibility features like "Skip to content" links, ARIA labels on icon-only buttons, and sufficient focus ring contrast when dark mode is managed via state.
**Action:** Added `aria-label` and `title` to icon buttons, ensured the `<main>` tag had the correct `id` and `tabIndex="-1"`, and implemented dynamic focus ring offsets (`focus-visible:ring-offset-*`) for better contrast in both light and dark modes.
## 2024-05-25 - [Accessibility] Consistent Skip Links in React Apps
**Learning:** `docs/analysis` lacked a complete "skip to main content" implementation: the `<a href="#main-content" ...>` skip link was missing, and the corresponding `<main id="main-content" tabIndex="-1" ...>` target also had to be added so the interaction would work correctly for keyboard and assistive technology users.
**Action:** When auditing React SPA dashboards, explicitly verify both parts are implemented together: the `<main id="main-content" tabIndex="-1" ...>` target exists AND the `<a href="#main-content" ...>` skip link is present at the beginning of the application's layout.
## 2024-04-07 - Dynamic Focus Rings for Dark Mode
**Learning:** When managing dark mode via React state (e.g., `darkMode` variable) instead of Tailwind's native `dark:` classes, focus rings (`focus-visible:ring-offset-*`) must be dynamically applied using conditional template literals to ensure proper contrast.
**Action:** Always use conditional expressions for focus ring offset colors (e.g., `${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'}`) in such components.
## 2024-04-08 - Match HTML lang attribute with content language
**Learning:** React scaffolds like Vite default to `lang="en"`, but if the content is in another language (e.g., German), it severely impacts screen reader pronunciation, breaking basic accessibility.
**Action:** Always verify that the `<html lang="...">` attribute matches the actual localization of the application content.

## 2025-04-11 - [Accessibility] Correct language attributes in React scaffolds
**Learning:** React scaffolds like Vite default to `lang="en"` in `index.html`. For applications with non-English content (e.g., German), failing to update the `<html lang="...">` attribute causes screen readers to mispronounce the content, creating a poor user experience.
**Action:** Always verify and update the `<html lang="...">` attribute to match the actual localization of the application to ensure proper screen reader pronunciation.
## 2024-05-24 - [Accessibility] Skip Link in React Analysis Dashboard
**Learning:** The "Zum Hauptinhalt springen" skip link was added to `docs/analysis/src/App.jsx`, but the `<main>` tag was missing the corresponding `id="main-content"`, meaning the link was not functional. Furthermore, the `<main>` tag also needed `tabIndex="-1"` and `outline-none` so that it could receive programmatic focus after jumping, without leaving an unsightly default focus ring. We also fixed the icon-only buttons missing `aria-label`, `title`, and dynamic focus offset rings.
**Action:** When adding skip links, always verify that the target element actually has the corresponding `id`, `tabIndex="-1"`, and a hidden focus style (`outline-none` or equivalent) to ensure a complete and polished accessible interaction. Ensure icon-only buttons receive `aria-label`, `title`, and dynamically styled focus rings based on dark/light mode state.
## 2025-04-04 - [Accessibility] Missing semantic ARIA and dynamic focus labels
**Learning:** When dealing with interactive icon buttons in React SPAs, a common anti-pattern is leaving them unlabelled for screen readers, meaning only their visual presence provides context. Additionally, applying standard tailwind focus styles to fixed headers over dynamic dark mode backgrounds can result in poor contrast for keyboard focus rings. Adding semantic labels (`aria-label`, `title`) and state-aware focus styles vastly improves accessibility with minimal code changes.
**Action:** Ensure icon-only buttons always include `aria-label` and `title` tags corresponding to their function and state. Use dynamic template literals to adjust `focus-visible` classes based on the current background state, ensuring high contrast visibility for keyboard users.
## 2026-08-28 - Dynamic Citation Keyboard Accessibility
**Learning:** Injected citation markers (e.g., dynamically created sup elements in React) require manual implementation of keyboard event handlers (onkeydown), role (link), and tabindex to be accessible since they bypass standard React accessibility flows.
**Action:** Always manually configure ARIA roles, tabindex, and keyboard events for DOM elements injected outside of the React lifecycle.
