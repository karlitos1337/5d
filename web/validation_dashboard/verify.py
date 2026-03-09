from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("pageerror", lambda msg: print(f"PAGE ERROR: {msg}"))
        page.goto("http://localhost:3000/")

        # Verify skip to main content link
        skip_link = page.locator("text=Zum Hauptinhalt springen")
        skip_link.wait_for(state="attached")
        print("Skip link found")

        # Verify dark mode toggle
        dark_toggle = page.locator("button[aria-label='Zum dunklen Modus wechseln']")
        dark_toggle.wait_for()
        print("Dark toggle found")
        dark_toggle.click()

        # Verify it changed label
        light_toggle = page.locator("button[aria-label='Zum hellen Modus wechseln']")
        light_toggle.wait_for()
        print("Light toggle found")

        # Scroll around to test scroll throttler
        page.evaluate("window.scrollTo(0, 1000)")
        page.wait_for_timeout(500)

        # Take screenshot
        page.screenshot(path="verification.png")
        print("Screenshot saved to web/validation_dashboard/verification.png")

        browser.close()

if __name__ == "__main__":
    verify()
