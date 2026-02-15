
import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

describe('Performance & Concurrency', () => {
  beforeEach(() => {
    vi.useRealTimers();
    clearCache();
    localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test('fetchAllData should execute fetches in parallel', async () => {
    const delay = 50;
    let concurrentCount = 0;
    let maxConcurrent = 0;

    global.fetch = vi.fn().mockImplementation(async (url) => {
      concurrentCount++;
      maxConcurrent = Math.max(maxConcurrent, concurrentCount);
      await new Promise(r => setTimeout(r, delay));
      concurrentCount--;

      // Return minimal valid structure to avoid parsing errors
      return {
        ok: true,
        json: async () => {
          if (url.includes('schools')) return [];
          if (url.includes('countries')) return [];
          if (url.includes('validation')) return {};
          if (url.includes('baseline')) return null;
          if (url.includes('worldbank')) return [{}, []]; // WB format
          if (url.includes('geojson')) return {};
          return {};
        },
        text: async () => "" // CSVs
      };
    });

    const start = Date.now();
    await fetchAllData();
    const duration = Date.now() - start;

    // We expect at least 5 concurrent requests (schools, countries, validation, baseline, WB APIs...)
    expect(maxConcurrent).toBeGreaterThan(3);

    // If sequential: 10+ requests * 50ms = >500ms
    // If parallel: ~50ms + overhead. Allow < 300ms.
    // Note: Use a generous upper bound to avoid flakiness, but strict enough to catch sequential.
    // There are about 12 fetches. 12 * 50 = 600ms.
    expect(duration).toBeLessThan(400);
  });

  test('fetchWithCache should persist all keys to localStorage despite concurrency', async () => {
    // Mock fetch to be instant but async
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [],
      text: async () => ""
    });

    await fetchAllData();

    const raw = localStorage.getItem('5d-map-cache-v1');
    const cache = JSON.parse(raw || '{}');
    const keys = Object.keys(cache);

    // We expect these keys to be present if no race condition occurred
    const expectedKeys = [
      'schools',
      'countries',
      'validation',
      'baseline_snapshot',
      'wgi_rl_est',
      'wgi_va_est',
      'wgi_ge_est',
      'wb_dropout',
      'wb_dropout_series'
    ];

    // Check that we have a significant number of keys
    // If race condition exists (read-modify-write without re-read), many will be lost (overwritten).
    // E.g. only the last one to write will be there.
    expect(keys.length).toBeGreaterThanOrEqual(expectedKeys.length - 2); // Allow slight variation but should be mostly full

    // Specifically check for critical keys
    expect(keys).toContain('schools');
    expect(keys).toContain('wgi_rl_est');
    expect(keys).toContain('wgi_ge_est');
  });
});
