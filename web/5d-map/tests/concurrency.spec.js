import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

// Mock localStorage
const mockStorage = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => { store[key] = value.toString(); },
    removeItem: (key) => { delete store[key]; },
    clear: () => { store = {}; }
  };
})();

Object.defineProperty(global, 'localStorage', {
  value: mockStorage
});

// Mock fetch
global.fetch = vi.fn();

describe('API Fetcher Concurrency', () => {
  beforeEach(() => {
    mockStorage.clear();
    clearCache();
    vi.resetAllMocks();

    // Default fetch mock setup to return empty arrays/objects to not crash
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ([]),
      text: async () => ('Code,Year,Value\nDEU,2020,1')
    });
  });

  it('handles concurrent execution without losing data', async () => {
    // If the cache was not re-read before writing, some cache entries would be lost
    // when using Promise.all because they all start with an empty cache object
    await fetchAllData();

    const cacheStr = mockStorage.getItem('5d-map-cache-v1');
    const cache = JSON.parse(cacheStr || '{}');

    // Check if multiple keys are present in the cache, indicating that
    // the concurrent writes didn't completely overwrite each other
    expect(Object.keys(cache).length).toBeGreaterThan(5);
    expect(cache.schools).toBeDefined();
    expect(cache.countries).toBeDefined();
    expect(cache.wgi_rl_est).toBeDefined();
  });
});
