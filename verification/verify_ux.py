from playwright.sync_api import sync_playwright

def verify_accessibility_attributes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:4173")

        # Verify Skip Link
        skip_link = page.locator("a:text('Zum Inhalt springen')")
        print(f"Skip link count: {skip_link.count()}")

        # Focus to make it visible (it has sr-only class but focus:not-sr-only)
        skip_link.focus()
        page.screenshot(path="verification/skip_link.png")

        # Verify Dark Mode Button ARIA label
        # Default is Light Mode -> Button switches TO Dark Mode
        dark_mode_btn = page.get_by_role("button", name="Zum dunklen Modus wechseln")
        print(f"Dark mode button found: {dark_mode_btn.count() > 0}")

        # Click to toggle
        dark_mode_btn.click()

        # Now it should say "Zum hellen Modus wechseln"
        light_mode_btn = page.get_by_role("button", name="Zum hellen Modus wechseln")
        print(f"Light mode button found: {light_mode_btn.count() > 0}")

        # Verify Mobile Menu Button ARIA label (hidden on desktop usually, but let's check existence)
        # Note: Mobile menu button is md:hidden, so we might need to set viewport size
        page.set_viewport_size({"width": 375, "height": 667})

        mobile_menu_btn = page.get_by_role("button", name="Navigation öffnen")
        print(f"Mobile menu button found: {mobile_menu_btn.count() > 0}")

        mobile_menu_btn.click()

        # Verify Mobile Menu container ID
        mobile_menu = page.locator("#mobile-menu")
        print(f"Mobile menu container found: {mobile_menu.count() > 0}")

        page.screenshot(path="verification/mobile_menu.png")

        browser.close()

if __name__ == "__main__":
    verify_accessibility_attributes()
