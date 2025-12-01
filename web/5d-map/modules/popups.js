export function createSchoolPopup(school) {
  const safe = (v) => (v == null ? '' : String(v));
  return `
    <div class="school-popup">
      <h3>${safe(school.name)}</h3>
      <p><strong>Typ:</strong> ${safe(school.type)}</p>
      <p><strong>Gegründet:</strong> ${safe(school.founded)}</p>
      <p><strong>Schüler:</strong> ${safe(school.students)}</p>
      <hr>
      <p><strong>Outcomes:</strong></p>
      <ul>
        <li>College-Rate: ${safe(school?.outcomes?.college)}%</li>
        <li>Zufriedenheit: ${safe(school?.outcomes?.satisfaction)}%</li>
      </ul>
      ${school.detailsLink ? `<a href="${safe(school.detailsLink)}" target="_blank" rel="noreferrer">Mehr erfahren →</a>` : ''}
    </div>
  `;
}

export function createIMPPopup(feature, info) {
  const name = feature?.properties?.ADMIN || feature?.properties?.NAME || 'Unbekannt';
  const iso3 = feature?.properties?.ISO_A3 || feature?.id || '—';
  if (!info) {
    return `<div><strong>${name}</strong><br><small>${iso3}</small><br><em>Keine IMP‑Daten vorhanden.</em></div>`;
  }

  const pct = (x) => (x == null ? '—' : `${(x * 100).toFixed(1)}%`);
  const dep = info?.sources?.dep;
  const drp = info?.sources?.drp;
  const wgiRL = info?.sources?.wgi_rl; // original [-2.5,2.5]
  const wgiVA = info?.sources?.wgi_va;
  const wgiGE = info?.sources?.wgi_ge;
  const dims = info?.dims || {};
  const baselineFlag = info?.sources?.baseline ? ' (Baseline aktiviert)' : '';

  // Formel: IMP_raw = A × IM × R × SP × Au, clamp[0,1]
  // A = 1 − Dropout, IM = 1 − Depression, R=SP=Au=0.5 (Platzhalter)
  return `
    <div class="imp-popup">
      <h3>${name}</h3>
      <p><small>${iso3}</small></p>
      <p><strong>IMP:</strong> ${pct(info.score)}${baselineFlag}</p>
      <hr>
      <p><strong>Dimensionen</strong></p>
      <ul>
        <li>A (Zugang): ${pct(dims.A)} ${drp != null ? `(Dropout: ${Number(drp).toFixed(1)}%)` : ''}</li>
        <li>IM (Mental Health): ${pct(dims.IM)} ${dep != null ? `(Depression: ${Number(dep).toFixed(1)}%)` : ''}</li>
        <li>R (Rule of Law): ${pct(dims.R)} ${wgiRL != null ? `(WGI RL.EST: ${Number(wgiRL).toFixed(2)})` : ''}</li>
        <li>SP (Voice & Accountability): ${pct(dims.SP)} ${wgiVA != null ? `(WGI VA.EST: ${Number(wgiVA).toFixed(2)})` : ''}</li>
        <li>Au (Gov. Effectiveness): ${pct(dims.Au)} ${wgiGE != null ? `(WGI GE.EST: ${Number(wgiGE).toFixed(2)})` : ''}</li>
      </ul>
      <canvas id="imp-radar-${iso3}" width="220" height="220"></canvas>
      <p><em>Formel:</em> IMP = A × IM × R × SP × Au;<br>
      <small>Skala Radar: 1–100. WGI normalisiert: (x+2.5)/5×100. Baseline füllt fehlende Werte.</small></p>
    </div>
  `;
}

export function initRadarChart(iso3, dims) {
  try {
    const el = document.getElementById(`imp-radar-${iso3}`);
    if (!el || typeof Chart === 'undefined') return;
    const toPct = (x) => (x == null ? 50 : Math.max(0, Math.min(100, x * 100)));
    const data = [toPct(dims.A), toPct(dims.IM), toPct(dims.R), toPct(dims.SP), toPct(dims.Au)];
    new Chart(el, {
      type: 'radar',
      data: {
        labels: ['A', 'IM', 'R', 'SP', 'Au'],
        datasets: [{
          data,
          backgroundColor: 'rgba(33, 128, 141, 0.2)',
          borderColor: 'rgba(33, 128, 141, 1)',
          borderWidth: 2,
          pointBackgroundColor: 'rgba(33, 128, 141, 1)'
        }]
      },
      options: {
        responsive: true,
        scales: { r: { min: 0, max: 100, ticks: { stepSize: 20 } } },
        plugins: { legend: { display: false } }
      }
    });
  } catch (e) {
    console.warn('Radar init failed:', e);
  }
}
