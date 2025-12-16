from playwright.sync_api import sync_playwright
import time

def verify_skip_link():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the HTML file directly
        import os
        cwd = os.getcwd()
        file_path = f"file://{cwd}/web/5d-map/index.html"
        page.goto(file_path)

        # Press Tab to focus the skip link
        page.keyboard.press("Tab")

        # Wait for transition
        time.sleep(0.5)

        # Check if the skip link is focused and visible
        skip_link = page.locator(".skip-link")

        # Take a screenshot
        page.screenshot(path="verification/skip_link_focused.png")

        # Check if it has the correct text
        text = skip_link.text_content()
        print(f"Skip link text: {text}")

        # Click the link (by pressing Enter since it's focused)
        page.keyboard.press("Enter")

        # Check if focus moved to main content
        focused_element_id = page.evaluate("document.activeElement.id")
        print(f"Focused element ID: {focused_element_id}")

        browser.close()

if __name__ == "__main__":
    verify_skip_link()
