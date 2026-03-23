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
    const strong = document.createElement('strong');
    strong.textContent = 'IMP‑Score';
    div.appendChild(strong);
    div.appendChild(document.createElement('br'));

    for (let i = 0; i < grades.length - 1; i++) {
      const from = grades[i], to = grades[i + 1];
      const color = getColor((from + to) / 2);
      const label = `${Math.round(from * 100)}–${Math.round(to * 100)}%`;
      const row = document.createElement('div');

      const icon = document.createElement('i');
      icon.style.background = color;
      row.appendChild(icon);
      row.appendChild(document.createTextNode(` ${label}`));

      div.appendChild(row);
    }
    const note = document.createElement('div');
    note.className = 'legend-note';
    const small = document.createElement('small');
    small.textContent = 'WGI normalisiert, höher ist besser.';
    note.appendChild(small);
    div.appendChild(note);
    return div;
  };
  return control;
}

export function createValidationLegendControl() {
  const control = L.control({ position: 'bottomright' });
  control.onAdd = function () {
    const div = L.DomUtil.create('div', 'legend');
    const strong = document.createElement('strong');
    strong.textContent = 'Validierung';
    div.appendChild(strong);
    div.appendChild(document.createElement('br'));

    const rows = [
      { color: '#22C55E', label: 'Grün: extern validiert', status: 'green' },
      { color: '#E8B84A', label: 'Gelb: Community/Wikipedia', status: 'yellow' },
      { color: '#C0152F', label: 'Rot: keine Validierung', status: 'red' },
      { color: '#2dd4bf', label: 'Alle', status: 'all' }
    ];
    rows.forEach(r => {
      const row = document.createElement('div');

      const icon = document.createElement('i');
      icon.style.background = r.color;
      row.appendChild(icon);
      row.appendChild(document.createTextNode(` ${r.label}`));

      row.style.cursor = 'pointer';
      row.title = 'Klicken zum Filtern';
      row.addEventListener('click', () => {
        const ev = new CustomEvent('validation-filter', { detail: { status: r.status } });
        window.dispatchEvent(ev);
      });
      div.appendChild(row);
    });
    const note = document.createElement('div');
    note.className = 'legend-note';
    const small = document.createElement('small');
    small.textContent = 'Daten: validation.json';
    note.appendChild(small);
    div.appendChild(note);
    return div;
  };
  return control;
}

function getIconForType(type) {
  const icons = { sudbury: '🟢', waldorf: '🔵', 'folk-high': '🟡', tokkatsu: '🟣' };
  return icons[type] || '⚪';
}

// Validierungsring: zeichnet einen dezenten Ring um Länder mit verifizierten Daten
export function createValidationRingLayer(data, filterStatus) {
  const { countries, validatedISO3, validationItems } = data || {};
  const group = L.layerGroup();
  if (!Array.isArray(countries)) return group;
  let isoSet = new Set(Array.isArray(validatedISO3) ? validatedISO3 : []);
  const metaByISO3 = {};
  if (Array.isArray(validationItems)) {
    for (const it of validationItems) {
      if (it && it.iso3) {
        metaByISO3[it.iso3] = {
          status: String(it.status || ''),
          source: String(it.source || '')
        };
      }
    }
  }
  if (filterStatus && filterStatus !== 'all' && Array.isArray(validationItems)) {
    isoSet = new Set(validationItems.filter(it => String(it.status) === String(filterStatus) && it.iso3).map(it => it.iso3));
  }
  for (const c of countries) {
    const { iso3, lat, lng } = c || {};
    if (!iso3 || typeof lat !== 'number' || typeof lng !== 'number') continue;
    if (!isoSet.has(iso3)) continue;
    const meta = metaByISO3[iso3] || {};
    const statusLabel = meta.status === 'green' ? 'extern' : meta.status === 'yellow' ? 'community' : meta.status === 'red' ? 'keine' : '—';
    const src = meta.source || 'validation.json';
    const circle = L.circle([lat, lng], {
      radius: 300000, // 300 km
      color: '#2dd4bf',
      weight: 2,
      fill: false,
      opacity: 0.9
    }).bindTooltip(`✔️ ${c.name || iso3}<br/><small>Status: ${statusLabel}, Quelle: ${src}</small>`, { permanent: false });
    group.addLayer(circle);
  }
  return group;
}

// Quellen-Layer: zeigt Abdeckung/Zahl der Quellen pro Land als kleine Marker
export function createSourcesLayer(data) {
  const { countries, sourcesByISO3 } = data || {};
  const group = L.layerGroup();
  if (!Array.isArray(countries) || !sourcesByISO3) return group;
  for (const c of countries) {
    const { iso3, lat, lng } = c || {};
    if (!iso3 || typeof lat !== 'number' || typeof lng !== 'number') continue;
    const info = sourcesByISO3[iso3];
    const count = Number(info?.count || 0);
    const categoriesArr = Array.isArray(info?.categories) ? info.categories : [];
    const categories = categoriesArr.length ? categoriesArr.join(', ') : '—';
    const color = count >= 10 ? '#22C55E' : count >= 3 ? '#E8B84A' : '#C0152F';
    const m = L.circleMarker([lat, lng], {
      radius: Math.max(4, Math.min(12, count)),
      color,
      fillColor: color,
      fillOpacity: 0.7,
      weight: 1
    }).bindPopup(`<b>${c.name || iso3}</b><br/>Quellen: ${count}<br/>Kategorien: ${categoriesArr.length}<br/><small>${categories}</small>`);
    group.addLayer(m);
  }
  return group;
}
