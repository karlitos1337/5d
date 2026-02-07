import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
// We are testing fetchWithCache, which we will export in the implementation step.
import { fetchWithCache, clearCache } from '../modules/api-fetcher.js';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: vi.fn((key) => store[key] || null),
    setItem: vi.fn((key, value) => { store[key] = value.toString(); }),
    removeItem: vi.fn((key) => { delete store[key]; }),
    clear: vi.fn(() => { store = {}; }),
    key: vi.fn((i) => Object.keys(store)[i]),
    get length() { return Object.keys(store).length; },
    // Custom helper for test
    _store: () => store
  };
})();

// Assign to global window object (jsdom environment)
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock Fetch
global.fetch = vi.fn();

describe('API Fetcher Performance & Granular Caching', () => {
  beforeEach(() => {
    localStorageMock.clear();
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    localStorageMock.removeItem.mockClear();
    vi.clearAllMocks();
  });

  it('should use granular caching keys instead of monolithic cache', async () => {
    // Mock fetch response
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ test: 'data' })
    });

    const data = await fetchWithCache('test_key', async () => {
        const res = await fetch('url');
        return res.json();
    });

    expect(data).toEqual({ test: 'data' });

    // Check if setItem was called with the new prefix
    // Expect '5d-map-cache-v2:test_key'
    expect(localStorageMock.setItem).toHaveBeenCalledWith(
        '5d-map-cache-v2:test_key',
        expect.stringContaining('"data":{"test":"data"}')
    );
  });

  it('should retrieve data from granular cache if valid', async () => {
     const cacheKey = '5d-map-cache-v2:cached_key';
     const cachedData = { data: { cached: true }, timestamp: Date.now() };
     localStorageMock.setItem(cacheKey, JSON.stringify(cachedData));

     // Fetch should NOT be called
     const fetcher = vi.fn();

     const result = await fetchWithCache('cached_key', fetcher);

     expect(result).toEqual({ cached: true });
     expect(fetcher).not.toHaveBeenCalled();
     expect(localStorageMock.getItem).toHaveBeenCalledWith(cacheKey);
  });

  it('should clear only granular cache keys', async () => {
      localStorageMock.setItem('5d-map-cache-v2:k1', 'val1');
      localStorageMock.setItem('5d-map-cache-v2:k2', 'val2');
      localStorageMock.setItem('other-app-key', 'keep-me');

      clearCache();

      const store = localStorageMock._store();
      expect(store['5d-map-cache-v2:k1']).toBeUndefined();
      expect(store['5d-map-cache-v2:k2']).toBeUndefined();
      expect(store['other-app-key']).toBeDefined();
  });
});
