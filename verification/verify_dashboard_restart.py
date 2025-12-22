from playwright.sync_api import sync_playwright

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the dashboard (now on 5173 presumably)
        url = "http://localhost:5173/5d/docs/analysis/"
        print(f"Navigating to {url}")
        page.goto(url)

        # Wait for content to load
        page.wait_for_selector("h1")

        # Check title
        h1_text = page.locator("h1").inner_text()
        print(f"Found H1: {h1_text}")
        if "Validierung des 5D-Intelligence Frameworks" not in h1_text:
            print("FAILED: H1 text mismatch")

        # Take screenshot of Hero
        page.screenshot(path="verification/dashboard_hero_styled.png")
        print("Screenshot saved: dashboard_hero_styled.png")

        browser.close()

if __name__ == "__main__":
    verify_dashboard()
