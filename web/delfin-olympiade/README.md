# Delfinitiv.. nicht! Hihihi

Ein Delfin-Sprungspiel, inspiriert von *Dolphin Olympics*, komplett in einer HTML-Datei
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
  (Perfekt / Sauber / Bauchklatscher); alle Trickpunkte landen in der Kombo-Kasse und werden mal Multiplikator (bis ×10)
  ausgezahlt, wenn 15 s im Wasser kein neuer Trick kommt; ein Bauchklatscher beendet die Kombo und die Kasse ist weg
- Wellenreiten: mit S / ↓ beim Auftauchen auf der Oberfläche surfen, loslassen = Absprung
- Jede Kombo-Stufe macht den Delfin im Wasser schneller (Tempo ×1 bis ×5,23). Oberhalb von 30 m wächst die
  Höhe exponentiell: Wolken, Weltraum, ISS, Mond, Planeten, Voyager 1, Proxima Centauri, Milchstraße, Andromeda,
  Virgo-Haufen, Rand des Universums und dahinter das Multiversum mit dem Urdelfin (schaltet den Kosmos-Skin frei)
- Fotoshooting am Flugzeug (11 km, nur im Wettkampf): Blitzlicht-Marathon in Zeitlupe, der Delfin posiert in Anzug,
  Fliege und Sonnenbrille, danach friert das Bild als Magazin-Cover „Killer-Shot“ ein (+5.000)
- Weltraum-Modus ab der Kármán-Linie: keine Erd-Schwerkraft, je höher desto schneller (Tempo-Anzeige bis zur
  vielfachen Lichtgeschwindigkeit); der Delfin dreht wie in der Luft Saltos, die Nase lenkt sanft zur Seite; nach dem Mond folgen Mars, Jupiter, Saturn, Neptun und Pluto, zwischen Mond und Pluto in echten Abstandsverhältnissen zueinander (lineare Strecke), danach geht es raus aus dem Sonnensystem; hinter jedem Planeten bzw. jeder Wegmarke liegt eine waagerechte Sternenbahn, die man erst ansteuern muss:
  mit ↓ beim Kreuzen einrasten, seitlich grinden (Schwung lädt, Punkte), loslassen = Boost nach oben; der Schwung läuft nach Zeit ab; ist er alle, fällt der Delfin mit normaler Luft-Physik in einer Parabel zurück, ohne künstliches Abbremsen; nur wer ganz oben ankommt,
  wird per Wurmloch nach Hause geportet. Hardcore (Menü/Pause): Schwung läuft doppelt so schnell leer, kein Portal,
  Wegmarken ×2 Punkte
- Kosmos-Kombo: Wegmarken multiplizieren die Punkte des laufenden Sprungs (Flugzeug ×2, Mond ×5, Mars ×10, Jupiter ×25,
  Saturn ×50, Neptun ×100, Pluto ×150 … bis Urdelfin ×100.000); es zählt der höchste im Sprung, jede Wiederholung derselben
  Wegmarke in einer Runde 1 % weniger; nur bei sauberer Landung zählt er auch für die Sprungpunkte
- Zwischen-Szenen im All (einmal pro Runde, überspringbar): Auf dem Mond schleicht sich der Delfin pfeifend an,
  wirft die Flagge der Menschen weg und steckt die von „Delfine United“ hin; auf dem Mars sonnt er sich auf der
  Liege; am Saturn surft er auf den Ringen
- Zwischen-Szenen und Fotoshooting lassen sich im Hauptmenü und im Pausenmenü abschalten (Punkte gibt es trotzdem)
- Rammbock: ab Mond-Tempo (glühender Delfin) werden Quallen, Kraken und Anglerfische zerstört; ein Bauchklatscher mit
  hohem Tempo oder nach der Rückkehr aus dem All löst eine Schockwelle aus (Bauchplatscher-Bombe)
- Tiefsee: am Grund nur ein Krake (Tintenwolke) und ein Anglerfisch mit Leuchtköder
- Lagune ohne Wände: Wer seitlich rausschwimmt oder -springt, kommt auf der anderen Seite wieder rein
- Fischschwärme durchkreuzen: 5.000 Punkte (in derselben Kombo jedes weitere Mal 1 % weniger) und
  ein Bonusverstärker auf alle Punkte (+1 %, jedes weitere Mal 1 % weniger als zuvor)
- Wenige Ringe (6, in der Ring-Jagd 10), jeder gibt einmalig einen Speed-Boost (+35 %, Gold +45 %); Gold-Ringe hoch oben, Möwen-Stups, Himmelssterne, Fischschwärme, Perlenmuscheln, Quallen
- 6 Power-ups: Turbo, Doppelte Punkte, Magnet, Zeitlupe, Leichtflug, Rakete
- Tag-Nacht-Zyklus mit Sonne, Mond, Sternen, Leuchtturm und Biolumineszenz bei Nacht
- Grafik: Parallax-Hügel, Wolken, Lichtstrahlen unter Wasser, Wellen mit Ripples, Spritz- und
  Blasenpartikel, Bewegungsspur, Kamera-Zoom bei hohen Sprüngen
- Über 30 Erfolge, davon 9 geheime (im Menü als ??? bis zum Freischalten), 5 Delfin-Skins (Gold und Neon freischaltbar), Rekorde im `localStorage`
