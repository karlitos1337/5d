import { fetchAllData } from './modules/api-fetcher.js';
import { initMap, addLayer, removeLayer } from './modules/map-renderer.js';
import { createHeatmapLayer, createSchoolMarkers, createIMPLayer, createIMPLegendControl } from './modules/layers.js';

let map;
let activeLayer = null;
let cachedData = {};
let legendCtl = null;

function setLoading(isLoading) {
  document.body.classList.toggle('loading', !!isLoading);
}

function updateLastUpdateTime() {
  const el = document.getElementById('last-update');
  if (el) el.textContent = new Date().toLocaleString('de-DE');
}

function activateLayer(layerName) {
  if (activeLayer) removeLayer(map, activeLayer);
  if (legendCtl) { try { map.removeControl(legendCtl); } catch {} legendCtl = null; }
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
    case 'time':
      activeLayer = null; // (kommt später)
      break;
    default:
      activeLayer = null;
  }
  if (activeLayer) addLayer(map, activeLayer);
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
  document.getElementById('layer-time')?.addEventListener('click', () => activateLayer('time'));

  // Auto-Refresh jede Stunde
  setInterval(refreshData, 3600000);
}

init();
