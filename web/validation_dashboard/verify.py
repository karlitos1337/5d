from playwright.sync_api import sync_playwright


def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:3000")
        page.wait_for_selector("text=Validierung des 5D-Intelligence Frameworks")
        page.screenshot(path="verification.png", full_page=True)

        # Test dark mode toggle
        page.click('button[aria-label="Switch to dark mode"]')
        page.wait_for_timeout(500)
        page.screenshot(path="verification_dark.png", full_page=True)

        # Test mobile menu
        page.set_viewport_size({"width": 375, "height": 812})
        page.click('button[aria-label="Toggle menu"]')
        page.wait_for_timeout(500)
        page.screenshot(path="verification_mobile.png")

        browser.close()


if __name__ == "__main__":
    verify()
