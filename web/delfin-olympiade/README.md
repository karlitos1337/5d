# Delfin-Olympiade

Ein Delfin-Sprungspiel im Stil von *Dolphin Olympics*, komplett in einer HTML-Datei
(Canvas 2D + WebAudio, keine Abhängigkeiten außer Google Fonts).

**Starten:** `index.html` im Browser öffnen. Läuft auch, wenn man den Inhalt in einen
Online-Playground (z. B. Google AI Studio „Build“, CodePen, JSFiddle) einfügt.

## Steuerung
| Taste | Aktion |
|---|---|
| ↑ / W | Schwimmen |
| ← → / A D | Lenken, in der Luft Salto |
| ↓ / S | Schraube in der Luft |
| Leertaste | Turbo (verbraucht Energie) |
| P / Esc, M | Pause, Ton an/aus |

Touch-Buttons erscheinen automatisch auf Handys, Gamepads werden ebenfalls unterstützt.

## Features
- 3 Modi: Wettkampf (2 min), Ring-Jagd (15 Ringe auf Zeit), Freies Spiel
- Tricks: Saltos vorwärts/rückwärts (bis Mehrfach), Schrauben, Kombis; Bewertung der Landung
  (Perfekt / Sauber / Bauchklatscher) und Kombo-Multiplikator bis ×10
- Jede Kombo-Stufe macht den Delfin im Wasser schneller (Tempo ×1 bis ×5,23). Oberhalb von 30 m wächst die
  Höhe exponentiell: Wolken, Weltraum, ISS, Mond, Planeten, Voyager 1, Proxima Centauri, Milchstraße, Andromeda,
  Virgo-Haufen, Rand des Universums und dahinter das Multiversum mit dem Urdelfin (schaltet den Kosmos-Skin frei)
- Fotoshooting am Flugzeug (11 km, nur im Wettkampf): Blitzlicht-Marathon in Zeitlupe, der Delfin posiert in Anzug,
  Fliege und Sonnenbrille, danach friert das Bild als Magazin-Cover „Killer-Shot“ ein (+5.000)
- Zwischen-Szenen im All (einmal pro Runde, überspringbar): Auf dem Mond schleicht sich der Delfin pfeifend an,
  wirft die Flagge der Menschen weg und steckt die von „Delfine United“ hin; auf dem Mars sonnt er sich auf der
  Liege; am Saturn surft er auf den Ringen
- Tiefsee: wenige Quallen erst in der Tiefe, am Grund Kraken (Tintenwolke) und Anglerfische mit Leuchtköder
- Lagune ohne Wände: Wer seitlich rausschwimmt oder -springt, kommt auf der anderen Seite wieder rein
- Fischschwärme durchkreuzen: 5.000 Punkte (in derselben Kombo jedes weitere Mal 1 % weniger) und
  ein Bonusverstärker auf alle Punkte (+1 %, jedes weitere Mal 1 % weniger als zuvor)
- Ringe (Gold-Ringe hoch oben), Möwen-Stups, Himmelssterne, Fischschwärme, Perlenmuscheln, Quallen
- 6 Power-ups: Turbo, Doppelte Punkte, Magnet, Zeitlupe, Leichtflug, Rakete
- Tag-Nacht-Zyklus mit Sonne, Mond, Sternen, Leuchtturm und Biolumineszenz bei Nacht
- Grafik: Parallax-Hügel, Wolken, Lichtstrahlen unter Wasser, Wellen mit Ripples, Spritz- und
  Blasenpartikel, Bewegungsspur, Kamera-Zoom bei hohen Sprüngen
- 14 Erfolge, 5 Delfin-Skins (Gold und Neon freischaltbar), Rekorde im `localStorage`
