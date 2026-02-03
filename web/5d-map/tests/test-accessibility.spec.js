import { describe, test, expect, beforeAll } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

describe('Accessibility Checks', () => {
  let dom;
  let document;

  beforeAll(() => {
    // Read index.html from the parent directory
    const htmlPath = path.resolve(__dirname, '../index.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    dom = new JSDOM(html);
    document = dom.window.document;
  });

  test('Loading overlay has correct ARIA attributes', () => {
    const overlay = document.querySelector('.loading-overlay');
    expect(overlay).not.toBeNull();
    // It should have role="status" and aria-live="polite"
    // to announce loading state without interrupting aggressively
    expect(overlay.getAttribute('role')).toBe('status');
    expect(overlay.getAttribute('aria-live')).toBe('polite');
  });

  test('Spinner is hidden from screen readers', () => {
    const spinner = document.querySelector('.spinner');
    expect(spinner).not.toBeNull();
    // The visual spinner should be hidden from screen readers
    expect(spinner.getAttribute('aria-hidden')).toBe('true');
  });
});
