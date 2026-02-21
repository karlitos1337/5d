import { describe, test, expect, beforeEach, vi } from 'vitest';
import { fetchWithCache, clearCache } from '../modules/api-fetcher.js';

describe('Concurrency and Caching', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  test('Parallel fetches should both persist to cache (Race Condition Fix)', async () => {
    // Mock fetchers with delay to ensure they overlap
    const fetchA = async () => {
      await new Promise(resolve => setTimeout(resolve, 50));
      return 'dataA';
    };
    const fetchB = async () => {
      await new Promise(resolve => setTimeout(resolve, 50));
      return 'dataB';
    };

    // Run in parallel
    // If race condition exists:
    // 1. A reads cache {}
    // 2. B reads cache {}
    // 3. A finishes, writes {A}
    // 4. B finishes, writes {B} (overwriting A)
    // Fix: B finishes, re-reads {A}, writes {A, B}
    await Promise.all([
      fetchWithCache('keyA', fetchA),
      fetchWithCache('keyB', fetchB)
    ]);

    // Verify localStorage has both keys
    const raw = localStorage.getItem('5d-map-cache-v1');
    expect(raw).not.toBeNull();
    const cache = JSON.parse(raw);

    expect(cache).toHaveProperty('keyA');
    expect(cache.keyA.data).toBe('dataA');

    expect(cache).toHaveProperty('keyB');
    expect(cache.keyB.data).toBe('dataB');
  });

  test('Sequential fetches should work correctly', async () => {
    await fetchWithCache('key1', async () => 'data1');
    await fetchWithCache('key2', async () => 'data2');

    const cache = JSON.parse(localStorage.getItem('5d-map-cache-v1'));
    expect(cache.key1.data).toBe('data1');
    expect(cache.key2.data).toBe('data2');
  });
});
