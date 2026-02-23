import { describe, test, expect, beforeEach } from 'vitest';
import { fetchWithCache, clearCache } from '../modules/api-fetcher.js';

describe('Concurrency Tests', () => {
  beforeEach(() => {
    clearCache();
    localStorage.clear();
  });

  test('parallel fetchWithCache calls should not lose data due to race conditions', async () => {
    // Create a fetcher that waits a bit to ensure overlap
    // The delay ensures that all calls read the 'old' cache state before any of them writes the new state.
    const slowFetcher = (val) => async () => {
      await new Promise(resolve => setTimeout(resolve, 50));
      return val;
    };

    // Start 5 parallel requests
    // Without the fix, they will all read an empty cache (or near empty).
    // When they finish, they will each write a cache containing only THEIR entry (plus whatever was there at start).
    // The last one to write 'wins', but the previous writes are lost.
    const p1 = fetchWithCache('key1', slowFetcher('value1'));
    const p2 = fetchWithCache('key2', slowFetcher('value2'));
    const p3 = fetchWithCache('key3', slowFetcher('value3'));
    const p4 = fetchWithCache('key4', slowFetcher('value4'));
    const p5 = fetchWithCache('key5', slowFetcher('value5'));

    await Promise.all([p1, p2, p3, p4, p5]);

    // Check localStorage
    const raw = localStorage.getItem('5d-map-cache-v1');
    const cache = raw ? JSON.parse(raw) : {};

    // Verify all keys are present
    const keys = Object.keys(cache);
    console.log('Final cache keys:', keys);

    expect(cache).toHaveProperty('key1');
    expect(cache).toHaveProperty('key2');
    expect(cache).toHaveProperty('key3');
    expect(cache).toHaveProperty('key4');
    expect(cache).toHaveProperty('key5');
  });
});
