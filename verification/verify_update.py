from playwright.sync_api import sync_playwright, expect
import os

def verify_app(page):
    # Ensure verification directory exists
    os.makedirs("verification", exist_ok=True)

    # Note: I started the server on port 3000
    page.goto("http://localhost:3000")

    # Check for main title - using heading role to be specific
    expect(page.get_by_role("heading", name="Validierung des 5D-Intelligence Frameworks")).to_be_visible()

    # Check for specific elements added in the update
    # The update includes a citation system. Let's check for a superscript.
    # The script adds 'sup' elements.
    # "Das Framework basiert auf der Selbstbestimmungstheorie" has a citation [6]

    # Wait for the citation script to run (useEffect)
    page.wait_for_timeout(2000)

    # Verify a citation button exists.
    # It's created with document.createElement('sup') and text content "6" for the first one in Framework section.
    # Based on the code:
    # <p ... data-ref="...|6">
    # creates <sup>6</sup>

    # Let's try to find a sup element with text "6"
    citation = page.locator("sup").filter(has_text="6").first
    expect(citation).to_be_visible()

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
