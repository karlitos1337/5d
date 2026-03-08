from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to local server...")
        page.goto("http://localhost:3000/")

        # Wait for the main heading
        page.wait_for_selector("h1:has-text('Validierung des 5D-Intelligence Frameworks')")

        print("Checking skip link...")
        # Check visually hidden skip link
        skip_link = page.get_by_role("link", name="Zum Hauptinhalt springen")
        skip_link.wait_for(state="attached") # It's sr-only so it might not be visually visible until focused

        print("Checking image citations...")
        # Check image citations using the data-ref attribute to locate the wrapper/image and then the super script sibling or child
        page.wait_for_selector("img[data-ref]")
        img_element = page.query_selector("img[data-ref]")

        # Because we used insertBefore for images, the sup should be a next sibling
        sup_sibling = page.evaluate("el => el.nextElementSibling && el.nextElementSibling.tagName.toLowerCase() === 'sup'", img_element)
        print(f"Citation for image exists as next sibling: {sup_sibling}")

        print("Taking screenshot of top part...")
        page.screenshot(path="web/validation_dashboard/verification.png")

        print("Scrolling down slightly to test scroll handler...")
        page.evaluate("window.scrollBy(0, 500)")
        page.wait_for_timeout(1000)

        print("Testing dark mode toggle...")
        # Click the dark mode toggle
        dark_mode_button = page.get_by_role("button", name="Zum dunklen Modus wechseln")
        dark_mode_button.click()

        print("Taking screenshot of dark mode...")
        page.screenshot(path="web/validation_dashboard/verification_dark.png")

        # Open mobile menu (simulate narrow viewport first)
        page.set_viewport_size({"width": 375, "height": 812})
        page.wait_for_timeout(500)

        print("Testing mobile menu toggle...")
        menu_button = page.get_by_role("button", name="Menü öffnen")
        menu_button.click()
        page.wait_for_timeout(500)

        menu_close_button = page.get_by_role("button", name="Menü schließen")
        menu_close_button.wait_for(state="visible")

        print("Taking screenshot of mobile menu...")
        page.screenshot(path="web/validation_dashboard/verification_mobile_menu.png")

        browser.close()
        print("Verification script finished successfully.")

if __name__ == "__main__":
    verify_frontend()