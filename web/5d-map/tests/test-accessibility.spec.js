import { describe, test, expect, beforeAll } from 'vitest';
import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

describe('Accessibility Checks', () => {
  let dom;
  let document;

  beforeAll(() => {
    const html = fs.readFileSync(path.resolve(__dirname, '../index.html'), 'utf8');
    dom = new JSDOM(html);
    document = dom.window.document;
  });

  test('Loading overlay should have accessible role and live region', () => {
    const overlay = document.querySelector('.loading-overlay');
    expect(overlay).toBeTruthy();
    expect(overlay.getAttribute('role')).toBe('status');
    expect(overlay.getAttribute('aria-live')).toBe('polite');
  });

  test('Loading spinner should be hidden from screen readers', () => {
    const spinner = document.querySelector('.spinner');
    expect(spinner).toBeTruthy();
    expect(spinner.getAttribute('aria-hidden')).toBe('true');
  });
});
