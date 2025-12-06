/**
 * Unit Tests für 5D Map
 * Framework: Vitest (kompatibel mit Jest API)
 * Run: npm test
 */

import { describe, test, expect, beforeEach } from 'vitest';

describe('5D Map Core Functions', () => {
  test('IMP calculation is correct', () => {
    // IMP = A × IM × R × SP × Au (alle 0-1)
    const dims = {
      A: 0.8,   // Autonomy
      IM: 0.9,  // Intrinsic Motivation
      R: 0.7,   // Resilience
      SP: 0.6,  // Social Participation
      Au: 0.8   // Authenticity
    };
    
    const imp = dims.A * dims.IM * dims.R * dims.SP * dims.Au;
    expect(imp).toBeCloseTo(0.24192, 4);
  });

  test('normalize value clamps between 0 and 1', () => {
    const normalize = (val, min, max) => Math.max(0, Math.min(1, (val - min) / (max - min)));
    
    expect(normalize(-5, -2.5, 2.5)).toBe(0);
    expect(normalize(0, -2.5, 2.5)).toBe(0.5);
    expect(normalize(2.5, -2.5, 2.5)).toBe(1);
    expect(normalize(10, -2.5, 2.5)).toBe(1);
  });

  test('depression to IM conversion (1 - depression/100)', () => {
    const toIM = (depression) => Math.max(0, Math.min(1, 1 - depression / 100));
    
    expect(toIM(0)).toBe(1);    // 0% Depression → IM=1
    expect(toIM(50)).toBe(0.5);  // 50% Depression → IM=0.5
    expect(toIM(100)).toBe(0);   // 100% Depression → IM=0
    expect(toIM(150)).toBe(0);   // >100% clamped to 0
  });

  test('dropout to Autonomy conversion (1 - dropout/100)', () => {
    const toA = (dropout) => Math.max(0, Math.min(1, 1 - dropout / 100));
    
    expect(toA(0)).toBe(1);
    expect(toA(25)).toBe(0.75);
    expect(toA(100)).toBe(0);
  });
});

describe('WGI Normalization', () => {
  test('WGI RL.EST normalization (-2.5 to 2.5 → 0 to 1)', () => {
    const normalizeWGI = (val) => {
      if (val == null) return 0.5;
      return Math.max(0, Math.min(1, (val + 2.5) / 5));
    };
    
    expect(normalizeWGI(-2.5)).toBe(0);
    expect(normalizeWGI(0)).toBe(0.5);
    expect(normalizeWGI(2.5)).toBe(1);
    expect(normalizeWGI(null)).toBe(0.5);
  });
});

describe('Heatmap Intensity Calculation', () => {
  test('combines depression and dropout correctly', () => {
    const calculateIntensity = (depression, dropout) => {
      const dep = depression ?? 0;
      const drp = dropout ?? 0;
      const avg = (dep + drp) / 2;
      return Math.max(0, Math.min(1, avg / 100));
    };
    
    expect(calculateIntensity(20, 30)).toBeCloseTo(0.25, 2);
    expect(calculateIntensity(0, 0)).toBe(0);
    expect(calculateIntensity(100, 100)).toBe(1);
    expect(calculateIntensity(null, 50)).toBeCloseTo(0.25, 2);
  });
});

describe('Color Mapping for IMP', () => {
  test('returns correct color for IMP score', () => {
    const getIMPColor = (imp) => {
      if (imp >= 0.7) return '#22C55E'; // Dunkelgrün
      if (imp >= 0.5) return '#84CC90'; // Hellgrün
      if (imp >= 0.3) return '#FDE68A'; // Gelb
      if (imp >= 0.2) return '#E8814A'; // Orange
      return '#C0152F'; // Rot
    };
    
    expect(getIMPColor(0.8)).toBe('#22C55E');
    expect(getIMPColor(0.6)).toBe('#84CC90');
    expect(getIMPColor(0.4)).toBe('#FDE68A');
    expect(getIMPColor(0.25)).toBe('#E8814A');
    expect(getIMPColor(0.1)).toBe('#C0152F');
  });
});

describe('Data Validation', () => {
  test('validates school data structure', () => {
    const school = {
      name: 'Test School',
      type: 'sudbury',
      lat: 52.52,
      lng: 13.40,
      founded: 2010,
      students: 100,
      outcomes: {
        college: 85,
        satisfaction: 90
      }
    };
    
    expect(school).toHaveProperty('name');
    expect(school).toHaveProperty('lat');
    expect(school).toHaveProperty('lng');
    expect(school.type).toMatch(/^(sudbury|waldorf|folk-high|tokkatsu)$/);
    expect(school.lat).toBeGreaterThanOrEqual(-90);
    expect(school.lat).toBeLessThanOrEqual(90);
    expect(school.lng).toBeGreaterThanOrEqual(-180);
    expect(school.lng).toBeLessThanOrEqual(180);
  });

  test('validates country data has ISO3 code', () => {
    const country = {
      name: 'Germany',
      iso3: 'DEU',
      lat: 51.1657,
      lng: 10.4515
    };
    
    expect(country.iso3).toHaveLength(3);
    expect(country.iso3).toMatch(/^[A-Z]{3}$/);
  });
});

describe('Cache Strategy', () => {
  test('checks if cache is expired (1 hour TTL)', () => {
    const CACHE_TTL = 3600000; // 1 hour in ms
    
    const isCacheValid = (timestamp) => {
      return Date.now() - timestamp < CACHE_TTL;
    };
    
    const now = Date.now();
    expect(isCacheValid(now)).toBe(true);
    expect(isCacheValid(now - 1800000)).toBe(true); // 30 min ago
    expect(isCacheValid(now - 3600000)).toBe(false); // exactly 1h ago
    expect(isCacheValid(now - 7200000)).toBe(false); // 2h ago
  });
});
