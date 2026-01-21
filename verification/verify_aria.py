from playwright.sync_api import sync_playwright

def verify_aria_labels():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Ensure we connect to the preview server
        page.goto("http://localhost:4173")

        # Verify Desktop Navigation
        nav = page.get_by_role("navigation", name="Hauptnavigation")
        if nav.count() > 0:
            print("✅ Main navigation has correct aria-label")
        else:
            print("❌ Main navigation missing aria-label")

        # Verify Nav Buttons
        einleitung_btn = page.get_by_role("button", name="Springe zu Abschnitt: Einleitung")
        if einleitung_btn.count() > 0:
            print("✅ Nav button 'Einleitung' has correct aria-label")
        else:
             print("❌ Nav button 'Einleitung' missing aria-label")

        # Verify Dark Mode Toggle
        # We check for the initial state label (assuming default is light mode -> "Zum dunklen Modus wechseln")
        dark_mode_btn = page.get_by_label("Zum dunklen Modus wechseln")
        if dark_mode_btn.count() > 0:
             print("✅ Dark mode toggle has correct aria-label")
        else:
             # Check if it's in dark mode already
             dark_mode_btn_alt = page.get_by_label("Zum hellen Modus wechseln")
             if dark_mode_btn_alt.count() > 0:
                 print("✅ Dark mode toggle has correct aria-label (Dark Mode Active)")
             else:
                 print("❌ Dark mode toggle missing aria-label")

        # Verify Mobile Menu Toggle (hidden on desktop, but should exist in DOM)
        # We need to set viewport to mobile to interact with it, or just check existence in DOM
        menu_btn = page.get_by_label("Menü öffnen")
        if menu_btn.count() > 0:
             print("✅ Mobile menu toggle has correct aria-label")
        else:
             print("❌ Mobile menu toggle missing aria-label")

        # Take a screenshot to confirm visual state hasn't regressed
        page.screenshot(path="verification/aria_verification.png")
        print("📸 Screenshot saved to verification/aria_verification.png")

        browser.close()

if __name__ == "__main__":
    verify_aria_labels()
