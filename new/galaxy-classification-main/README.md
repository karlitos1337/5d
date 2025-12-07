# AstroML: Klassifikation und Helligkeitsvorhersage von Himmelsobjekten

Dieses Projekt beschäftigt sich mit der Anwendung von Machine Learning und Deep Learning auf reale astronomische Bilddaten. Ziel ist es, Himmelsobjekte wie Galaxien oder Sterne anhand von Bilddaten (z. B. vom Sloan Digital Sky Survey, SDSS) zu klassifizieren oder ihre Helligkeit bzw. Entfernung vorherzusagen.

## 🔭 Motivation

Als Physikstudent mit Schwerpunkt in Astroteilchenphysik möchte ich mit diesem Projekt zeigen, wie moderne Machine-Learning-Methoden in der astrophysikalischen Datenanalyse eingesetzt werden können. Dieses Projekt dient zugleich als Teil meines öffentlichen Portfolios.

## 🧠 Technologien

- Python 3.x
- Jupyter Notebooks
- NumPy, Pandas, Matplotlib
- scikit-learn
- TensorFlow / PyTorch (für CNNs)
- Astroquery (zum Zugriff auf SDSS-Daten)
- ggf. OpenCV oder PIL zur Bildbearbeitung

## 📊 Projektziele

- Datenbeschaffung und Vorverarbeitung astronomischer Bilddaten (SDSS)
- Aufbau von CNN-Modellen zur Klassifikation von Galaxientypen (z. B. Spiral vs. elliptisch)
- Regressionsmodelle zur Vorhersage der scheinbaren Helligkeit
- Optional: Clustering-Analyse zur Gruppierung ähnlicher Objekte
- Evaluation mit realen Metriken (Accuracy, MSE, etc.)

## 📁 Projektstruktur (geplant)
AstroML/
├── data/ # Bilddaten (nicht im Repo enthalten, siehe Hinweise)
├── notebooks/ # Jupyter Notebooks für Datenanalyse und Modelltraining
├── models/ # Gespeicherte Modelle (optional .gitignored)
├── src/ # Python-Skripte und Hilfsfunktionen
├── .gitignore
├── LICENSE
├── README.md


## 🔗 Datenquelle

Die Bilddaten stammen vom [Sloan Digital Sky Survey (SDSS)](https://www.sdss.org/). Für den Zugriff wird das Python-Paket `astroquery` verwendet.

⚠️ Hinweis: Rohdaten (Bilder) sind aus Speichergründen nicht Teil des Repositories. Ein Download-Skript wird bereitgestellt.

## 🚧 Status

Das Projekt befindet sich in der Aufbauphase. Erste Notebooks zur Datenbeschaffung und Modellvorbereitung sind in Arbeit.

## 📜 Lizenz

Dieses Projekt steht unter der [MIT License](LICENSE).

## 👤 Autor

Andreas Pfeffer
https://github.com/Andreas-pf
---

*Dieses Repository ist Teil meines persönlichen Portfolios zur Demonstration praktischer Programmierkenntnisse im Bereich Machine Learning und Astrophysik.*

