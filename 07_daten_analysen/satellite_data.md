# 🛰️ Satellite Data – Open Satellite Imagery (Satellite Map Space)

**Dimension**: 07_daten_analysen  
**Cross-Reference**: web/5d-map (Geographic Visualization)  
**Datum**: 2025-12-03  
**Status**: Sprint 3 - Medium-Priority (Optional)

---

## 📊 Übersicht

**URL**: https://satellitemap.space/  
**Score**: 5/10  
**Status**: Optional (Nische: Satellite Imagery)

---

## 🟢 Satellite Map Space

### Features
- **Open Satellite Imagery:** Sentinel-2 (EU), Landsat (NASA), MODIS (NASA)
- **Free Access:** Keine API Keys, keine Registration
- **Use Cases:**
  - **Agriculture:** Crop monitoring (NDVI: Normalized Difference Vegetation Index)
  - **Urban Planning:** City growth tracking
  - **Climate:** Deforestation, glacier melting, wildfires
  - **Research:** Remote Sensing, GIS (Geographic Information Systems)

### Technical Specs
- **Resolution:** 10m (Sentinel-2), 30m (Landsat), 250m (MODIS)
- **Update Frequency:** Daily (MODIS), 5 days (Sentinel-2), 16 days (Landsat)
- **Bands:** Visible (RGB), Near-Infrared (NIR), Shortwave Infrared (SWIR)

---

## 🎓 Integration in 5D-Framework

### 7. Datenanalysen
- **Satellite Data Sources:** Sentinel-2, Landsat, MODIS als primäre Quellen
- **Use Cases:** Vegetation Patterns (Ecology), Urban Growth (Governance)

### web/5d-map
- **Integration:** Satellite overlays für 5d-map (z.B. Vegetation Health per Country)
- **Example:** NDVI-Overlay → zeigt Ressourcenqualität pro Land

---

## 🔄 Vergleich: Satellite Map Space vs. Google Earth

| Kriterium | Satellite Map Space | Google Earth |
|-----------|---------------------|--------------|
| **Kosten** | $0 | $0 (Consumer), $399/Jahr (Pro) |
| **Resolution** | 10m (Sentinel-2) | 1m (commercial satellites) |
| **Update Frequency** | 5 days (Sentinel-2) | Monthly (varies by region) |
| **Open Data** | ✅ Sentinel-2, Landsat (Public Domain) | ❌ Proprietary (Maxar, DigitalGlobe) |
| **API** | ✅ Free (Copernicus, NASA) | ✅/❌ Free (Consumer), Paid (Commercial) |

**Empfehlung:** Satellite Map Space (Open Data, Research) → Google Earth (Consumer, High Resolution)

---

## 📚 BibTeX-Referenzen

```bibtex
@misc{satellitemapspace2025,
  title = {Satellite Map Space: Open Satellite Imagery Platform},
  author = {{Satellite Map Space Team}},
  year = {2025},
  howpublished = {\url{https://satellitemap.space/}},
  note = {Free access to Sentinel-2, Landsat, MODIS satellite imagery}
}

@misc{sentinel22025,
  title = {Sentinel-2: EU Earth Observation Satellite},
  author = {{European Space Agency}},
  year = {2025},
  howpublished = {\url{https://sentinel.esa.int/web/sentinel/missions/sentinel-2}},
  note = {10m resolution, 5-day revisit, 13 spectral bands, open data (Copernicus)}
}

@misc{landsat2025,
  title = {Landsat: NASA Earth Observation Program},
  author = {{NASA}},
  year = {2025},
  howpublished = {\url{https://landsat.gsfc.nasa.gov/}},
  note = {30m resolution, 16-day revisit, 50+ years of data, public domain}
}
```

---

## 🔗 Cross-Reference Map

| Thema | Verweis | Begründung |
|-------|---------|------------|
| **5D-Map** | `web/5d-map/` | Satellite overlays (NDVI, Urban Growth) |
| **Ecology** | `06_synthesen_kompilationen/vegetation_patterns.md` | Remote Sensing für Vegetationsmuster |
| **Data Sources** | `07_daten_analysen/data_sources.md` | Sentinel-2, Landsat als primäre Quellen |

---

## 🚀 Action Items

- [x] Satellite Map Space dokumentiert
- [ ] BibTeX Batch 11 (satellitemapspace2025, sentinel22025, landsat2025) - Q1 2026
- [ ] 5d-map Satellite Overlay Prototype (NDVI per Country) - Q2 2026
- [ ] Vegetation Patterns File (`06_synthesen_kompilationen/vegetation_patterns.md`) - Q2 2026

---

**Last Updated:** 2025-12-03  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)  
**License:** CC BY 4.0
