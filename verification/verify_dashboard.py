from playwright.sync_api import sync_playwright, expect
import os

def verify_app(page):
    page.goto("http://localhost:5173/")

    # Check for the main heading from the new App.jsx
    expect(page.get_by_role("heading", name="Validierung des 5D-Intelligence Frameworks")).to_be_visible()

    # Check for a specific section button
    expect(page.get_by_role("button", name="Methodik")).to_be_visible()

    # Scroll down to trigger animations
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000) # Wait for animations

    # Take screenshot
    screenshot_path = os.path.abspath("verification/dashboard_screenshot.png")
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"Screenshot saved to {screenshot_path}")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_app(page)
        finally:
            browser.close()
