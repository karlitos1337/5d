## 2025-05-27 - Missing ARIA Labels on Interactive Elements
**Learning:** A common accessibility issue in this dashboard is icon-only buttons (like dark mode toggles or mobile menus) missing `aria-label` or `aria-expanded` attributes. This makes them invisible or confusing to screen reader users.
**Action:** Always verify icon-only buttons have descriptive `aria-label` attributes during code reviews or when modifying components.

## 2025-05-27 - Scroll-based Navigation Feedback
**Learning:** Long single-page applications often lack easy navigation back to the top, which can be frustrating on mobile devices or after deep reading.
**Action:** Implement a "Back to Top" button that appears after scrolling, providing a quick way to return to the navigation menu.
