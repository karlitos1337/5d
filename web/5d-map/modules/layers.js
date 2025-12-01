import { createSchoolPopup, createIMPPopup, initRadarChart } from './popups.js';

// Einfache Beispielpunkte (lat, lng, intensität 0..1) für Offline‑Heatmap
const SAMPLE_POINTS = [
  [52.52, 13.405, 0.35],   // Berlin
  [48.8566, 2.3522, 0.55], // Paris
  [51.5074, -0.1278, 0.45],// London
  [40.7128, -74.0060, 0.6],// NYC
  [35.6895, 139.6917, 0.5] // Tokio
];

export function createHeatmapLayer(pointsMaybe) {
  // Wenn bereits fertige Punkte (lat,lng,intensity) übergeben wurden, nutze diese
  const points = Array.isArray(pointsMaybe) && Array.isArray(pointsMaybe[0])
    ? pointsMaybe
    : SAMPLE_POINTS;
  return L.heatLayer(points, {
    radius: 25,
    blur: 15,
    maxZoom: 17,
    gradient: {
      0.0: '#22C55E',
      0.5: '#E8814A',
      1.0: '#C0152F'
    }
  });
}

export function createSchoolMarkers(schools = []) {
  const group = L.layerGroup();
  for (const s of schools) {
    const html = getIconForType(s.type);
    const icon = L.divIcon({ className: `school-marker school-marker--${s.type||'na'}`, html, iconSize: [20,20] });
    if (typeof s.lat === 'number' && typeof s.lng === 'number') {
      const m = L.marker([s.lat, s.lng], { icon }).bindPopup(createSchoolPopup(s));
      group.addLayer(m);
    }
  }
  return group;
}

export function createIMPLayer(data) {
  const { worldGeoJSON, impByISO3 } = data || {};
  if (!worldGeoJSON || !worldGeoJSON.features || !impByISO3) {
    console.warn('IMP‑Layer: GeoJSON oder Scores fehlen.');
    return L.layerGroup();
  }

  const scale = (v) => {
    // Farbskala grün→gelb→rot für [0,1]
    if (v == null) return '#cccccc';
    if (v < 0.33) return '#22C55E';
    if (v < 0.66) return '#E8B84A';
    return '#C0152F';
  };

  const layer = L.geoJSON(worldGeoJSON, {
    style: (feature) => {
      const iso3 = feature?.properties?.ISO_A3 || feature?.id;
      const info = impByISO3[iso3];
      const v = info?.score;
      return {
        color: '#333',
        weight: 0.6,
        fillColor: scale(v),
        fillOpacity: v == null ? 0.15 : 0.7,
      };
    },
    onEachFeature: (feature, layer) => {
      const iso3 = feature?.properties?.ISO_A3 || feature?.id;
      const info = impByISO3[iso3];
      layer.bindPopup(createIMPPopup(feature, info));
      layer.on('popupopen', () => {
        if (info?.dims) initRadarChart(iso3, info.dims);
      });
      layer.on('mouseover', function () { this.setStyle({ weight: 1.2 }); });
      layer.on('mouseout', function () { this.setStyle({ weight: 0.6 }); });
    }
  });

  return layer;
}

export function createTimeHeatmapLayer(data, year) {
  const { countries, depressionSeries, dropoutSeries } = data || {};
  if (!countries || !Array.isArray(countries) || !depressionSeries || !dropoutSeries) {
    return L.layerGroup();
  }
  const points = [];
  for (const c of countries) {
    const iso3 = c.iso3; const lat = Number(c.lat); const lng = Number(c.lng);
    if (!iso3 || Number.isNaN(lat) || Number.isNaN(lng)) continue;
    const depVal = depressionSeries[iso3]?.[year];
    const drpVal = dropoutSeries[iso3]?.[year];
    if (depVal == null && drpVal == null) continue;
    const vals = [];
    if (typeof depVal === 'number') vals.push(depVal);
    if (typeof drpVal === 'number') vals.push(drpVal);
    if (!vals.length) continue;
    const intensity = Math.max(0, Math.min(1, (vals.reduce((a,b)=>a+b,0)/vals.length) / 100));
    points.push([lat, lng, intensity]);
  }
  return L.heatLayer(points, {
    radius: 25,
    blur: 15,
    maxZoom: 17,
    gradient: {
      0.0: '#22C55E',
      0.5: '#E8814A',
      1.0: '#C0152F'
    }
  });
}

export function createIMPLegendControl() {
  const grades = [0, 0.33, 0.66, 1.0];
  const getColor = (v) => (v < 0.33 ? '#22C55E' : v < 0.66 ? '#E8B84A' : '#C0152F');
  const control = L.control({ position: 'bottomright' });
  control.onAdd = function () {
    const div = L.DomUtil.create('div', 'legend');
    div.innerHTML = '<strong>IMP‑Score</strong><br>';
    for (let i = 0; i < grades.length - 1; i++) {
      const from = grades[i], to = grades[i + 1];
      const color = getColor((from + to) / 2);
      const label = `${Math.round(from * 100)}–${Math.round(to * 100)}%`;
      const row = document.createElement('div');
      row.innerHTML = `<i style="background:${color}"></i> ${label}`;
      div.appendChild(row);
    }
    const note = document.createElement('div');
    note.className = 'legend-note';
    note.innerHTML = '<small>WGI normalisiert, höher ist besser.</small>';
    div.appendChild(note);
    return div;
  };
  return control;
}

function getIconForType(type) {
  const icons = { sudbury: '🟢', waldorf: '🔵', 'folk-high': '🟡', tokkatsu: '🟣' };
  return icons[type] || '⚪';
}
