from playwright.sync_api import sync_playwright, expect
import os

def verify_app(page):
    # Ensure verification directory exists
    os.makedirs("verification", exist_ok=True)

    # Note: Using port 4173 which is the default for 'vite preview'
    page.goto("http://localhost:4173/5d/docs/analysis/")

    # Check for main title - using heading role to be specific
    expect(page.get_by_role("heading", name="Validierung des 5D-Intelligence Frameworks")).to_be_visible()

    # Check for navigation
    expect(page.get_by_role("button", name="Einleitung")).to_be_visible()
    expect(page.get_by_role("button", name="5D-Intelligence Framework")).to_be_visible()

    # Check for specific 5D content elements
    expect(page.get_by_text("Autonomie: Selbstbestimmung")).to_be_visible()

    # Check for footer or end section
    expect(page.get_by_text("Alle Angaben ohne Gewähr")).to_be_visible()

    # Scroll a bit to trigger animations
    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(1000) # Wait for animations

    # Take screenshot
    page.screenshot(path="verification/app_verification.png", full_page=True)
    print("Screenshot saved to verification/app_verification.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_app(page)
        finally:
            browser.close()
