# Pilotstudie: Teilnahme, Freigabe, Einpflegen

So kommen Antworten von der Teilnahme-Seite in den Datensatz, und nur mit deiner Freigabe.

## 1. Teilnehmende

Die Teilnahme-Seite liegt unter `web/5d-map/teilnahme/index.html`. Sie wird mit der 5D-Karte über GitHub Pages veröffentlicht (Workflow `deploy-map.yml`), zum Beispiel unter `https://karlitos1337.github.io/5d/teilnahme/`.

1. Zweck und Datenschutz lesen und zustimmen (ab 18 Jahren).
2. Fragebogen ausfüllen: 25 IMP-Fragen aus der OSF-Präregistrierung, 5 Fragen zur Lebenszufriedenheit (SWLS) und eine Aufmerksamkeitsfrage.
3. Die eigene 5D-Auswertung sofort sehen. Sie wird nur im Browser berechnet, es wird nichts gesendet.
4. Freiwillig: ausdrücklich einwilligen und die Antworten per E-Mail spenden. Die E-Mail enthält einen Code `5DP1.…` ohne Namen, ohne E-Mail-Adresse und ohne Freitext.

## 2. Deine Freigabe

1. E-Mail lesen. Wirkt die Spende ernst gemeint, kopierst du den Code.
2. Auf GitHub: **Actions → Pilotdaten einpflegen → Run workflow**.
3. Code einfügen, Aktion **einpflegen** wählen und starten.
4. Die Action prüft den Code (Version, Wertebereiche, keine Zusatzfelder, kein doppelter Code) und trägt ihn in `08_experimente_validierung/data/pilot_responses.csv` ein. Ein ungültiger Code wird abgelehnt, die Action schlägt dann fehl.
5. Danach die E-Mail löschen. So steht es auf der Seite: spätestens nach 30 Tagen.

Lokal geht es auch: `python scripts/pilot_import.py "5DP1.…"`

## 3. Widerruf

Schreibt eine Person mit ihrem Teilnahme-Code (z. B. `K7Q2-9XPA`), dann startest du dieselbe Action mit diesem Code und der Aktion **entfernen**. Lokal geht das mit `python scripts/pilot_import.py K7Q2-9XPA --remove`.

## Hinweise

- Die Datenschutztexte auf der Seite sind ein sorgfältiger Entwurf, aber keine Rechtsberatung. Vor dem breiten Einsatz sollte sie jemand mit Datenschutzkenntnis gegenlesen.
- Kontaktname und E-Mail-Adresse stehen oben im Skript der Seite (`CONTACT_NAME`, `CONTACT_MAIL`).
- In der Spalte `aufmerksamkeit_ok` steht 0, wenn die Aufmerksamkeitsfrage falsch beantwortet wurde. Diese Datensätze werden laut Präregistrierung bei der Auswertung ausgeschlossen, aber nicht beim Import.
- Die Daten passen zu den Analysen für H1 und H2 sowie zur IRT-Validierung (#572). `cluster_analysis.py` (#571) erwartet ein anderes Format (Zustand, Niveau, Verschränkung, Cluster) und müsste dafür angepasst werden.
