
import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => { store[key] = value.toString(); },
    removeItem: (key) => { delete store[key]; },
    clear: () => { store = {}; },
    _getStore: () => store
  };
})();

Object.defineProperty(global, 'localStorage', { value: localStorageMock });

// Mock Fetch
global.fetch = vi.fn();

describe('Concurrency & Race Conditions in api-fetcher', () => {
  beforeEach(() => {
    localStorageMock.clear();
    vi.clearAllMocks();

    // Default fetch behavior: return minimal valid JSON after a delay
    global.fetch.mockImplementation(async (url) => {
      // Add random delay between 10ms and 50ms to simulate network jitter
      await new Promise(r => setTimeout(r, 10 + Math.random() * 40));

      // Return minimal valid structure for each type of request
      if (url.includes('schools')) return { ok: true, json: async () => [] };
      if (url.includes('countries')) return { ok: true, json: async () => [] };
      if (url.includes('validation')) return { ok: true, json: async () => ({ validatedISO3: [], items: [] }) };
      if (url.includes('baseline')) return { ok: true, json: async () => null };
      if (url.includes('depression')) return { ok: true, text: async () => "Code,Year,Value\nDEU,2020,5.0" };
      if (url.includes('dropout')) return { ok: true, json: async () => [{}, []] }; // WB API format
      if (url.includes('indicator')) return { ok: true, json: async () => [{}, []] }; // WB API format
      if (url.includes('geojson')) return { ok: true, json: async () => ({ type: "FeatureCollection", features: [] }) };

      return { ok: true, json: async () => ({}) };
    });
  });

  test('fetchAllData should populate all cache keys correctly under concurrency', async () => {
    await fetchAllData();

    const cacheRaw = localStorageMock.getItem('5d-map-cache-v1');
    expect(cacheRaw).toBeTruthy();

    const cache = JSON.parse(cacheRaw);
    const keys = Object.keys(cache);

    // Expected keys based on fetchAllData implementation
    const expectedKeys = [
      'schools', 'countries', 'validation', 'baseline_snapshot',
      'owid_depression', 'owid_depression_series',
      'wb_dropout', 'wb_dropout_series',
      'wgi_rl_est', 'wgi_va_est', 'wgi_ge_est',
      'world_geojson'
    ];

    // Check if all expected keys are present in the cache
    // If a race condition occurs during parallel fetch, some keys will be missing
    // because one saveCache() overwrote another's addition.
    const missing = expectedKeys.filter(k => !keys.includes(k));

    expect(missing).toEqual([]);
    expect(keys.length).toBeGreaterThanOrEqual(12);
  }, 10000); // Increased timeout for slow fetches
});
