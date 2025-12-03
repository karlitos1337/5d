import { fetchAllData } from './modules/api-fetcher.js';
import { initMap, addLayer, removeLayer } from './modules/map-renderer.js';
import { createHeatmapLayer, createSchoolMarkers, createIMPLayer, createIMPLegendControl, createTimeHeatmapLayer, createValidationRingLayer, createSourcesLayer } from './modules/layers.js';

let map;
let activeLayer = null;
let cachedData = {};
let legendCtl = null;
let selectedYear = null;

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
      activeLayer = createValidationRingLayer(cachedData);
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

  document.getElementById('layer-status-quo')?.addEventListener('click', () => activateLayer('status-quo'));
  document.getElementById('layer-schools')?.addEventListener('click', () => activateLayer('schools'));
  document.getElementById('layer-imp')?.addEventListener('click', () => activateLayer('imp'));
  document.getElementById('layer-validation')?.addEventListener('click', () => activateLayer('validation'));
  document.getElementById('layer-sources')?.addEventListener('click', () => activateLayer('sources'));
  document.getElementById('layer-time')?.addEventListener('click', () => activateLayer('time'));

  const yearSlider = document.getElementById('year-slider');
  yearSlider?.addEventListener('input', (e) => {
    selectedYear = Number(e.target.value);
    const label = document.getElementById('year-label');
    if (label) label.textContent = String(selectedYear);
    if (document.getElementById('layer-time')?.classList.contains('btn--primary')) {
      if (activeLayer) removeLayer(map, activeLayer);
      activeLayer = createTimeHeatmapLayer(cachedData, selectedYear);
      if (activeLayer) addLayer(map, activeLayer);
    }
  });

  // Auto-Refresh jede Stunde
  setInterval(refreshData, 3600000);
}

init();
