import { fetchAllData, clearCache } from './modules/api-fetcher.js';
import { initMap, addLayer, removeLayer } from './modules/map-renderer.js';
import { createHeatmapLayer, createSchoolMarkers, createIMPLayer, createIMPLegendControl, createTimeHeatmapLayer, createValidationRingLayer, createSourcesLayer, createValidationLegendControl } from './modules/layers.js';
import { debounce } from './modules/utils.js';

let map;
let activeLayer = null;
let cachedData = {};
let legendCtl = null;
let selectedYear = null;
let infoEl, infoTextEl;
let validationFilter = 'all';
let validationCountEl;

function setLoading(isLoading, message = 'Lade Daten...') {
  document.body.classList.toggle('loading', !!isLoading);
  const msgEl = document.querySelector('.loading-spinner p');
  if (msgEl) msgEl.textContent = message;
}

function updateLastUpdateTime() {
  const el = document.getElementById('last-update');
  if (el) el.textContent = new Date().toLocaleString('de-DE');
}

function activateLayer(layerName) {
  if (activeLayer) removeLayer(map, activeLayer);
  if (legendCtl) { try { map.removeControl(legendCtl); } catch {} legendCtl = null; }
  const timeCtl = document.getElementById('time-controls');
  if (timeCtl) timeCtl.style.display = layerName === 'time' ? 'block' : 'none';
  if (infoEl && infoTextEl) {
    const infoMap = {
      'status-quo': 'Heatmap: Mittelwert aus Depression/Dropout (%). Daten: OWID/World Bank.',
      'schools': 'Marker: Alternative Schulen (lokale Daten).',
      'imp': 'IMP‑Choropleth: A×IM×R×SP×Au; WGI‑Normalisierung.',
      'validation': 'Validierung (Ringe): extern verifizierte Länder. Daten: validation.json.',
      'sources': 'Quellen (Marker): Anzahl/Kategorien pro Land aus validation.json.',
      'time': 'Zeitreise: historischer Heatmap‑Modus mit Jahres‑Slider.'
    };
    const txt = infoMap[layerName] || '—';
    infoTextEl.textContent = txt;
    infoEl.style.display = 'block';
  }
  document.querySelectorAll('.btn').forEach(btn => btn.classList.remove('btn--primary'));
  const btn = document.getElementById(`layer-${layerName}`);
  if (btn) btn.classList.add('btn--primary');

  switch (layerName) {
    case 'status-quo':
      activeLayer = createHeatmapLayer(cachedData.heatmapPoints);
      break;
    case 'schools':
      activeLayer = createSchoolMarkers(cachedData.schools || []);
      break;
    case 'imp':
      activeLayer = createIMPLayer(cachedData);
      legendCtl = createIMPLegendControl();
      legendCtl.addTo(map);
      break;
    case 'validation':
      activeLayer = createValidationRingLayer(cachedData, validationFilter);
      legendCtl = createValidationLegendControl();
      legendCtl.addTo(map);
      break;
    case 'sources':
      activeLayer = createSourcesLayer(cachedData);
      break;
    case 'time':
      if (!selectedYear) {
        selectedYear = (cachedData.seriesYears && cachedData.seriesYears[cachedData.seriesYears.length - 1]) || new Date().getFullYear();
      }
      updateYearSliderRange();
      activeLayer = createTimeHeatmapLayer(cachedData, selectedYear);
      break;
    default:
      activeLayer = null;
  }
  if (activeLayer) addLayer(map, activeLayer);
}

function updateYearSliderRange() {
  const slider = document.getElementById('year-slider');
  const label = document.getElementById('year-label');
  if (!slider || !label || !Array.isArray(cachedData.seriesYears) || !cachedData.seriesYears.length) return;
  slider.min = String(cachedData.seriesYears[0]);
  slider.max = String(cachedData.seriesYears[cachedData.seriesYears.length - 1]);
  if (!selectedYear) selectedYear = cachedData.seriesYears[cachedData.seriesYears.length - 1];
  slider.value = String(selectedYear);
  label.textContent = String(selectedYear);
}

async function refreshData() {
  setLoading(true);
  try {
    cachedData = await fetchAllData();
    updateLastUpdateTime();
    const current = document.querySelector('.btn.btn--primary');
    const name = current ? current.id.replace('layer-', '') : 'status-quo';
    activateLayer(name);
  } catch (e) {
    console.error('Refresh error:', e);
  } finally {
    setLoading(false);
  }
}

