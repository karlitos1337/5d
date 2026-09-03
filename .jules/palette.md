## 2024-05-14 - React Dependency Arrays and Linting
**Learning:** Static arrays or objects used within React hooks (like `useEffect`) should be defined outside the component function body. If they are defined inside, ESLint's `react-hooks/exhaustive-deps` will flag them because a new reference is created on every render.
**Action:** Always extract constant/static data configurations out of React component scopes to maintain stable references and pass strict linting configurations without needing `useMemo`.

## 2024-05-14 - Scroll Spy with IntersectionObserver
**Learning:** Raw scroll event listeners checking offsets (like `scrollY + 200`) can cause layout thrashing and don't match the modern web performance standard.
**Action:** Replace raw scroll event calculation logic with an `IntersectionObserver` using a negative `rootMargin` (like `'-20% 0px -79% 0px'`) to accurately recreate scroll-spy active link behavior performantly.

## 2024-05-14 - Dynamic Non-React Elements and Accessibility
**Learning:** If elements are injected into a React application using raw DOM APIs (e.g., `document.createElement('sup')`) to bypass standard frameworks, they completely miss any React-level accessibility wrappers.
**Action:** You must manually attach specific accessible properties to dynamically injected DOM nodes, including `role='button'`, `tabIndex=0`, and an `onkeydown` listener that handles 'Enter' or ' ' to replicate native focusable interactive elements.
