## 2025-02-21 - Added ARIA attributes to navigation buttons
**Learning:** Icon-only toggle buttons for fundamental features like dark mode and mobile menus are common accessibility pitfalls. Screen readers cannot interpret the visual icon changes alone.
**Action:** Always ensure icon-only interactive elements receive dynamic `aria-label` attributes reflecting their current state, and use `aria-expanded` for menu toggles to provide context to assistive technologies.
