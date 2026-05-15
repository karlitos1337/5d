from playwright.sync_api import sync_playwright
import os

os.makedirs("/home/jules/verification/videos", exist_ok=True)
os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

def run_cuj(page):
    page.goto("http://localhost:4173")
    page.wait_for_timeout(1000)

    # Click moon icon
    page.get_by_role("button", name="Dark Mode aktivieren").click()
    page.wait_for_timeout(1000)

    # Focus moon icon to see ring
    page.get_by_role("button", name="Light Mode aktivieren").focus()
    page.wait_for_timeout(1000)

    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
