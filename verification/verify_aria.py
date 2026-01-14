import re
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # We need to map the base URL since the preview server might serve at /5d/docs/analysis/
        # Usually vite preview runs on 4173
        context = browser.new_context()
        page = context.new_page()

        # Try to navigate to the preview URL.
        # Since base is /5d/docs/analysis/, we might need to hit http://localhost:4173/5d/docs/analysis/
        page.goto("http://localhost:4173/5d/docs/analysis/")

        # Wait for the sun/moon icon to appear
        page.wait_for_selector('button[aria-label*="Switch to"]')

        # Get the dark mode toggle button
        # It should initially be in light mode, so aria-label should be "Switch to dark mode"
        # Wait, the code says: aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        # Initial state is darkMode = false (from useState(false))

        toggle_btn = page.locator('button[aria-label="Switch to dark mode"]')
        expect(toggle_btn).to_be_visible()

        print("Found dark mode toggle with correct ARIA label")

        # Check mobile menu button (it's hidden on desktop, but should exist in DOM or visible if viewport is small)
        # The class has md:hidden.
        # Let's resize viewport to mobile
        page.set_viewport_size({"width": 375, "height": 667})

        menu_btn = page.locator('button[aria-label="Open main menu"]')
        expect(menu_btn).to_be_visible()
        expect(menu_btn).to_have_attribute("aria-expanded", "false")

        print("Found mobile menu toggle with correct ARIA label and expanded state")

        # Take a screenshot
        page.screenshot(path="verification/aria_check.png")

        browser.close()

if __name__ == "__main__":
    run()
