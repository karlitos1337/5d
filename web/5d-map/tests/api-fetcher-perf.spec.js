
import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchAllData, clearCache } from '../modules/api-fetcher.js';

// Mock global fetch
const fetchMock = vi.fn();
global.fetch = fetchMock;

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: vi.fn((key) => store[key] || null),
    setItem: vi.fn((key, value) => { store[key] = value.toString(); }),
    removeItem: vi.fn((key) => { delete store[key]; }),
    clear: vi.fn(() => { store = {}; }),
    key: vi.fn((i) => Object.keys(store)[i] || null),
    get length() { return Object.keys(store).length; }
  };
})();
Object.defineProperty(global, 'localStorage', { value: localStorageMock });

describe('API Fetcher Performance & Granular Caching', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorageMock.clear();
    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => ({}),
      text: async () => ""
    });
  });

  test('uses granular cache keys instead of monolithic object', async () => {
    // Setup fetch to return distinct data
    fetchMock.mockImplementation((url) => {
      if (url.includes('schools')) return Promise.resolve({ ok: true, json: async () => [{ name: 'School A' }] });
      if (url.includes('countries')) return Promise.resolve({ ok: true, json: async () => [{ iso3: 'DEU' }] });
      return Promise.resolve({ ok: true, json: async () => ({}), text: async () => "" });
    });

    await fetchAllData();

    // Verify localStorage has granular keys
    const keys = Object.keys(localStorageMock.getItem.mock.calls).map(call => call && call[0]).filter(k => k && k.startsWith('5d-map-cache-v2:'));

    // We expect calls to getItem with keys like '5d-map-cache-v2:schools', '5d-map-cache-v2:countries', etc.
    // The exact implementation might vary, but we want to ensure we are NOT just getting one big key.

    // Check if any setItem call used the new prefix
    const setCalls = localStorageMock.setItem.mock.calls;
    const hasGranularKey = setCalls.some(args => args[0].startsWith('5d-map-cache-v2:schools'));

    expect(hasGranularKey).toBe(true);
  });

  test('fetches data in parallel', async () => {
    // Create a delayed fetch to simulate network latency
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    fetchMock.mockImplementation(async (url) => {
      await delay(100); // 100ms delay for each request
      if (url.includes('schools')) return { ok: true, json: async () => [] };
      if (url.includes('countries')) return { ok: true, json: async () => [] };
      return { ok: true, json: async () => ({}), text: async () => "" };
    });

    const start = Date.now();
    await fetchAllData();
    const duration = Date.now() - start;

    // If sequential: 10+ requests * 100ms = >1000ms
    // If parallel: ~100ms + overhead
    // We allow some buffer, but it should be significantly less than sequential sum.
    // There are at least 10 fetches.
    expect(duration).toBeLessThan(800);
  });
});
