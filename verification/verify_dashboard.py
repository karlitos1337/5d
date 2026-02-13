from playwright.sync_api import expect, sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto("http://localhost:3000")

            # Verify title
            expect(page).to_have_title("Validierung des 5D-Intelligence Frameworks")

            # Verify main heading
            # Using get_by_role is better
            heading = page.get_by_role("heading", name="Validierung des 5D-Intelligence Frameworks")
            expect(heading).to_be_visible()

            # Verify sections exist
            expect(page.get_by_role("button", name="Einleitung")).to_be_visible()
            expect(page.get_by_role("button", name="5D-Intelligence Framework")).to_be_visible()

            # Verify some content
            # The text is inside a list item
            # <li><span><strong>Autonomie</strong>: Selbstbestimmung ...</span></li>
            # We can search for text "Autonomie" inside the list

            autonomy_item = page.locator("li").filter(has_text="Autonomie")
            expect(autonomy_item).to_be_visible()

            # Take screenshot
            page.screenshot(path="verification/dashboard.png", full_page=True)
            print("Verification successful!")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()


if __name__ == "__main__":
    run()
