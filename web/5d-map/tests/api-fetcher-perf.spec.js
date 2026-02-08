
import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
// Assuming api-fetcher.js exports fetchWithCache or similar logic.
// However, fetchWithCache is not exported directly in the original file.
// I'll need to test via an exported function that uses it, or modify the export list.
// The file exports fetchAllData, clearCache.
// To test granular caching, I might need to test `fetchAllData` and check localStorage usage.
// Or I can temporarily export `fetchWithCache` for testing, but that modifies the source code for testing purposes.
// Alternatively, I can mock fetch and check what keys are accessed when `fetchAllData` runs.

// Let's modify api-fetcher.js slightly to export fetchWithCache for testing?
// No, I should test public API if possible. `fetchAllData` calls `fetchWithCache`.
// I can mock `fetch` to return dummy data for each endpoint and see how localStorage is used.

import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

describe('API Fetcher Caching Performance', () => {
  const CACHE_PREFIX = '5d-map-cache-v2:';

  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();

    // Mock global fetch
    global.fetch = vi.fn((url) => {
      if (url.includes('schools.json')) return Promise.resolve({ ok: true, json: () => Promise.resolve([]) });
      if (url.includes('countries.json')) return Promise.resolve({ ok: true, json: () => Promise.resolve([]) });
      if (url.includes('validation.json')) return Promise.resolve({ ok: true, json: () => Promise.resolve({ validatedISO3: [], items: [] }) });
      if (url.includes('baseline.json')) return Promise.resolve({ ok: true, json: () => Promise.resolve(null) });
      if (url.includes('depression')) return Promise.resolve({ ok: true, text: () => Promise.resolve('Code,Year,Value\nDEU,2020,5.0') });
      if (url.includes('dropout')) return Promise.resolve({ ok: true, json: () => Promise.resolve([{}, []]) });
      if (url.includes('indicator')) return Promise.resolve({ ok: true, json: () => Promise.resolve([{}, []]) }); // WGI
      if (url.includes('geojson')) return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    });
  });

  test('should use granular caching keys', async () => {
    // Spy on localStorage
    const setItemSpy = vi.spyOn(Storage.prototype, 'setItem');
    const getItemSpy = vi.spyOn(Storage.prototype, 'getItem');

    await fetchAllData();

    // Verification: Check if granular keys are used
    // The current implementation uses '5d-map-cache-v1'.
    // The optimized implementation should use keys starting with '5d-map-cache-v2:'.

    // We expect calls like setItem('5d-map-cache-v2:schools', ...)
    // instead of setItem('5d-map-cache-v1', ...)

    const calls = setItemSpy.mock.calls;
    const granularKeys = calls.filter(call => call[0].startsWith(CACHE_PREFIX));

    // This assertion will fail until the refactor is applied
    expect(granularKeys.length).toBeGreaterThan(0);

    // Also check that we are NOT storing the monolithic cache
    const monolithicCalls = calls.filter(call => call[0] === '5d-map-cache-v1');
    expect(monolithicCalls.length).toBe(0);
  });
});
