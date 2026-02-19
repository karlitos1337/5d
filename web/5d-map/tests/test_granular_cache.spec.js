import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

describe('Granular Caching Strategy', () => {
  let store = {};

  beforeEach(() => {
    store = {};

    // Mock localStorage
    const localStorageMock = {
      getItem: vi.fn((key) => store[key] || null),
      setItem: vi.fn((key, value) => { store[key] = value; }),
      removeItem: vi.fn((key) => { delete store[key]; }),
      clear: vi.fn(() => { store = {}; }),
      key: vi.fn((i) => Object.keys(store)[i]),
      get length() { return Object.keys(store).length; }
    };
    vi.stubGlobal('localStorage', localStorageMock);

    // Mock fetch
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve([]), // Default empty array for JSON
      text: () => Promise.resolve('Code,Year,Value\nTEST,2023,100') // Default CSV
    })));
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  test('fetchAllData stores data in granular keys', async () => {
    // Run the function
    await fetchAllData();

    // Check what was stored
    const keys = Object.keys(store);
    const granularKeys = keys.filter(k => k.startsWith('5d-map-v1:'));

    // We expect granular keys to be present
    expect(granularKeys).toContain('5d-map-v1:schools');
    expect(granularKeys).toContain('5d-map-v1:countries');
    expect(granularKeys).toContain('5d-map-v1:validation');

    // Ensure the old monolithic key is NOT created
    expect(keys).not.toContain('5d-map-cache-v1');
  });

  test('clearCache removes granular keys and legacy key', () => {
    // Setup initial state
    store['5d-map-v1:schools'] = JSON.stringify({ data: [], timestamp: Date.now() });
    store['5d-map-v1:countries'] = JSON.stringify({ data: [], timestamp: Date.now() });
    store['5d-map-cache-v1'] = JSON.stringify({ schools: [] }); // Legacy key
    store['other-app-key'] = 'keep-me';

    clearCache();

    // Verify cleanup
    expect(store['5d-map-v1:schools']).toBeUndefined();
    expect(store['5d-map-v1:countries']).toBeUndefined();
    expect(store['5d-map-cache-v1']).toBeUndefined();

    // Verify other keys are preserved
    expect(store['other-app-key']).toBeDefined();
  });
});
