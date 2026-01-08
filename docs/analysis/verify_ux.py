from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app
        print("Navigating to app...")
        page.goto("http://localhost:5173/5d/docs/analysis/")

        # Wait for citations to be processed
        page.wait_for_selector('button[aria-label^="Quelle"]')

        print("Found citations.")

        # Check for citation button
        citation_btn = page.locator('button[aria-label^="Quelle"]').first
        print(f"Citation text: {citation_btn.text_content()}")

        # Focus on the citation button to verify focus styles
        citation_btn.focus()

        # Take screenshot of citation
        os.makedirs('/home/jules/verification', exist_ok=True)
        page.screenshot(path='/home/jules/verification/citation.png')
        print("Screenshot saved to /home/jules/verification/citation.png")

        # Check for skip link
        # It should be hidden (sr-only) until focused
        skip_link = page.locator('a[href="#einleitung"]')
        # Focus on it
        skip_link.focus()

        # Take screenshot of skip link
        page.screenshot(path='/home/jules/verification/skip_link.png')
        print("Screenshot saved to /home/jules/verification/skip_link.png")

        browser.close()

if __name__ == "__main__":
    run()
