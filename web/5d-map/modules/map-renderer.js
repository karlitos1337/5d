export function initMap(elId = 'map', center = [20, 0], zoom = 2) {
  const map = L.map(elId, { worldCopyJump: true }).setView(center, zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(map);
  return map;
}

export function addLayer(map, layer) {
  if (layer) layer.addTo(map);
}

export function removeLayer(map, layer) {
  if (layer) map.removeLayer(layer);
}
