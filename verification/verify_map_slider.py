from playwright.sync_api import sync_playwright

def verify_map_slider(page):
    # Navigate to the app
    page.goto("http://localhost:5500")

    # Wait for map to load (basic check)
    page.wait_for_selector("#map")

    # Click the "Time" layer button
    page.click("#layer-time")

    # Wait for the slider to appear
    page.wait_for_selector("#year-slider")

    # Get min/max to be safe, but we saw 2018-2020
    # Set value to 2019 and trigger input event
    page.evaluate("""
        const slider = document.getElementById('year-slider');
        slider.value = 2019;
        slider.dispatchEvent(new Event('input'));
    """)

    # Wait a bit for debounce (100ms) and render
    page.wait_for_timeout(1000)

    # Take screenshot
    page.screenshot(path="verification/map_slider.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify_map_slider(page)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
