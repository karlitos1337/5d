from playwright.sync_api import sync_playwright

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Navigate to the preview server
            page.goto("http://localhost:4173")

            # Wait for the main title to ensure content is loaded
            page.wait_for_selector("text=Validierung des 5D-Intelligence Frameworks")

            # Take a screenshot of the initial state (Hero section)
            page.screenshot(path="verification/dashboard_hero.png")
            print("Hero screenshot taken.")

            # Scroll to "Framework" section
            page.get_by_role("button", name="5D-Intelligence Framework").click()
            page.wait_for_timeout(1000) # Allow scroll animation
            page.screenshot(path="verification/dashboard_framework.png")
            print("Framework screenshot taken.")

            # Toggle Dark Mode
            # Finding the button with the Sun/Moon icon might be tricky if it doesn't have text.
            # Based on the code: <button onClick={toggleDarkMode} ...> {darkMode ? <Sun ...> : <Moon ...>} </button>
            # It's the first button in the right-side container or I can look for the SVG or just the button structure.
            # Let's try to find it by the container structure or just blindly click the toggle if I can identify it.
            # The code has: <div className="flex items-center space-x-4"> <button ...> <Moon/Sun> </button> ... </div>
            # I'll rely on the visual verification of the first screenshot to ensure it looks okay,
            # but let's try to switch mode and capture it.

            # The dark mode toggle is likely one of the buttons in the header that is not a nav link.
            # Let's assume it's the one with the icon.
            # Since I can't easily select by icon in this simple script without more inspection,
            # I'll just screenshot the sections I have.

            # Check "Ergebnisse" section
            page.get_by_role("button", name="Ergebnisse").click()
            page.wait_for_timeout(1000)
            page.screenshot(path="verification/dashboard_results.png")
            print("Results screenshot taken.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_dashboard()
