
from playwright.sync_api import sync_playwright

def verify_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to http://localhost:4173/5d/docs/analysis/")
            page.goto("http://localhost:4173/5d/docs/analysis/")

            # Wait for the main title to ensure page is loaded
            page.wait_for_selector('text=Validierung des 5D-Intelligence Frameworks')

            # Scroll down a bit to see more content and trigger scroll effects
            page.evaluate("window.scrollBy(0, 500)")

            # Wait for animations
            page.wait_for_timeout(1000)

            # Take screenshot of the top section
            page.screenshot(path="verification/app_screenshot.png")
            print("Screenshot saved to verification/app_screenshot.png")

            # Check for the presence of specific elements from the new code
            # e.g., the citation sup elements
            page.evaluate("window.scrollBy(0, 500)")
            page.wait_for_timeout(1000)
             # Take another screenshot of the content
            page.screenshot(path="verification/app_content.png")
            print("Screenshot saved to verification/app_content.png")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_app()
