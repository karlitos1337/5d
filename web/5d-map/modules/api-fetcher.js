const CACHE_KEY = '5d-map-cache-v1';
const CACHE_TTL = 60 * 60 * 1000; // 1h

function loadCache() {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveCache(cache) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(cache));
  } catch {
    // ignore
  }
}

export function clearCache() {
  try {
    localStorage.removeItem(CACHE_KEY);
  } catch {
    // ignore
  }
}

async function fetchJSON(url) {
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.json();
}

async function fetchWithCache(key, fetcher) {
  const cache = loadCache();
  const now = Date.now();
  const entry = cache[key];
  if (entry && (now - entry.timestamp) < CACHE_TTL) {
    return entry.data;
  }
  try {
    const data = await fetcher();
    // Re-read cache to ensure we don't overwrite parallel updates
    const currentCache = loadCache();
    currentCache[key] = { data, timestamp: now };
    saveCache(currentCache);
    return data;
  } catch (e) {
    if (entry) return entry.data; // Fallback auf alten Cache
    throw e;
  }
}

export async function fetchAllData() {
  const result = {};

  // WGI‑Proxies (World Bank Governance Indicators) Helper
  const wgiFetch = async (code) => {
    const url = `https://api.worldbank.org/v2/country/all/indicator/${code}?format=json&per_page=20000`;
    const data = await fetchJSON(url);
    const rows = Array.isArray(data) ? data[1] || [] : [];
    const latest = {};
    for (const r of rows) {
      const iso3 = r?.countryiso3code; const year = Number(r?.date);
      const val = r?.value == null ? null : Number(r.value);
      if (!iso3 || val == null || Number.isNaN(val)) continue;
      const prev = latest[iso3];
      if (!prev || year > prev.year) latest[iso3] = { value: val, year };
    }
    const map = {};
    for (const [k, v] of Object.entries(latest)) map[k] = v.value;
    return map;
  };

  // Start all fetches in parallel
  const schoolsPromise = fetchWithCache('schools', () => fetchJSON('./data/schools.json'))
    .catch(() => []);

  const countriesPromise = fetchWithCache('countries', () => fetchJSON('./data/countries.json'))
    .catch(() => []);

  const validationPromise = fetchWithCache('validation', () => fetchJSON('./data/validation.json'))
    .catch(() => ({ validatedISO3: [], items: [] }));

  const baselinePromise = fetchWithCache('baseline_snapshot', () => fetchJSON('./data/baseline.json'))
    .catch(() => null);

  const depressionMapPromise = fetchWithCache('owid_depression', async () => {
    const proxyUrl = 'http://localhost:5510/proxy/depression-prevalence.csv';
    const remoteUrl = 'https://ourworldindata.org/grapher/depression-prevalence.csv';
    try {
      let res = await fetch(proxyUrl, { cache: 'no-store' });
      if (!res.ok) {
        res = await fetch(remoteUrl, { cache: 'no-store' });
      }
      if (!res.ok) throw new Error(`HTTP ${res.status} for ${remoteUrl}`);
      const text = await res.text();
      const rows = parseCSV(text);
      return reduceLatestByCode(rows, 'Code');
    } catch (e) {
      console.warn('Depression remote fetch fehlgeschlagen, nutze lokalen Fallback:', e.message);
      const localRes = await fetch('./data/depression_sample.csv');
      const localText = await localRes.text();
      const localRows = parseCSV(localText);
      return reduceLatestByCode(localRows, 'Code');
    }
  }).catch(() => ({}));

  const depressionSeriesPromise = fetchWithCache('owid_depression_series', async () => {
    const proxyUrl = 'http://localhost:5510/proxy/depression-prevalence.csv';
    const remoteUrl = 'https://ourworldindata.org/grapher/depression-prevalence.csv';
    const buildSeries = (rows) => {
      const series = {};
      for (const r of rows) {
        const code = r.Code; const year = r.Year; const valueKey = Object.keys(r).slice(-1)[0];
        const val = r[valueKey];
        if (!code || !year || val == null || Number.isNaN(val)) continue;
        if (!series[code]) series[code] = {};
        series[code][year] = val;
      }
      return series;
    };
    try {
      let res = await fetch(proxyUrl, { cache: 'no-store' });
      if (!res.ok) {
        res = await fetch(remoteUrl, { cache: 'no-store' });
      }
      if (!res.ok) throw new Error(`HTTP ${res.status} for ${remoteUrl}`);
      const text = await res.text();
      const rows = parseCSV(text);
      return buildSeries(rows);
    } catch (e) {
      console.warn('Depression series remote fetch fehlgeschlagen, Fallback lokal:', e.message);
      const localRes = await fetch('./data/depression_sample.csv');
      const localText = await localRes.text();
      const localRows = parseCSV(localText);
      return buildSeries(localRows);
    }
  }).catch(() => ({}));

  const dropoutMapPromise = fetchWithCache('wb_dropout', async () => {
    const url = 'https://api.worldbank.org/v2/country/all/indicator/SE.PRM.DROPOUT.ZS?format=json&per_page=20000';
    const data = await fetchJSON(url);
    const rows = Array.isArray(data) ? data[1] || [] : [];
    const latest = {};
    for (const r of rows) {
      const iso3 = r?.countryiso3code; const year = Number(r?.date);
      const val = r?.value == null ? null : Number(r.value);
      if (!iso3 || val == null || Number.isNaN(val)) continue;
      const prev = latest[iso3];
      if (!prev || year > prev.year) latest[iso3] = { value: val, year };
    }
    const map = {};
    for (const [k, v] of Object.entries(latest)) map[k] = v.value;
    return map;
  }).catch(() => ({}));

  const dropoutSeriesPromise = fetchWithCache('wb_dropout_series', async () => {
    try {
      const url = 'https://api.worldbank.org/v2/country/all/indicator/SE.PRM.DROPOUT.ZS?format=json&per_page=20000';
      const data = await fetchJSON(url);
      const rows = Array.isArray(data) ? data[1] || [] : [];
      const series = {};
      for (const r of rows) {
        const iso3 = r?.countryiso3code; const year = Number(r?.date); const val = r?.value == null ? null : Number(r.value);
        if (!iso3 || !year || val == null || Number.isNaN(val)) continue;
        if (!series[iso3]) series[iso3] = {};
        series[iso3][year] = val;
      }
      return series;
    } catch { return {}; }
  }).catch(() => ({}));

  const wgiRlPromise = fetchWithCache('wgi_rl_est', () => wgiFetch('RL.EST')).catch(() => ({}));
  const wgiVaPromise = fetchWithCache('wgi_va_est', () => wgiFetch('VA.EST')).catch(() => ({}));
  const wgiGePromise = fetchWithCache('wgi_ge_est', () => wgiFetch('GE.EST')).catch(() => ({}));

  const geoJsonPromise = fetchWithCache('world_geojson', async () => {
    const url = 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson';
    return fetchJSON(url);
  }).catch(() => null);

  // Await all concurrently
  const [
    schools,
    countries,
    validation,
    baseline,
    depressionMap,
    depressionSeries,
    dropoutMap,
    dropoutSeries,
    wgi_rl_raw,
    wgi_va_raw,
    wgi_ge_raw,
    worldGeoJSON
  ] = await Promise.all([
    schoolsPromise,
    countriesPromise,
    validationPromise,
    baselinePromise,
    depressionMapPromise,
    depressionSeriesPromise,
    dropoutMapPromise,
    dropoutSeriesPromise,
    wgiRlPromise,
    wgiVaPromise,
    wgiGePromise,
    geoJsonPromise
  ]);

  result.schools = schools;
  result.worldGeoJSON = worldGeoJSON;

  const normalizeWGI = (m) => {
    const out = {};
    for (const [k, v] of Object.entries(m)) {
      const norm = (Number(v) + 2.5) / 5;
      out[k] = Number.isFinite(norm) ? Math.max(0, Math.min(1, norm)) : undefined;
    }
    return out;
  };

  const wgi_rl = normalizeWGI(wgi_rl_raw); // R
  const wgi_va = normalizeWGI(wgi_va_raw); // SP
  const wgi_ge = normalizeWGI(wgi_ge_raw); // Au

  // Baseline-Merge: Fehlende Werte aus Baseline einpflegen (nur Latest-Level, nicht Serien)
  function mergeMissing(target, baseSection) {
    if (!baseSection) return;
    for (const [iso3, val] of Object.entries(baseSection)) {
      if (target[iso3] == null) target[iso3] = val;
    }
  }
  if (baseline) {
    mergeMissing(depressionMap, baseline.depression_latest);
    mergeMissing(dropoutMap, baseline.dropout_latest);
    // WGI Rohwerte baseline in raw maps, danach erneut normalisieren für konsistente Skala
    mergeMissing(wgi_rl_raw, baseline.wgi_rl);
    mergeMissing(wgi_va_raw, baseline.wgi_va);
    mergeMissing(wgi_ge_raw, baseline.wgi_ge);
  }
  const wgi_rl_full = normalizeWGI(wgi_rl_raw);
  const wgi_va_full = normalizeWGI(wgi_va_raw);
  const wgi_ge_full = normalizeWGI(wgi_ge_raw);

  // Heatmap-Punkte: Mittelwert aus normierten (%) Werten, sofern vorhanden
  result.heatmapPoints = [];
  // Stelle Länder für andere Layer bereit
  result.countries = countries;
  for (const c of countries) {
    const iso3 = c.iso3;
    const lat = Number(c.lat), lng = Number(c.lng);
    if (!iso3 || Number.isNaN(lat) || Number.isNaN(lng)) continue;
    const dep = depressionMap[iso3]; // Prozent
    const drp = dropoutMap[iso3];    // Prozent
    if (dep == null && drp == null) continue;
    const vals = [];
    if (typeof dep === 'number') vals.push(dep);
    if (typeof drp === 'number') vals.push(drp);
    if (!vals.length) continue;
    const intensity = Math.max(0, Math.min(1, (vals.reduce((a,b)=>a+b,0)/vals.length) / 100));
    result.heatmapPoints.push([lat, lng, intensity]);
  }

  // IMP-Berechnung (Proxy-basiert) pro ISO3, nutzt Depression & Dropout
  // Dimensionen in [0,1]:
  // A  = 1 - clamp(dropout/100)         (Zugang)
  // IM = 1 - clamp(depression/100)      (Mental Health, invertiert)
  // R  = WGI Rule of Law (RL.EST)       → (x+2.5)/5
  // SP = WGI Voice & Accountability (VA.EST) → (x+2.5)/5
  // Au = WGI Gov. Effectiveness (GE.EST)→ (x+2.5)/5
  // IMP_raw = A * IM * R * SP * Au; clamp auf [0,1]
  result.impByISO3 = {};
  const clamp01 = (x) => Math.max(0, Math.min(1, x));
  for (const iso3 of Object.keys({ ...depressionMap, ...dropoutMap, ...wgi_rl_full, ...wgi_va_full, ...wgi_ge_full })) {
    const dep = depressionMap[iso3]; // %
    const drp = dropoutMap[iso3]; // %
    const A = drp == null ? 0.5 : (1 - clamp01(Number(drp) / 100));
    const IM = dep == null ? 0.5 : (1 - clamp01(Number(dep) / 100));
    const R = wgi_rl_full[iso3] ?? 0.5;
    const SP = wgi_va_full[iso3] ?? 0.5;
    const Au = wgi_ge_full[iso3] ?? 0.5;
    const raw = clamp01(A * IM * R * SP * Au);
    result.impByISO3[iso3] = {
      score: raw,
      dims: { A, IM, R, SP, Au },
      sources: { dep, drp, wgi_rl: wgi_rl_raw[iso3], wgi_va: wgi_va_raw[iso3], wgi_ge: wgi_ge_raw[iso3], baseline: Boolean(baseline) }
    };
  }

  result.baselineApplied = Boolean(baseline);

  // Zeitreise: verfügbare Jahre (Schnittmenge oder Vereinigung) für Slider
  const yearSet = new Set();
  for (const iso3 of Object.keys(depressionSeries)) {
    Object.keys(depressionSeries[iso3]).forEach(y => yearSet.add(Number(y)));
  }
  for (const iso3 of Object.keys(dropoutSeries)) {
    Object.keys(dropoutSeries[iso3]).forEach(y => yearSet.add(Number(y)));
  }
  const years = Array.from(yearSet).filter(y => Number.isFinite(y)).sort((a,b)=>a-b);
  result.seriesYears = years;
  result.depressionSeries = depressionSeries;
  result.dropoutSeries = dropoutSeries;
  // Validierungs‑ und Quelleninfos bereitstellen
  result.validatedISO3 = Array.isArray(validation.validatedISO3) ? validation.validatedISO3 : [];
  result.validationItems = Array.isArray(validation.items) ? validation.items : [];
  // einfache Quellenzählung pro ISO3 aus validation.items (optional)
  const sourcesByISO3 = {};
  for (const c of countries) {
    sourcesByISO3[c.iso3] = { count: 0, categories: [] };
  }
  if (Array.isArray(validation.items)) {
    for (const it of validation.items) {
      const cat = String(it.domain || 'misc');
      const status = String(it.status || 'red');
      // Optionale ISO3‑Zuordnung per item.iso3
      if (it.iso3 && sourcesByISO3[it.iso3]) {
        sourcesByISO3[it.iso3].count += 1;
        if (!sourcesByISO3[it.iso3].categories.includes(cat)) sourcesByISO3[it.iso3].categories.push(cat);
        if (!sourcesByISO3[it.iso3].categories.includes(status)) sourcesByISO3[it.iso3].categories.push(status);
      }
    }
  }
  result.sourcesByISO3 = sourcesByISO3;

  return result;
}

