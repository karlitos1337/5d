/**
 * E2E Tests mit Playwright
 * Run: npx playwright test
 */

import { test, expect } from '@playwright/test';

test.describe('5D Map E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5500');
    // Warte bis Map geladen ist
    await page.waitForSelector('#map', { state: 'visible' });
  });

  test('should load map correctly', async ({ page }) => {
    await expect(page.locator('#map')).toBeVisible();
    await expect(page.locator('.app-header h1')).toContainText('5D‑Intelligenz Global');
  });

  test('should have all 4 layer buttons', async ({ page }) => {
    await expect(page.locator('#layer-status-quo')).toBeVisible();
    await expect(page.locator('#layer-schools')).toBeVisible();
    await expect(page.locator('#layer-imp')).toBeVisible();
    await expect(page.locator('#layer-time')).toBeVisible();
  });

  test('should toggle between layers', async ({ page }) => {
    // Start mit Status Quo
    await expect(page.locator('#layer-status-quo')).toHaveClass(/btn--primary/);
    
    // Klick auf Schulen
    await page.click('#layer-schools');
    await expect(page.locator('#layer-schools')).toHaveClass(/btn--primary/);
    await expect(page.locator('#layer-status-quo')).not.toHaveClass(/btn--primary/);
    
    // Klick auf IMP
    await page.click('#layer-imp');
    await expect(page.locator('#layer-imp')).toHaveClass(/btn--primary/);
    await expect(page.locator('.legend')).toBeVisible();
    
    // Klick auf Zeitreise
    await page.click('#layer-time');
    await expect(page.locator('#layer-time')).toHaveClass(/btn--primary/);
    await expect(page.locator('#time-controls')).toBeVisible();
  });

  test('should display time slider when Zeitreise is active', async ({ page }) => {
    await page.click('#layer-time');
    await expect(page.locator('#time-controls')).toBeVisible();
    await expect(page.locator('#year-slider')).toBeVisible();
    await expect(page.locator('#year-label')).toBeVisible();
  });

  test('should update year label when slider changes', async ({ page }) => {
    await page.click('#layer-time');
    const slider = page.locator('#year-slider');
    const label = page.locator('#year-label');
    
    await slider.evaluate((el) => { el.value = "2020"; el.dispatchEvent(new Event('input')) });
    await expect(label).toContainText('2020');
    
    await slider.evaluate((el) => { el.value = "2015"; el.dispatchEvent(new Event('input')) });
    await expect(label).toContainText('2015');
  });

  test('should show loading overlay during initial load', async ({ page }) => {
    // Reload page
    await page.goto('http://localhost:5500', { waitUntil: 'commit' });
    
    // Loading overlay sollte kurz sichtbar sein
    const loadingOverlay = page.locator('.loading-overlay');
    // Wir können nicht garantieren dass wir es sehen (zu schnell),
    // aber wenn body.loading existiert, sollte overlay display:flex haben
    const bodyClass = await page.locator('body').getAttribute('class');
    if (bodyClass?.includes('loading')) {
      await expect(loadingOverlay).toBeVisible();
    }
  });

  test('should display last update timestamp', async ({ page }) => {
    const updateTime = page.locator('#last-update');
    await expect(updateTime).not.toContainText('Lädt…');
    // Sollte ein Datum/Zeit enthalten
    await expect(updateTime).not.toBeEmpty();
  });

  test('should have working footer links', async ({ page }) => {
    await expect(page.locator('a[href="#sources"]')).toBeVisible();
    await expect(page.locator('a[href="#about"]')).toBeVisible();
    await expect(page.locator('a[href*="github.com"]')).toBeVisible();
  });

  test('should render map tiles', async ({ page }) => {
    // Warte auf Leaflet Tiles
    await page.waitForSelector('.leaflet-tile-loaded', { timeout: 10000 });
    const tiles = await page.locator('.leaflet-tile-loaded').count();
    expect(tiles).toBeGreaterThan(0);
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    
    await expect(page.locator('.app-header')).toBeVisible();
    await expect(page.locator('.controls')).toBeVisible();
    await expect(page.locator('#map')).toBeVisible();
    
    // Controls sollten Grid-Layout haben auf Mobile
    const controlsStyles = await page.locator('.controls').evaluate(el => {
      return window.getComputedStyle(el).display;
    });
    expect(controlsStyles).toBe('grid');
  });

  test('school markers should open popup on click', async ({ page }) => {
    await page.click('#layer-schools');
    await page.waitForTimeout(500); // Warte auf Layer-Render
    
    // Wenn Marker existieren
    const markers = page.locator('.school-marker');
    const markerCount = await markers.count();
    
    if (markerCount > 0) {
      await markers.first().click();
      await expect(page.locator('.leaflet-popup')).toBeVisible();
      await expect(page.locator('.school-popup')).toBeVisible();
    }
  });

  test('IMP layer should show legend', async ({ page }) => {
    await page.click('#layer-imp');
    await page.waitForTimeout(500);
    
    await expect(page.locator('.legend')).toBeVisible();
    // Legende sollte Farb-Indikatoren haben
    const legendItems = await page.locator('.legend i').count();
    expect(legendItems).toBeGreaterThan(0);
  });

  test('tooltips should be present on buttons', async ({ page }) => {
    const statusQuoBtn = page.locator('#layer-status-quo');
    const title = await statusQuoBtn.getAttribute('title');
    expect(title).toBeTruthy();
    expect(title).toContain('Depression');
  });
});

test.describe('Performance Tests', () => {
  test('should load within 3 seconds', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('http://localhost:5500');
    await page.waitForSelector('#map', { state: 'visible' });
    const loadTime = Date.now() - startTime;
    
    expect(loadTime).toBeLessThan(3000);
  });

  test('should not have console errors', async ({ page }) => {
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    await page.goto('http://localhost:5500', { waitUntil: 'commit' });
    await page.waitForTimeout(2000);
    
    // Erlaubte Warnings (z.B. CORS, fehlende Favicons)
    const allowedErrors = [
      'favicon.ico',
      'Failed to fetch',
      'CORS',
      'Content Security Policy',
      'violates the following directive'
    ];
    
    const criticalErrors = errors.filter(err => 
      !allowedErrors.some(allowed => err.includes(allowed))
    );
    
    expect(criticalErrors).toHaveLength(0);
  });
});
