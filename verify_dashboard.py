from playwright.sync_api import sync_playwright

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("http://localhost:5173")

            # Wait for content to load
            page.wait_for_selector("h1:has-text('Validierung des 5D-Intelligence Frameworks')", timeout=10000)

            # Take a screenshot of the top section
            page.screenshot(path="verification_dashboard.png")
            print("Screenshot taken: verification_dashboard.png")

            # Scroll to results section and take another screenshot
            page.get_by_role("button", name="Ergebnisse").click()
            page.wait_for_timeout(1000) # Wait for scroll
            page.screenshot(path="verification_dashboard_results.png")
            print("Screenshot taken: verification_dashboard_results.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_dashboard()