async function init() {
  map = initMap('map', [20, 0], 2);
  infoEl = document.getElementById('layer-info');
  infoTextEl = document.getElementById('layer-info-text');
  validationCountEl = document.getElementById('validation-count');
  setLoading(true);
  try {
    cachedData = await fetchAllData();
  } catch (e) {
    console.warn('Daten konnten nicht geladen werden, verwende Fallbacks.', e);
  } finally {
    setLoading(false);
  }
  updateLastUpdateTime();
  activateLayer('status-quo');
  updateValidationCount();

  document.getElementById('layer-status-quo')?.addEventListener('click', () => activateLayer('status-quo'));
  document.getElementById('reset-cache')?.addEventListener('click', () => { clearCache(); refreshData(); });
  document.getElementById('layer-schools')?.addEventListener('click', () => activateLayer('schools'));
  document.getElementById('layer-imp')?.addEventListener('click', () => activateLayer('imp'));
  document.getElementById('layer-validation')?.addEventListener('click', () => activateLayer('validation'));
  document.getElementById('export-validation-csv')?.addEventListener('click', () => exportValidationCSV());
  document.getElementById('export-validation-json')?.addEventListener('click', () => exportValidationJSON());
  document.getElementById('layer-sources')?.addEventListener('click', () => activateLayer('sources'));
  document.getElementById('layer-time')?.addEventListener('click', () => activateLayer('time'));

  const updateTimeLayer = debounce((year) => {
    if (document.getElementById('layer-time')?.classList.contains('btn--primary')) {
      if (activeLayer) removeLayer(map, activeLayer);
      activeLayer = createTimeHeatmapLayer(cachedData, year);
      if (activeLayer) addLayer(map, activeLayer);
    }
  }, 50);

  const yearSlider = document.getElementById('year-slider');
  yearSlider?.addEventListener('input', (e) => {
    selectedYear = Number(e.target.value);
    const label = document.getElementById('year-label');
    if (label) label.textContent = String(selectedYear);
    updateTimeLayer(selectedYear);
  });

  // Auto-Refresh jede Stunde
  setInterval(refreshData, 3600000);

  // Listen for validation filter changes from legend
  window.addEventListener('validation-filter', (e) => {
    validationFilter = e.detail?.status || 'all';
    updateValidationCount();
    if (document.getElementById('layer-validation')?.classList.contains('btn--primary')) {
      if (activeLayer) removeLayer(map, activeLayer);
      activeLayer = createValidationRingLayer(cachedData, validationFilter);
      if (activeLayer) addLayer(map, activeLayer);
    }
  });
}

function updateValidationCount() {
  if (!validationCountEl) return;
  const items = Array.isArray(cachedData.validationItems) ? cachedData.validationItems : [];
  const filtered = validationFilter && validationFilter !== 'all'
    ? items.filter(it => String(it.status) === String(validationFilter))
    : items;
  const label = validationFilter === 'all' ? 'alle' : validationFilter;
  validationCountEl.textContent = '';
  validationCountEl.appendChild(document.createTextNode('Filter: '));
  const strong1 = document.createElement('strong');
  strong1.textContent = label;
  validationCountEl.appendChild(strong1);
  validationCountEl.appendChild(document.createTextNode(' · Einträge: '));
  const strong2 = document.createElement('strong');
  strong2.textContent = filtered.length;
  validationCountEl.appendChild(strong2);
}

function exportValidationCSV() {
  const items = Array.isArray(cachedData.validationItems) ? cachedData.validationItems : [];
  const filtered = validationFilter && validationFilter !== 'all'
    ? items.filter(it => String(it.status) === String(validationFilter))
    : items.slice();
  const headers = ['id','name','domain','status','source','iso3'];
  const rows = [headers.join(',')];
  for (const it of filtered) {
    const vals = headers.map(h => {
      const v = it?.[h] ?? '';
      const s = String(v).replace(/"/g, '""');
      return /[",\n]/.test(s) ? `"${s}"` : s;
    });
    rows.push(vals.join(','));
  }
  const csv = rows.join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const suffix = validationFilter || 'all';
  a.href = url;
  a.download = `validation_${suffix}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function exportValidationJSON() {
  const items = Array.isArray(cachedData.validationItems) ? cachedData.validationItems : [];
  const filtered = validationFilter && validationFilter !== 'all'
    ? items.filter(it => String(it.status) === String(validationFilter))
    : items.slice();
  const blob = new Blob([JSON.stringify(filtered, null, 2)], { type: 'application/json;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const suffix = validationFilter || 'all';
  a.href = url;
  a.download = `validation_${suffix}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

init();
