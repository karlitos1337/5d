import { test, expect } from '@playwright/test';

test.describe('Accessibility Enhancements', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5500');
    await page.waitForSelector('#map', { state: 'visible' });
    // Wait for the app to initialize and activate the first layer
    // The status quo button gets the 'btn--primary' class when activated
    await expect(page.locator('#layer-status-quo')).toHaveClass(/btn--primary/);
  });

  test('Loading overlay should have ARIA live region attributes', async ({ page }) => {
    const overlay = page.locator('.loading-overlay');
    // Check for the attributes we are about to add
    await expect(overlay).toHaveAttribute('role', 'alert');
    await expect(overlay).toHaveAttribute('aria-live', 'assertive');
    await expect(overlay).toHaveAttribute('aria-atomic', 'true');
  });

  test('Main content should have aria-busy attribute', async ({ page }) => {
    const main = page.locator('#main-content');
    // It should be present and false when loaded
    await expect(main).toHaveAttribute('aria-busy', 'false');
  });

  test('Layer buttons should have aria-pressed attributes', async ({ page }) => {
    const statusQuoBtn = page.locator('#layer-status-quo');
    const schoolsBtn = page.locator('#layer-schools');

    // Initial state: Status Quo is active
    await expect(statusQuoBtn).toHaveAttribute('aria-pressed', 'true');
    await expect(schoolsBtn).toHaveAttribute('aria-pressed', 'false');

    // Click Schools
    await schoolsBtn.click();

    // Check if attributes updated
    await expect(schoolsBtn).toHaveAttribute('aria-pressed', 'true');
    await expect(statusQuoBtn).toHaveAttribute('aria-pressed', 'false');
  });
});
