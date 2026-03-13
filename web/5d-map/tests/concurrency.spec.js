import { describe, test, expect, vi, beforeEach } from 'vitest';
import { fetchWithCache, clearCache } from '../modules/api-fetcher.js';

describe('Concurrency Issues', () => {
  beforeEach(() => {
    // Mock localStorage
    let storage = {};
    vi.stubGlobal('localStorage', {
      getItem: (key) => storage[key] || null,
      setItem: (key, value) => { storage[key] = value; },
      removeItem: (key) => { delete storage[key]; },
      clear: () => { storage = {}; }
    });

    // Mock fetch to just return the requested url as data
    global.fetch = vi.fn((url) => Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ url })
    }));

    clearCache();
  });

  test('fetchWithCache race condition overwrites data', async () => {
    // This test simulates two concurrent fetches that finish at different times
    // Without the fix, both will read the empty cache at start,
    // and the one finishing last will overwrite the one finishing first.

    // Key A starts, reads empty cache
    // Key B starts, reads empty cache
    // Key A finishes, writes { A: ... }
    // Key B finishes, writes { B: ... } (overwriting A because it read empty cache)

    const delay = (ms) => new Promise(res => setTimeout(res, ms));

    const fetchA = () => fetchWithCache('keyA', async () => {
      await delay(50);
      return 'dataA';
    });

    const fetchB = () => fetchWithCache('keyB', async () => {
      await delay(100);
      return 'dataB';
    });

    // Run them in parallel
    await Promise.all([fetchA(), fetchB()]);

    // Check localStorage directly
    const raw = localStorage.getItem('5d-map-cache-v1');
    const cache = JSON.parse(raw);

    // If race condition exists, one key might be missing
    // We expect BOTH to be there if fixed
    // But for reproduction, we assert that the race condition happens (or just fail if it happens)

    // Actually, let's just assert that both keys SHOULD be present.
    // If the test fails, it confirms the bug.
    expect(cache).toHaveProperty('keyA');
    expect(cache).toHaveProperty('keyB');
    expect(cache.keyA.data).toBe('dataA');
    expect(cache.keyB.data).toBe('dataB');
  });
});
