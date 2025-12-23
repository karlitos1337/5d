from playwright.sync_api import sync_playwright

def verify_citation(page):
    page.goto('http://localhost:4173/5d/docs/analysis/dist/')

    # Wait for the citation buttons to be generated
    page.wait_for_selector('sup[role="button"]')

    # Find the first citation button
    citation = page.locator('sup[role="button"]').first

    # Verify attributes
    assert citation.get_attribute('tabindex') == '0'
    assert 'Citation' in citation.get_attribute('aria-label')

    # Focus and take screenshot of the button state
    citation.focus()
    page.screenshot(path='verification/citation_focus.png')

    print("Verification successful: Attributes present and focusable")

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify_citation(page)
        finally:
            browser.close()
