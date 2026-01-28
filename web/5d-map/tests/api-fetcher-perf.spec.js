import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

describe('fetchAllData Performance', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it('measures execution time of fetchAllData', async () => {
    const DELAY = 50; // ms per request

    // Mock fetch with a delay
    global.fetch = vi.fn().mockImplementation(async (url) => {
      await new Promise(resolve => setTimeout(resolve, DELAY));

      let data = {};
      // Return iterable for countries/schools to avoid TypeError
      if (String(url).includes('countries.json')) data = [];
      if (String(url).includes('schools.json')) data = [];
      if (String(url).includes('validation.json')) data = { validatedISO3: [], items: [] };

      return {
        ok: true,
        status: 200,
        json: async () => data,
        text: async () => "",
      };
    });

    const start = performance.now();
    await fetchAllData();
    const end = performance.now();

    const duration = end - start;
    console.log(`\n⚡ fetchAllData execution time: ${duration.toFixed(2)}ms ⚡\n`);

    expect(global.fetch).toHaveBeenCalled();
  });
});
