
from playwright.sync_api import sync_playwright

def verify_skip_link():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the file directly since it is static
        page.goto('file:///app/web/5d-map/index.html')

        # Verify Skip Link exists
        skip_link = page.locator('.skip-link')
        print(f'Skip link text: {skip_link.inner_text()}')

        # Verify it is initially hidden (top: -100px)
        # Note: We check the computed style
        box = skip_link.bounding_box()
        print(f'Skip link y-position: {box["y"]}')

        # Verify Main content ID
        main = page.locator('#main-content')
        print(f'Main ID found: {main.count() > 0}')

        # Focus on the skip link and take screenshot
        skip_link.focus()
        page.screenshot(path='verification/skip_link_focused.png')

        browser.close()

if __name__ == '__main__':
    verify_skip_link()
