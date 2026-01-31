import { describe, test, expect, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('UX / Accessibility Tests', () => {
  beforeEach(() => {
    // Load index.html content into the document
    const htmlPath = path.resolve(__dirname, '../index.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    document.documentElement.innerHTML = html;
  });

  test('Loading overlay has correct ARIA attributes', () => {
    const overlay = document.querySelector('.loading-overlay');
    expect(overlay).not.toBeNull();
    expect(overlay.getAttribute('role')).toBe('status');
    expect(overlay.getAttribute('aria-live')).toBe('polite');

    const spinner = document.querySelector('.spinner');
    expect(spinner).not.toBeNull();
    expect(spinner.getAttribute('aria-hidden')).toBe('true');
  });
});
