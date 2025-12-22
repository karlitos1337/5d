from playwright.sync_api import sync_playwright

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the dashboard
        # Using the URL from the vite output: http://localhost:5174/5d/docs/analysis/
        # But locally it might be serving relative to root, let's try just localhost:5174 if base is set
        url = "http://localhost:5174/5d/docs/analysis/"
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
        page.screenshot(path="verification/dashboard_hero.png")
        print("Screenshot saved: dashboard_hero.png")

        # Click Methodik
        page.click("text=Methodik")
        page.wait_for_timeout(500) # wait for smooth scroll
        page.screenshot(path="verification/dashboard_methodik.png")
        print("Screenshot saved: dashboard_methodik.png")

        # Toggle Dark Mode
        # Assuming the Sun/Moon icon is in a button
        # The code has buttons with Sun/Moon icons.
        # <button onClick={toggleDarkMode} ...> {darkMode ? <Sun.../> : <Moon.../>} </button>
        # We can look for the button containing the SVG or just the first button in that container.
        # Let's try finding the button that toggles dark mode. It is in the header.
        buttons = page.locator("header button").all()
        # The dark mode toggle is likely one of the last buttons or we can identify by icon.
        # But simple way: click the button that is NOT a nav link.
        # Nav links have text. Dark mode toggle has SVG.

        # Let's try to find the button with the Moon icon (since default is light mode)
        # However, Lucide icons might not have accessible text by default.
        # The button has className p-2 rounded-lg...

        # We can also rely on the fact it's in the header and has no text content (just icon).
        for btn in buttons:
             if not btn.inner_text():
                 btn.click()
                 break

        page.wait_for_timeout(500)
        page.screenshot(path="verification/dashboard_dark.png")
        print("Screenshot saved: dashboard_dark.png")

        browser.close()

if __name__ == "__main__":
    verify_dashboard()
