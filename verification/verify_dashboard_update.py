import time

from playwright.sync_api import sync_playwright


def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        print("Navigating to dashboard...")
        page.goto("http://localhost:5173")

        # Verify Title
        print("Verifying title...")
        page.wait_for_selector("text=Validierung des 5D-Intelligence Frameworks")

        # Verify Sections
        sections = ["Einleitung", "5D-Intelligence Framework", "Methodik", "Ergebnisse", "Validierung", "Implikationen", "Zukunftsperspektiven", "Schlussfolgerung"]
        for section in sections:
            if not page.is_visible(f"text={section}"):
                print(f"Section '{section}' not found visible on initial load (might be in menu or lower down).")
            else:
                print(f"Section '{section}' is visible.")

        # Test Navigation
        print("Clicking 'Methodik'...")
        page.click("text=Methodik")
        time.sleep(1) # Allow scroll

        # Test Dark Mode
        print("Toggling Dark Mode...")
        # The button has a Moon icon initially (since default is light), so we look for the button containing the SVG
        # The code uses Lucide icons.
        # Let's find the button that toggles dark mode. It is in the header.
        # It's the first button in the right-side group.
        # We can find it by the SVG inside or just the button structure.
        # Let's try to click the button that likely contains the Moon icon.

        # Taking initial screenshot
        page.screenshot(path="verification/dashboard_light.png")

        # Toggle
        # In the code: <button onClick={toggleDarkMode} ... > {darkMode ? <Sun /> : <Moon />} </button>
        # We can target the button by its content or hierarchy.
        # Let's target the button that is a sibling of the mobile menu button or just use the icon class if possible.
        # Easier: The button with the Moon icon.
        # Lucide icons usually render as <svg ... class="lucide lucide-moon" ...>
        page.locator(".lucide-moon").click()
        time.sleep(0.5)

        # Verify Dark Mode (background color change)
        # Main div has class: darkMode ? 'bg-gray-900 text-gray-100' : 'bg-white text-gray-900'
        # We can check the class of the first div or body.
        # The root div has the class.
        root_div = page.locator("#root > div").first
        classes = root_div.get_attribute("class")
        print(f"Classes after toggle: {classes}")
        if "bg-gray-900" in classes:
            print("Dark mode active.")
        else:
            print("Dark mode NOT active.")

        # Take Dark Mode Screenshot
        page.screenshot(path="verification/dashboard_dark.png")

        # Verify Citation
        # Look for a citation superscipt.
        # Code: const btn = document.createElement('sup'); btn.textContent = String(indexNum);
        # Let's look for a 'sup' tag.
        print("Verifying citations...")
        citation_count = page.locator("sup").count()
        print(f"Found {citation_count} citations.")

        browser.close()

if __name__ == "__main__":
    verify_dashboard()
