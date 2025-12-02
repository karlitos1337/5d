# 5D-Intelligence Analysis Framework

## Übersicht

Dieses Verzeichnis enthält alle Algorithmen zur **Verarbeitung und Analyse** der 5D-Survey-Daten.

## Komponenten

### 1. Score-Berechnung
- `calculate_5d_scores.py` - Haupt-Algorithmus
- Dimensionsspezifische Scores (normalized 0-1)
- Aggregierter 5D-Intelligence-Score
- Integration mit IMP-Formel

### 2. Clustering
- `cluster_responses.py` - K-Means & DBSCAN
- Segmentierung nach Profilen
- Identifikation von Mustern

### 3. Visualisierung
- `visualize_results.py` - Plotly-Charts
- Radar-Charts für 5D-Profile
- Heatmaps für Korrelationen
- Zeit-Serien (longitudinal)

### 4. Export
- CSV, JSON, BibTeX
- Aggregierte Statistiken
- Anonymisierte Rohdaten

## Verwendung

```python
from analysis import calculate_5d_scores, cluster_responses, visualize_results

# Scores berechnen
profile = calculate_5d_scores.calculate_5d_intelligence_profile(responses)

# Clustering
clusters = cluster_responses.cluster_participants(all_profiles)

# Visualisierung
fig = visualize_results.generate_dimension_radar_chart(profile)
fig.show()
```

## Wissenschaftliche Validierung

- Cronbach's Alpha für interne Konsistenz
- Test-Retest-Reliabilität
- Konstruktvalidität
