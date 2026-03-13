import { describe, test, expect, vi, beforeEach } from 'vitest';
// Note: fetchWithCache is not currently exported in the original file,
// but we will export it in the refactor step.
import { fetchAllData, fetchWithCache, clearCache } from '../modules/api-fetcher.js';

// Mock global fetch
const fetchMock = vi.fn();
global.fetch = fetchMock;

describe('API Fetcher Performance', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    clearCache();
  });

  test('fetchWithCache handles concurrent writes without data loss', async () => {
    // Simulation of the Race Condition:
    // 1. Two async operations start.
    // 2. Both read the initial cache state (empty).
    // 3. One finishes and writes its result.
    // 4. The other finishes and writes its result, potentially overwriting the first one
    //    if it writes the stale cache copy it read at step 2.

    fetchMock.mockImplementation(async (url) => {
      if (url === 'url-a') {
        await new Promise(r => setTimeout(r, 20)); // Delay A
        return { ok: true, json: async () => ({ id: 'A' }) };
      }
      if (url === 'url-b') {
        await new Promise(r => setTimeout(r, 40)); // Delay B
        return { ok: true, json: async () => ({ id: 'B' }) };
      }
      return { ok: false };
    });

    // Execute concurrently
    // We pass simple fetchers that return the mocked JSON
    const p1 = fetchWithCache('key-a', () => fetch('url-a').then(r => r.json()));
    const p2 = fetchWithCache('key-b', () => fetch('url-b').then(r => r.json()));

    await Promise.all([p1, p2]);

    // Check localStorage directly to verify persistence
    const storedRaw = localStorage.getItem('5d-map-cache-v1');
    const stored = storedRaw ? JSON.parse(storedRaw) : {};

    // Expect BOTH keys to be present.
    // If the race condition exists, one might be missing (likely key-a because B finishes last and overwrites).
    expect(stored).toHaveProperty('key-a');
    expect(stored).toHaveProperty('key-b');
  });

  test('fetchAllData executes requests in parallel', async () => {
    // Mock all fetches with a significant delay
    const DELAY = 50;
    fetchMock.mockImplementation(async (url) => {
      await new Promise(r => setTimeout(r, DELAY));

      // Return minimal valid data to prevent processing errors
      if (url.endsWith('.csv')) {
        return { ok: true, text: async () => "Code,Year,Val\nDEU,2020,10" };
      }
      // JSON response
      return { ok: true, json: async () => [] };
    });

    const start = Date.now();
    await fetchAllData();
    const end = Date.now();
    const duration = end - start;

    // There are ~12 independent fetches.
    // If sequential: duration >= 12 * 50ms = 600ms
    // If parallel: duration ~ 50ms (plus overhead)
    // We allow some buffer, so if it's under 200ms, it's definitely parallel.
    console.log(`Duration: ${duration}ms`);
    expect(duration).toBeLessThan(300);
  }, 10000); // 10s timeout
});
