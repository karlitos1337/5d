import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto("http://localhost:3000")

        # Wait for content to load
        await page.wait_for_selector("h1:has-text('Validierung des 5D-Intelligence Frameworks')")

        # Take screenshot of the whole page
        await page.screenshot(path="web/validation_dashboard/verification.png", full_page=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
