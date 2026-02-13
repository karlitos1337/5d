import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

describe('fetchAllData Concurrency', () => {
  let fetchMock;

  beforeEach(() => {
    // Clear localStorage to force network requests
    localStorage.clear();

    // Mock global fetch
    fetchMock = vi.fn();
    global.fetch = fetchMock;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test('should fetch data in parallel', async () => {
    // Create a controlled promise for fetch responses
    let resolveRef = [];

    fetchMock.mockImplementation(() => {
      return new Promise((resolve) => {
        resolveRef.push(resolve);
      });
    });

    // Start fetchAllData
    const fetchPromise = fetchAllData();

    // Allow any synchronous code to run (and start fetches)
    await new Promise(r => setTimeout(r, 0));

    // Check how many fetch calls have been initiated
    const callCount = fetchMock.mock.calls.length;
    console.log(`Fetch calls initiated: ${callCount}`);

    // If parallel, we expect multiple calls to be in flight.
    // There are about 12 fetches in fetchAllData.
    // If sequential, only 1 should be in flight (waiting for the first to resolve).

    // We expect at least more than 1 if some parallelism is happening.
    expect(callCount).toBeGreaterThan(1);

    // Clean up: Resolve all pending promises to avoid hanging
    resolveRef.forEach(resolve => resolve({
      ok: true,
      json: async () => ({}),
      text: async () => ""
    }));

    try {
      await fetchPromise;
    } catch (e) {
      // Ignore errors from empty responses
    }
  });
});
