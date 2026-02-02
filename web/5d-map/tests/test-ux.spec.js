import { describe, test, expect, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

describe('UX / Accessibility Checks', () => {
  let document;

  beforeEach(() => {
    // Load the HTML file
    const html = fs.readFileSync(path.resolve(__dirname, '../index.html'), 'utf8');
    const dom = new JSDOM(html);
    document = dom.window.document;
  });

  test('Loading overlay has correct ARIA attributes', () => {
    const overlay = document.querySelector('.loading-overlay');
    expect(overlay).toBeTruthy();
    expect(overlay.getAttribute('role')).toBe('status');
    expect(overlay.getAttribute('aria-live')).toBe('polite');
  });

  test('Spinner is hidden from screen readers', () => {
    const spinner = document.querySelector('.spinner');
    expect(spinner).toBeTruthy();
    expect(spinner.getAttribute('aria-hidden')).toBe('true');
  });
});
