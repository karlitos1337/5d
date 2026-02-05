/**
 * @vitest-environment jsdom
 */
import { describe, test, expect, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('UX Accessibility', () => {
  beforeEach(() => {
    const html = fs.readFileSync(path.resolve(__dirname, '../index.html'), 'utf8');
    document.documentElement.innerHTML = html;
  });

  test('Loading overlay has correct accessibility attributes', () => {
    const overlay = document.querySelector('.loading-overlay');
    expect(overlay).not.toBeNull();
    expect(overlay.getAttribute('role')).toBe('status');
    expect(overlay.getAttribute('aria-live')).toBe('polite');
  });

  test('Spinner is hidden from screen readers', () => {
    const spinner = document.querySelector('.spinner');
    expect(spinner).not.toBeNull();
    expect(spinner.getAttribute('aria-hidden')).toBe('true');
  });

  test('Main content exists for aria-busy toggle', () => {
    const main = document.getElementById('main-content');
    expect(main).not.toBeNull();
  });
});
