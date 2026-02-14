import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

describe('Parallel Fetch and Granular Cache', () => {
  let mockStorage = {};

  beforeEach(() => {
    mockStorage = {};

    // Mock localStorage
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => mockStorage[key] || null);
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation((key, val) => { mockStorage[key] = val; });
    vi.spyOn(Storage.prototype, 'removeItem').mockImplementation((key) => { delete mockStorage[key]; });
    vi.spyOn(Storage.prototype, 'clear').mockImplementation(() => { mockStorage = {}; });

    // Mock iteration
    Object.defineProperty(Storage.prototype, 'length', {
      get: () => Object.keys(mockStorage).length,
      configurable: true
    });
    vi.spyOn(Storage.prototype, 'key').mockImplementation((i) => Object.keys(mockStorage)[i]);

    // Mock fetch
    global.fetch = vi.fn((url) => {
      // Return promises that resolve after a short delay to simulate async
      return new Promise(resolve => {
        setTimeout(() => {
          if (url.endsWith('.csv')) {
            resolve({
              ok: true,
              text: async () => "Code,Year,Value\nDEU,2020,10.5"
            });
          } else if (url.includes('worldbank')) {
            resolve({
              ok: true,
              json: async () => [{}, [{ countryiso3code: 'DEU', date: '2020', value: 10 }]]
            });
          } else {
            resolve({
              ok: true,
              json: async () => ([{ iso3: 'DEU', lat: 0, lng: 0 }])
            });
          }
        }, 10);
      });
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should use granular cache keys', async () => {
    await fetchAllData();

    const keys = Object.keys(mockStorage);
    // Log keys for debugging if test fails
    // console.log('Storage keys:', keys);

    const hasGranularKeys = keys.some(k => k.startsWith('5d-map-v1:'));
    expect(hasGranularKeys, 'Should use granular keys starting with 5d-map-v1:').toBe(true);

    // Expect multiple keys, not just one monolithic key
    expect(keys.length).toBeGreaterThan(1);
    expect(mockStorage['5d-map-v1:schools']).toBeDefined();
  });

  it('should clear only relevant cache keys', async () => {
    mockStorage['5d-map-v1:test'] = 'delete me';
    mockStorage['other-app-key'] = 'keep me';

    clearCache();

    expect(mockStorage['5d-map-v1:test']).toBeUndefined();
    expect(mockStorage['other-app-key']).toBe('keep me');
  });

  it('should return complete result object', async () => {
    const result = await fetchAllData();
    expect(result.schools).toBeDefined();
    expect(result.countries).toBeDefined();
    expect(result.heatmapPoints).toBeDefined();
  });
});
