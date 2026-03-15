# Palette's Journal

## 2024-05-22 - Skip Link Implementation
**Learning:** Even single-page map applications need skip links because the header controls can be dense and repetitive for keyboard users.
**Action:** Always check for `main` content accessibility and provide a bypass mechanism for repeated navigation blocks.

## 2024-12-21 - React Dashboard Accessibility
**Learning:** React Single Page Applications (SPAs) often miss basic accessibility features like "Skip to content" links and ARIA labels on icon-only buttons, which are critical for keyboard and screen reader users. Adding these is a low-effort, high-impact improvement.
**Action:** When auditing React apps, immediately check for skip links and ensure all icon-only buttons (like dark mode toggles) have descriptive `aria-label` attributes.

## 2025-03-14 - Fix UI syntax and a11y properties in React SPA
**Learning:** During accessibility and UI audits in React SPAs (like `web/validation_dashboard`), it is common to find components with incorrectly duplicated JSX properties (e.g., duplicated `className` declarations, duplicate `aria-label` definitions on the same element), often resulting from botched copy/paste operations or auto-merges. Additionally, simple syntax errors in React hooks (like misaligned brackets in `useEffect`) can crash the linter and production build.
**Action:** When performing UX/a11y improvements, always thoroughly inspect JSX elements for duplicated props and syntax errors, and rigorously enforce the validation process using both local linters (`pnpm lint`) and the production build step (`pnpm build`).
