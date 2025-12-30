
from playwright.sync_api import sync_playwright
import os

def verify_map_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Absolute path to index.html
            cwd = os.getcwd()
            file_url = 'file://' + cwd + '/web/5d-map/index.html'
            print(f'Navigating to {file_url}')
            page.goto(file_url)

            # Wait for #map div
            page.wait_for_selector('#map')

            # Take screenshot of initial state
            page.screenshot(path='verification/map_initial.png')

            # Check for console errors
            page.on('console', lambda msg: print(f'Console: {msg.text}'))

            # Wait for any potential async loads (even if they fail due to CORS with file://)
            page.wait_for_timeout(2000)

            page.screenshot(path='verification/map_loaded.png')
            print('Screenshot taken at verification/map_loaded.png')
        except Exception as e:
            print(f'Error: {e}')
        finally:
            browser.close()

if __name__ == '__main__':
    verify_map_loads()
