import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

// Mock fetch globally
const originalFetch = global.fetch;
const originalLocalStorage = global.localStorage;

describe('Parallel Fetching Performance', () => {
  let store = {};

  beforeEach(() => {
    // Clean slate
    vi.resetModules();
    store = {};

    // Mock localStorage
    global.localStorage = {
      getItem: vi.fn((key) => store[key] || null),
      setItem: vi.fn((key, value) => { store[key] = value; }),
      removeItem: vi.fn((key) => { delete store[key]; }),
      clear: vi.fn(() => { store = {}; }),
      get length() { return Object.keys(store).length; },
      key: (i) => Object.keys(store)[i]
    };

    // Mock fetch with delay
    global.fetch = vi.fn(async (url) => {
      await new Promise(resolve => setTimeout(resolve, 50)); // 50ms delay per request
      if (url.includes('schools.json')) return { ok: true, json: async () => [] };
      if (url.includes('countries.json')) return { ok: true, json: async () => [] };
      if (url.includes('validation.json')) return { ok: true, json: async () => ({ validatedISO3: [], items: [] }) };
      if (url.includes('baseline.json')) return { ok: true, json: async () => null };
      if (url.includes('depression-prevalence.csv')) return { ok: true, text: async () => 'Entity,Code,Year,Depression\nAfghanistan,AFG,2019,5.1' };
      if (url.includes('SE.PRM.DROPOUT.ZS')) return { ok: true, json: async () => [{}, []] };
      if (url.includes('countries.geojson')) return { ok: true, json: async () => ({ type: 'FeatureCollection', features: [] }) };
      // Default fallback
      return { ok: true, json: async () => ({}) };
    });
  });

  afterEach(() => {
    global.fetch = originalFetch;
    global.localStorage = originalLocalStorage;
  });

  test('fetchAllData should execute in parallel (approx max delay)', async () => {
    const start = Date.now();
    const data = await fetchAllData();
    const duration = Date.now() - start;

    console.log(`Duration: ${duration}ms`);

    expect(data).toHaveProperty('schools');
    expect(data).toHaveProperty('countries');
    expect(data).toHaveProperty('heatmapPoints');

    expect(duration).toBeLessThan(300);
  }, 10000);

  test('clearCache should remove granular keys', () => {
    // Populate cache
    store['5d-map-v1:schools'] = '{"data":[],"timestamp":123}';
    store['5d-map-v1:countries'] = '{"data":[],"timestamp":123}';
    store['other-key'] = 'keep me';
    store['5d-map-cache-v1'] = 'legacy';

    clearCache();

    // Verify
    expect(store['5d-map-v1:schools']).toBeUndefined();
    expect(store['5d-map-v1:countries']).toBeUndefined();
    expect(store['other-key']).toBeDefined();
    // Legacy key should also be removed
    expect(store['5d-map-cache-v1']).toBeUndefined();
  });
});
