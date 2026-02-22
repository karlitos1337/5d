import { describe, test, expect, beforeEach, vi } from 'vitest';
import { fetchWithCache, clearCache } from '../modules/api-fetcher.js';

describe('fetchWithCache Concurrency', () => {
  beforeEach(() => {
    clearCache();
    vi.clearAllMocks();
  });

  test('handles concurrent writes correctly', async () => {
    // Simulate two slow fetchers running in parallel
    const fetcher1 = async () => {
      await new Promise(resolve => setTimeout(resolve, 50));
      return 'data1';
    };

    const fetcher2 = async () => {
      await new Promise(resolve => setTimeout(resolve, 50));
      return 'data2';
    };

    // Start both fetches
    const p1 = fetchWithCache('key1', fetcher1);
    const p2 = fetchWithCache('key2', fetcher2);

    await Promise.all([p1, p2]);

    // Check if both keys are in cache
    const cache = JSON.parse(localStorage.getItem('5d-map-cache-v1') || '{}');

    // Without the fix, one might overwrite the other
    expect(cache).toHaveProperty('key1');
    expect(cache).toHaveProperty('key2');
    expect(cache.key1.data).toBe('data1');
    expect(cache.key2.data).toBe('data2');
  });
});
