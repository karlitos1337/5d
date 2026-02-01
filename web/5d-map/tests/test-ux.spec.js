/**
 * UX & Accessibility Tests
 */
import { describe, test, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

// Read the HTML file directly
const html = fs.readFileSync(path.resolve(__dirname, '../index.html'), 'utf8');

describe('UX / Accessibility Checks', () => {
  // Set up the DOM before tests
  document.documentElement.innerHTML = html;

  test('Loading overlay has correct ARIA attributes', () => {
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

  test('Layer buttons have aria-pressed attributes', () => {
    const statusQuoBtn = document.getElementById('layer-status-quo');
    const schoolsBtn = document.getElementById('layer-schools');

    expect(statusQuoBtn.getAttribute('aria-pressed')).toBe('true');
    expect(schoolsBtn.getAttribute('aria-pressed')).toBe('false');
  });
});
