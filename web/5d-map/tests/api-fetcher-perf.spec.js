import { describe, test, expect, vi, beforeEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

describe('Performance Optimization: Granular Caching', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  test('uses granular cache keys instead of monolithic cache', async () => {
    // Mock fetch to return valid structures so fetchAllData completes
    global.fetch = vi.fn().mockImplementation((url) => {
      const urlStr = String(url);
      return Promise.resolve({
        ok: true,
        json: async () => {
          if (urlStr.includes('countries.json')) return [{ iso3: 'DEU', lat: 50, lng: 10 }];
          if (urlStr.includes('schools.json')) return [];
          if (urlStr.includes('validation.json')) return { validatedISO3: [], items: [] };
          if (urlStr.includes('baseline.json')) return { depression_latest: {}, dropout_latest: {} };
          if (urlStr.includes('worldbank.org')) return [{}, []]; // [meta, data]
          if (urlStr.includes('geojson')) return { type: 'FeatureCollection', features: [] };
          return {};
        },
        text: async () => "Code,Year,Value\nDEU,2020,5.5"
      });
    });

    // Spy on localStorage.setItem
    const setItemSpy = vi.spyOn(Storage.prototype, 'setItem');

    await fetchAllData();

    // Check that we are NOT using the old monolithic key
    // This assertion will FAIL if the code is not yet updated, which is what we want (Red phase)
    // Or rather, checking that we ARE using granular keys will fail.

    const keys = setItemSpy.mock.calls.map(call => call[0]);
    const granularKeys = keys.filter(k => k.startsWith('5d-map-cache-v2:'));

    // We expect multiple granular keys
    expect(granularKeys.length).toBeGreaterThan(0);
    expect(granularKeys).toContain('5d-map-cache-v2:schools');

    // Ensure we are NOT writing the old key (optional, but good for verification)
    expect(keys).not.toContain('5d-map-cache-v1');
  });

  test('clearCache removes only granular keys', () => {
      // Setup mock data
      localStorage.setItem('5d-map-cache-v2:test1', 'foo');
      localStorage.setItem('5d-map-cache-v2:test2', 'bar');
      localStorage.setItem('other-app-key', 'baz');

      // We need to mock removeItem because clearCache calls it
      const removeItemSpy = vi.spyOn(Storage.prototype, 'removeItem');

      clearCache();

      // Check logic
      // Since clearCache implementation might vary (iterate vs direct),
      // we check final state of localStorage if possible, or spy calls.
      // But in JSDOM, localStorage is functional.

      expect(localStorage.getItem('5d-map-cache-v2:test1')).toBeNull();
      expect(localStorage.getItem('5d-map-cache-v2:test2')).toBeNull();
      expect(localStorage.getItem('other-app-key')).toBe('baz');
  });
});
