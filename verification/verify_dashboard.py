from playwright.sync_api import Page, expect, sync_playwright

def test_dashboard_content(page: Page):
    # Navigate to the dashboard
    # The output says http://localhost:5173/5d/docs/analysis/
    # But usually vite root is / or base path
    # Let's try to access the URL provided in log
    page.goto("http://localhost:5173/5d/docs/analysis/")

    # Wait for the title to be visible
    # The user code has "5D-Intelligence Forschung" in the header
    header = page.get_by_text("5D-Intelligence Forschung")
    expect(header).to_be_visible()

    # Check for "Validierung des 5D-Intelligence Frameworks" which is in the Hero section
    hero_title = page.get_by_role("heading", name="Validierung des 5D-Intelligence Frameworks")
    expect(hero_title).to_be_visible()

    # Scroll down to ensure content loads (if lazy loaded or just for screenshot)
    page.evaluate("window.scrollTo(0, 500)")

    # Check for sections
    # { id: 'einleitung', label: 'Einleitung' }
    # { id: 'framework', label: '5D-Intelligence Framework' }

    # Check desktop nav
    nav_link = page.get_by_role("button", name="Einleitung").first
    expect(nav_link).to_be_visible()

    nav_link_fw = page.get_by_role("button", name="5D-Intelligence Framework").first
    expect(nav_link_fw).to_be_visible()

    # Take screenshot
    page.screenshot(path="verification/dashboard.png", full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_dashboard_content(page)
            print("Verification script finished successfully.")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()
