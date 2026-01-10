from playwright.sync_api import sync_playwright

def verify_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Adjust port if necessary, standard Vite port is 5173
            page.goto("http://localhost:5173/5d/docs/analysis/")

            # Wait for content to load
            page.wait_for_selector("text=Validierung des 5D-Intelligence Frameworks")

            # Verify sections exist
            sections = [
                "Einleitung",
                "5D-Intelligence Framework",
                "Methodik",
                "Ergebnisse",
                "Validierung",
                "Implikationen",
                "Zukunftsperspektiven",
                "Schlussfolgerung"
            ]

            for section in sections:
                if not page.get_by_text(section).first.is_visible():
                    print(f"Warning: Section {section} not found or not visible")

            # Take screenshot of the top section
            page.screenshot(path="verification_top.png")
            print("Screenshot taken: verification_top.png")

            # Scroll down to a middle section (e.g. Methodik) and take another screenshot
            method_link = page.get_by_text("Methodik").first
            if method_link.is_visible():
                method_link.click()
                page.wait_for_timeout(1000) # Wait for smooth scroll
                page.screenshot(path="verification_methodology.png")
                print("Screenshot taken: verification_methodology.png")

            # Verify dark mode toggle
            # Assuming the sun/moon icon is a button. The code uses lucide-react icons inside a button.
            # Let's try to find the button by its functionality or structure if aria-label is missing.
            # The button toggles dark mode.
            # We can look for the button that contains the Moon or Sun icon.
            # Since we can't easily select by icon content in playwright without aria labels,
            # we might need to rely on the fact it's one of the buttons in the header.
            # Let's just screenshot the light mode for now as the request was just to integrate the code.

        except Exception as e:
            print(f"Error during verification: {e}")
            page.screenshot(path="verification_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_app()