// --- Helpers ---
function parseCSV(text) {
  const lines = text.split(/\r?\n/).filter(Boolean);
  if (!lines.length) return [];
  const headers = splitCSVLine(lines[0]);
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const cols = splitCSVLine(lines[i]);
    if (!cols.length) continue;
    const obj = {};
    headers.forEach((h, idx) => obj[h] = cols[idx]);
    // normalize numeric
    if (obj.Year) obj.Year = Number(obj.Year);
    const valueKey = headers[headers.length - 1];
    if (obj[valueKey] != null) obj[valueKey] = Number(obj[valueKey]);
    rows.push(obj);
  }
  return rows;
}

function splitCSVLine(line) {
  const res = [];
  let cur = '', inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i+1] === '"') { cur += '"'; i++; }
      else { inQuotes = !inQuotes; }
    } else if (ch === ',' && !inQuotes) {
      res.push(cur); cur = '';
    } else {
      cur += ch;
    }
  }
  res.push(cur);
  return res;
}

function reduceLatestByCode(rows, codeKey) {
  const latest = {};
  const valueKey = Object.keys(rows[0] || {}).slice(-1)[0];
  for (const r of rows) {
    const code = r[codeKey];
    const year = Number(r.Year);
    const val = r[valueKey];
    if (!code || val == null || Number.isNaN(val)) continue;
    const prev = latest[code];
    if (!prev || year > prev.year) latest[code] = { value: Number(val), year };
  }
  const map = {};
  for (const [k, v] of Object.entries(latest)) map[k] = v.value;
  return map;
}
