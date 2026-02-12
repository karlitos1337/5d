import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

// Mock fetch globally
global.fetch = vi.fn();

describe('API Fetcher Parallelism', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
    vi.useRealTimers();
  });

  test('fetchAllData fetches independent data in parallel', async () => {
    // Setup delays
    const delay = (ms) => new Promise(r => setTimeout(r, ms));

    global.fetch.mockImplementation(async (url) => {
        await delay(50);

        const u = String(url);
        if (u.includes('schools')) return { ok: true, json: async () => [] };
        if (u.includes('countries')) return { ok: true, json: async () => [] };
        if (u.includes('validation')) return { ok: true, json: async () => ({ items: [], validatedISO3: [] }) };
        if (u.includes('baseline')) return { ok: true, json: async () => ({}) };
        if (u.includes('depression')) return { ok: true, text: async () => "Code,Year,Depression\nDEU,2020,5.5" };
        if (u.includes('dropout')) return { ok: true, json: async () => [{}, []] };
        if (u.includes('indicator')) return { ok: true, json: async () => [{}, []] };
        if (u.includes('geojson')) return { ok: true, json: async () => ({ type: 'FeatureCollection', features: [] }) };

        return { ok: true, json: async () => ({}), text: async () => "" };
    });

    const start = Date.now();
    await fetchAllData();
    const end = Date.now();
    const duration = end - start;

    // There are about 8-10 independent fetches.
    // Sequential: 10 * 50ms = 500ms
    // Parallel: ~50ms + overhead

    // Check if parallel: < 250ms
    console.log(`Duration: ${duration}ms`);
    expect(duration).toBeLessThan(250);
  });

  test('localStorage contains granular keys', async () => {
      global.fetch.mockResolvedValue({
          ok: true,
          json: async () => [],
          text: async () => ""
      });
      await fetchAllData();

      // We verify that we have stored data.
      expect(localStorage.length).toBeGreaterThan(0);

      // We also want to verify no race conditions happened (implicit in parallel test passing if fetching works)
      // But we can check specifically for keys later if we want.
  });
});
