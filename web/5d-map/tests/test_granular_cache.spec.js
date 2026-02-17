import { describe, test, expect, beforeEach, vi } from 'vitest';
import { fetchWithCache, clearCache } from '../modules/api-fetcher.js';

describe('Granular Caching', () => {
  const CACHE_PREFIX = '5d-map-v1:';
  const LEGACY_CACHE_KEY = '5d-map-cache-v1';

  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  test('fetchWithCache uses granular keys', async () => {
    const key = 'test-granular';
    const data = { foo: 'bar' };
    const fetcher = vi.fn().mockResolvedValue(data);

    // First call: cache miss, fetcher called, data cached
    const result1 = await fetchWithCache(key, fetcher);
    expect(result1).toEqual(data);
    expect(fetcher).toHaveBeenCalledTimes(1);

    // Verify granular key exists
    const stored = localStorage.getItem(CACHE_PREFIX + key);
    expect(stored).toBeTruthy();
    const parsed = JSON.parse(stored);
    expect(parsed.data).toEqual(data);
    expect(parsed.timestamp).toBeDefined();

    // Verify monolithic key does NOT exist (or at least isn't used for this new entry)
    // Note: If code is not updated yet, this assertion will fail because it WILL use monolithic key.
    // So this test confirms the change.
    const monolithic = localStorage.getItem(LEGACY_CACHE_KEY);
    expect(monolithic).toBeNull();

    // Second call: cache hit, fetcher NOT called
    const result2 = await fetchWithCache(key, fetcher);
    expect(result2).toEqual(data);
    expect(fetcher).toHaveBeenCalledTimes(1);
  });

  test('clearCache removes both legacy and granular keys', () => {
    // Setup legacy cache
    localStorage.setItem(LEGACY_CACHE_KEY, JSON.stringify({ old: 'data' }));

    // Setup granular cache
    localStorage.setItem(CACHE_PREFIX + 'k1', JSON.stringify({ data: 1 }));
    localStorage.setItem(CACHE_PREFIX + 'k2', JSON.stringify({ data: 2 }));

    // Setup unrelated key
    localStorage.setItem('other-app-data', 'preserve-me');

    clearCache();

    expect(localStorage.getItem(LEGACY_CACHE_KEY)).toBeNull();
    expect(localStorage.getItem(CACHE_PREFIX + 'k1')).toBeNull();
    expect(localStorage.getItem(CACHE_PREFIX + 'k2')).toBeNull();
    expect(localStorage.getItem('other-app-data')).toBe('preserve-me');
  });
});
