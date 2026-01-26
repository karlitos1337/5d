# Palette's Journal - Critical UX/A11y Learnings

## 2025-02-24 - Focus States and Tactile Feedback
**Learning:** The application lacked visible focus states for keyboard navigation, making it inaccessible for keyboard users. Buttons also lacked "active" (pressed) states, making interaction feel flat.
**Action:** Implemented global `:focus-visible` styles using the primary color and added `.btn:active` for tactile feedback. Always check `styles.css` for basic interactive states before assuming they exist.
