from playwright.sync_api import sync_playwright, expect

def verify_app(page):
    page.goto("http://localhost:5173/5d/docs/analysis/")

    # Check for main title - using heading role to be specific
    expect(page.get_by_role("heading", name="Validierung des 5D-Intelligence Frameworks")).to_be_visible()

    # Check for navigation
    expect(page.get_by_role("button", name="Einleitung")).to_be_visible()
    expect(page.get_by_role("button", name="5D-Intelligence Framework")).to_be_visible()

    # Check for dark mode toggle
    # It might be an SVG, so we can check for the button containing it or just the button itself
    # The code has buttons for sun/moon.

    # Scroll a bit to trigger animations
    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(1000) # Wait for animations

    # Take screenshot
    page.screenshot(path="/home/jules/verification/app_verification.png", full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_app(page)
        finally:
            browser.close()
