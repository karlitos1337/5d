from playwright.sync_api import sync_playwright

def verify_ux(page):
    page.goto("http://localhost:4173")

    # 1. Verify "Skip to content" link
    skip_link = page.get_by_text("Zum Hauptinhalt springen")
    if not skip_link.is_visible():
        print("Skip link not initially visible (correct)")

    # Focus to make it visible
    skip_link.focus()
    page.screenshot(path="verification/skip_link_focused.png")
    if skip_link.is_visible():
        print("Skip link visible on focus (correct)")

    # Verify target of skip link
    href = skip_link.get_attribute("href")
    print(f"Skip link href: {href}")
    assert href == "#main-content"

    # 2. Verify Dark Mode Toggle ARIA
    dark_mode_btn = page.get_by_role("button", name="In den dunklen Modus wechseln")
    if dark_mode_btn.count() > 0:
        print("Dark mode button has correct ARIA label")

    # Toggle to check dynamic label
    dark_mode_btn.click()
    page.wait_for_timeout(500) # Wait for state change

    light_mode_btn = page.get_by_role("button", name="In den hellen Modus wechseln")
    if light_mode_btn.count() > 0:
        print("Light mode button has correct ARIA label after toggle")

    # 3. Verify Citation Buttons (Wait for hydration/useEffect)
    page.wait_for_selector('sup[role="button"]')
    citation_btn = page.locator('sup[role="button"]').first

    aria_label = citation_btn.get_attribute("aria-label")
    title = citation_btn.get_attribute("title")

    print(f"Citation ARIA: {aria_label}")
    print(f"Citation Title: {title}")

    assert "Quelle" in aria_label
    assert "Quelle:" in title

    # Take final screenshot
    page.screenshot(path="verification/ux_verification.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify_ux(page)
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/failure.png")
        finally:
            browser.close()
