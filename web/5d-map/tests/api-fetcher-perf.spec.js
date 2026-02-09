import { describe, test, expect, vi, beforeEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: vi.fn((key) => store[key] || null),
    setItem: vi.fn((key, value) => {
      store[key] = value.toString();
    }),
    removeItem: vi.fn((key) => {
      delete store[key];
    }),
    clear: vi.fn(() => {
      store = {};
    }),
    key: vi.fn((i) => Object.keys(store)[i] || null),
    get length() {
      return Object.keys(store).length;
    }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
});

// Mock fetch
global.fetch = vi.fn();

describe('API Fetcher Performance (Granular Caching)', () => {
  beforeEach(() => {
    localStorageMock.clear();
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    localStorageMock.removeItem.mockClear();
    fetch.mockReset();
  });

  test('should use granular keys for caching instead of monolithic object', async () => {
    // Setup fetch mock to return simple data
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ([{ iso3: 'DEU', lat: 0, lng: 0 }]), // mocked array for countries/schools
      text: async () => 'code,year,val\nTEST,2020,10'
    });

    // Run the function
    await fetchAllData();

    // Verify localStorage.setItem was called with granular keys
    // The current (bad) implementation uses '5d-map-cache-v1'
    // The new (good) implementation should use keys like '5d-map-cache-v2:schools'

    const setItemCalls = localStorageMock.setItem.mock.calls.map(call => call[0]);

    // We expect multiple calls with different keys starting with the prefix
    const granularKeys = setItemCalls.filter(key => key.startsWith('5d-map-cache-v2:'));

    // Assert we are using the new prefix and granular keys
    expect(granularKeys.length).toBeGreaterThan(0);
    expect(granularKeys).toContain('5d-map-cache-v2:schools');

    // Assert we are NOT using the old monolithic key
    expect(setItemCalls).not.toContain('5d-map-cache-v1');
  });

  test('should only retrieve specific key from cache', async () => {
    // Pre-fill cache with a specific item
    const testKey = '5d-map-cache-v2:schools';
    const testData = { data: [{ name: 'Test School' }], timestamp: Date.now() };
    localStorageMock.setItem(testKey, JSON.stringify(testData));
    localStorageMock.setItem.mockClear(); // clear the set call
    localStorageMock.getItem.mockClear(); // clear the get call inside setItem

    // Run fetchAllData
    // It should hit the cache for schools
    await fetchAllData();

    // Verify getItem was called for the specific key
    expect(localStorageMock.getItem).toHaveBeenCalledWith(testKey);
  });

  test('clearCache should remove only prefixed keys', () => {
    // Setup mixed keys
    localStorageMock.setItem('5d-map-cache-v2:keep', 'value');
    localStorageMock.setItem('other-key', 'keep-me');
    localStorageMock.setItem('5d-map-cache-v2:remove-me', 'bye');

    // Call clearCache
    clearCache();

    // Verify
    // Since we don't know exact implementation of clearCache yet (it might clear all v2 keys),
    // let's assume it clears everything with the prefix.
    // Wait, clearCache() usually clears EVERYTHING related to the map.

    // Check what was removed
    const removeCalls = localStorageMock.removeItem.mock.calls.map(c => c[0]);
    expect(removeCalls).toContain('5d-map-cache-v2:keep');
    expect(removeCalls).toContain('5d-map-cache-v2:remove-me');
    expect(removeCalls).not.toContain('other-key');
  });
});
