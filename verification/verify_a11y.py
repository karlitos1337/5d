from playwright.sync_api import sync_playwright

def verify_a11y():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the local dev server
        # Note: server is running on 3000 now
        page.goto("http://localhost:3000")

        # Wait for content to load
        page.wait_for_selector('text=5D-Intelligence Forschung')

        # Check for Dark Mode Toggle aria-label
        toggle_btn = page.locator('button[aria-label="Zum dunklen Modus wechseln"]')
        # Wait for it to be attached
        try:
            toggle_btn.wait_for(state="attached", timeout=5000)
            print("✅ Dark Mode toggle has correct aria-label")
        except:
             print("❌ Dark Mode toggle missing aria-label or not found")

        # Check Mobile Menu Toggle (hidden on desktop)
        menu_btn = page.locator('button[aria-label="Menü öffnen"]')

        try:
            menu_btn.wait_for(state="attached", timeout=5000)
            print("✅ Mobile Menu toggle has correct aria-label")

            # Verify aria-controls and aria-expanded
            controls = menu_btn.get_attribute("aria-controls")
            # In HTML, boolean false attribute might be missing or "false" depending on React version/implementation
            # But we passed `aria-expanded={mobileMenuOpen}` where it's boolean.
            # React renders `aria-expanded="false"` if false.
            expanded = menu_btn.get_attribute("aria-expanded")

            if controls == "mobile-menu":
                print(f"✅ aria-controls is correct: {controls}")
            else:
                print(f"❌ aria-controls mismatch: {controls}")

            print(f"ℹ️ aria-expanded is: {expanded}")

        except:
            print("❌ Mobile Menu toggle missing aria-label or not found")

        # Take a screenshot to verify visual state (should look normal)
        page.screenshot(path="verification/verification.png")

        browser.close()

if __name__ == "__main__":
    verify_a11y()
