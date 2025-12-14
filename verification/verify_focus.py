from playwright.sync_api import sync_playwright

def verify_focus():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:5500")

        # Force remove loading overlay
        page.evaluate("""
            const overlay = document.querySelector('.loading-overlay');
            if (overlay) overlay.remove();
            document.body.classList.remove('loading');
        """)

        page.wait_for_timeout(200)

        # Focus on the first button
        page.locator("#layer-status-quo").focus()
        page.wait_for_timeout(200)

        # Verify focus style computed
        btn = page.locator("#layer-status-quo")
        outline = btn.evaluate("el => getComputedStyle(el).outline")
        print(f"Computed outline: {outline}")

        page.screenshot(path="verification/focus_state.png")

        # Verify aria-live
        layer_info = page.locator("#layer-info")
        aria_live = layer_info.get_attribute("aria-live")
        print(f"aria-live attribute: {aria_live}")

        browser.close()

if __name__ == "__main__":
    verify_focus()
