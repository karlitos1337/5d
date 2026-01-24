import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

describe('api-fetcher performance', () => {
  beforeEach(() => {
    // Mock localStorage
    const store = {};
    vi.stubGlobal('localStorage', {
      getItem: (key) => store[key] || null,
      setItem: (key, value) => { store[key] = value; },
      removeItem: (key) => { delete store[key]; },
    });

    // Mock fetch with delays
    vi.stubGlobal('fetch', async (url) => {
      await new Promise(r => setTimeout(r, 50)); // 50ms delay per request

      // Return minimal valid data structure for each endpoint
      if (url.includes('schools')) return { ok: true, json: async () => [] };
      if (url.includes('countries.json')) return { ok: true, json: async () => [] };
      if (url.includes('validation')) return { ok: true, json: async () => ({ validatedISO3: [], items: [] }) };
      if (url.includes('baseline')) return { ok: true, json: async () => null };

      // CSV response for depression (Code, Year, Value)
      if (url.includes('depression')) return { ok: true, text: async () => 'Code,Year,Val\nDEU,2020,5.5' };

      // World Bank API response structure: [metadata, data]
      if (url.includes('worldbank') || url.includes('indicator')) return { ok: true, json: async () => [{}, []] };

      if (url.includes('geojson')) return { ok: true, json: async () => ({ type: 'FeatureCollection', features: [] }) };

      return { ok: false, status: 404 };
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    clearCache();
  });

  it('measures fetchAllData execution time', async () => {
    const start = Date.now();
    await fetchAllData();
    const end = Date.now();
    const duration = end - start;

    console.log(`fetchAllData took ${duration}ms`);

    // We export the duration so we can see it in logs
    // 12 sequential requests * 50ms = ~600ms
    // Parallel should be ~50ms
  });
});
