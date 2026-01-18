
import { describe, test, expect, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

describe('Accessibility Attributes', () => {
  let dom;
  let document;

  beforeEach(() => {
    const html = fs.readFileSync(path.resolve(__dirname, '../index.html'), 'utf8');
    dom = new JSDOM(html);
    document = dom.window.document;
  });

  test('Loading overlay has accessible role and aria attributes', () => {
    const overlay = document.querySelector('.loading-overlay');
    expect(overlay).not.toBeNull();
    expect(overlay.getAttribute('role')).toBe('status');
    expect(overlay.getAttribute('aria-live')).toBe('polite');
    expect(overlay.getAttribute('aria-busy')).toBe('true');
  });

  test('Controls container has toolbar role', () => {
    const controls = document.querySelector('.controls');
    expect(controls).not.toBeNull();
    expect(controls.getAttribute('role')).toBe('toolbar');
    expect(controls.getAttribute('aria-label')).toBe('Kartensteuerung');
  });
});
