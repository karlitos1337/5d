import { test, expect } from '@playwright/test';

test.describe('5D Map UX & Accessibility', () => {
  test.beforeEach(async ({ page, browserName }) => {
    // Firefox has specific environment issues (hanging fetch) in this sandbox
    if (browserName === 'firefox') test.skip();

    // Abort service worker to prevent reloads during test
    await page.route('**/sw.js', route => route.abort());

    // Requires server to be running on 5500
    await page.goto('http://localhost:5500');

    // Wait for loading to finish by checking the update time text
    // The text changes from "Lädt…" to a date when init() completes
    await expect(page.locator('#last-update')).not.toContainText('Lädt…');
  });

  test('Loading overlay should have role="alert"', async ({ page }) => {
    const overlay = page.locator('.loading-overlay');
    await expect(overlay).toHaveAttribute('role', 'alert');
    await expect(overlay).toHaveAttribute('aria-live', 'assertive');
  });

  test('Layer buttons should have aria-pressed attributes', async ({ page }) => {
    // Default state: Status Quo is active
    const statusQuo = page.locator('#layer-status-quo');
    const schools = page.locator('#layer-schools');
    const imp = page.locator('#layer-imp');
    const validation = page.locator('#layer-validation');
    const sources = page.locator('#layer-sources');
    const time = page.locator('#layer-time');

    await expect(statusQuo).toHaveAttribute('aria-pressed', 'true');
    await expect(schools).toHaveAttribute('aria-pressed', 'false');
    await expect(imp).toHaveAttribute('aria-pressed', 'false');
    await expect(validation).toHaveAttribute('aria-pressed', 'false');
    await expect(sources).toHaveAttribute('aria-pressed', 'false');
    await expect(time).toHaveAttribute('aria-pressed', 'false');

    // Click Schools
    // Small delay to ensure event listeners are fully attached in all browsers (e.g. Firefox)
    await page.waitForTimeout(500);
    await schools.click();
    await expect(statusQuo).toHaveAttribute('aria-pressed', 'false');
    await expect(schools).toHaveAttribute('aria-pressed', 'true');

    // Click IMP
    await imp.click();
    await expect(schools).toHaveAttribute('aria-pressed', 'false');
    await expect(imp).toHaveAttribute('aria-pressed', 'true');

    // Click Validation
    await validation.click();
    await expect(imp).toHaveAttribute('aria-pressed', 'false');
    await expect(validation).toHaveAttribute('aria-pressed', 'true');

    // Click Sources
    await sources.click();
    await expect(validation).toHaveAttribute('aria-pressed', 'false');
    await expect(sources).toHaveAttribute('aria-pressed', 'true');

    // Click Time
    await time.click();
    await expect(sources).toHaveAttribute('aria-pressed', 'false');
    await expect(time).toHaveAttribute('aria-pressed', 'true');
  });
});
