import { describe, test, expect, beforeEach, vi } from 'vitest';
import { fetchWithCache, clearCache } from '../modules/api-fetcher.js';

describe('Granular Caching Strategy', () => {
  const PREFIX = '5d-map-v1:';
  const LEGACY_KEY = '5d-map-cache-v1';

  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  test('fetchWithCache fetches data and stores it with granular key', async () => {
    const key = 'test-data';
    const data = { value: 123 };
    const fetcher = vi.fn().mockResolvedValue(data);

    // First call: should fetch
    const result1 = await fetchWithCache(key, fetcher);
    expect(result1).toEqual(data);
    expect(fetcher).toHaveBeenCalledTimes(1);

    // Check localStorage
    const storedRaw = localStorage.getItem(PREFIX + key);
    expect(storedRaw).not.toBeNull();
    const stored = JSON.parse(storedRaw);
    expect(stored.data).toEqual(data);
    expect(stored.timestamp).toBeTypeOf('number');
  });

  test('fetchWithCache uses cached data on second call', async () => {
    const key = 'test-data';
    const data = { value: 456 };
    const fetcher = vi.fn().mockResolvedValue(data);

    // Pre-populate cache
    localStorage.setItem(PREFIX + key, JSON.stringify({
      data,
      timestamp: Date.now()
    }));

    // Call: should use cache
    const result = await fetchWithCache(key, fetcher);
    expect(result).toEqual(data);
    expect(fetcher).not.toHaveBeenCalled();
  });

  test('clearCache removes granular keys and legacy key', () => {
    localStorage.setItem(PREFIX + 'key1', '{"data":1}');
    localStorage.setItem(PREFIX + 'key2', '{"data":2}');
    localStorage.setItem(LEGACY_KEY, '{"old":3}');
    localStorage.setItem('other-app-key', 'keep-me');

    clearCache();

    expect(localStorage.getItem(PREFIX + 'key1')).toBeNull();
    expect(localStorage.getItem(PREFIX + 'key2')).toBeNull();
    expect(localStorage.getItem(LEGACY_KEY)).toBeNull();
    expect(localStorage.getItem('other-app-key')).toBe('keep-me');
  });
});
