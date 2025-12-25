from playwright.sync_api import Page, expect, sync_playwright
import time

def verify_5d_intelligence_dashboard(page: Page):
    """
    Verifies that the 5D-Intelligence Dashboard loads and displays key sections.
    """
    # 1. Arrange: Go to the dashboard.
    page.goto("http://localhost:5173/5d/docs/analysis/")

    # 2. Act: Wait for the main heading to be visible.
    # The heading "Validierung des 5D-Intelligence Frameworks" should be present.
    heading = page.get_by_role("heading", name="Validierung des 5D-Intelligence Frameworks")
    expect(heading).to_be_visible()

    # 3. Check for specific sections
    # Check "Das 5D-Intelligence Framework" section
    framework_heading = page.get_by_role("heading", name="Das 5D-Intelligence Framework")
    expect(framework_heading).to_be_visible()

    # Check that dimensions are listed
    autonomy = page.get_by_text("Autonomie: Selbstbestimmung")
    expect(autonomy).to_be_visible()

    # 4. Check citations
    # Citations are dynamically added with superscript numbers.
    # We can check if a sup element exists.
    # Using a CSS selector for 'sup'
    citations = page.locator("sup")
    expect(citations.first).to_be_visible()

    # 5. Screenshot: Capture the dashboard.
    page.screenshot(path="/home/jules/verification/dashboard.png", full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_5d_intelligence_dashboard(page)
            print("Verification successful!")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="/home/jules/verification/failure.png")
            raise e
        finally:
            browser.close()
