from playwright.sync_api import sync_playwright

def verify_accessibility_improvements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the preview server
        try:
            page.goto("http://localhost:4173")
            page.wait_for_load_state("networkidle")

            # 1. Verify Skip Link
            # It should be hidden by default (sr-only) but exist in the DOM
            skip_link = page.locator("a[href='#main-content']")
            if skip_link.count() > 0:
                print("✅ Skip link found in DOM")

                # Check class contains sr-only
                classes = skip_link.get_attribute("class")
                if "sr-only" in classes:
                    print("✅ Skip link has sr-only class")
                else:
                    print(f"❌ Skip link missing sr-only class: {classes}")

                # Verify it becomes visible on focus (we can simulate focus)
                skip_link.focus()
                # Taking a screenshot of the focused skip link
                page.screenshot(path="verification/skip_link_focused.png")
                print("📸 Screenshot of focused skip link saved")
            else:
                print("❌ Skip link NOT found")

            # 2. Verify ARIA Labels
            # Dark Mode Button
            # Locate by the aria-label we added
            dark_mode_btn = page.get_by_label("Zum dunklen Modus wechseln")
            if dark_mode_btn.is_visible():
                print("✅ Dark mode button found by aria-label 'Zum dunklen Modus wechseln'")
            else:
                # Try the other state label if default is dark for some reason
                dark_mode_btn_alt = page.get_by_label("Zum hellen Modus wechseln")
                if dark_mode_btn_alt.is_visible():
                    print("✅ Dark mode button found by aria-label 'Zum hellen Modus wechseln'")
                else:
                    print("❌ Dark mode button NOT found by aria-label")

            # Mobile Menu Button (hidden on desktop, need to set viewport or just check existence in DOM)
            # It's hidden with md:hidden class, but still in DOM?
            # Let's check logic: {mobileMenuOpen ? ... : ...}
            # Initial state is closed, label "Menü öffnen"
            menu_btn = page.locator("button[aria-label='Menü öffnen']")
            if menu_btn.count() > 0:
                 print("✅ Mobile menu button found by aria-label 'Menü öffnen'")
            else:
                 print("❌ Mobile menu button NOT found by aria-label")

            # 3. Verify Main ID
            main_content = page.locator("main#main-content")
            if main_content.count() > 0:
                print("✅ Main element has id='main-content'")
            else:
                print("❌ Main element missing id='main-content'")

        except Exception as e:
            print(f"❌ Error during verification: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_accessibility_improvements()
