# Pilotstudie: Teilnahme, Freigabe, Export

Die Teilnahme-Seite (`web/5d-map/teilnahme/`, live unter https://karlitos1337.github.io/5d/teilnahme/) wertet im Browser aus. Wer möchte, spendet am Ende pseudonym an eine Supabase-Datenbank in Frankfurt. Ins öffentliche Repository kommt nur, was du vorher freigegeben hast.

**Stand:** Solange `SUPABASE_URL` und `SUPABASE_ANON_KEY` in der Seite leer sind, ist die Spende abgeschaltet. Die Seite sagt das dann auch so.

## Ablauf im Überblick

1. Teilnehmende füllen die Seite aus und sehen sofort ihre Auswertung.
2. Wer spenden will, stimmt ausdrücklich zu und klickt „Antworten pseudonym spenden“. Gesendet werden nur Zahlen, Altersgruppe (freiwillig), das Ergebnis der Aufmerksamkeitsfrage und ein zufälliger Teilnahme-Code. Es gibt keine E-Mail-Adresse und keine Uhrzeit.
3. Die Zeile landet in Supabase mit `approved = false`.
4. **Deine Freigabe:** Im Supabase-Dashboard (Table Editor → `pilot_submissions`) setzt du bei plausiblen Zeilen `approved` auf `true`. Offensichtlichen Unsinn löschst du.
5. Die Action **„Pilotdaten exportieren“** schreibt alle freigegebenen Zeilen nach `08_experimente_validierung/data/pilot_responses.csv`. Sie läuft automatisch alle drei Tage oder sofort über Actions → Run workflow.

## Einrichtung (einmalig, ca. 15 Minuten)

1. **Projekt anlegen:** Auf supabase.com ein neues Projekt erstellen, Region **Central EU (Frankfurt)**.
2. **Tabelle anlegen:** Im Dashboard unter *SQL Editor* den Inhalt von `supabase/pilot_schema.sql` einfügen und ausführen. Danach darf der öffentliche Schlüssel nur noch einfügen, nicht lesen, ändern oder löschen. Die Freigabe kann er auch nicht selbst setzen.
3. **Vertrag zur Auftragsverarbeitung (DPA):** Bei Supabase in den Organisationseinstellungen abschließen. Erst danach stimmt der Satz auf der Seite, dass ein solcher Vertrag besteht. **Ohne DPA die Spende nicht einschalten.**
4. **GitHub-Secrets:** Unter Repository → Settings → Secrets and variables → Actions anlegen:
   - `SUPABASE_URL`: die Projekt-URL (`https://….supabase.co`)
   - `SUPABASE_SERVICE_KEY`: den **service_role**-Schlüssel. Er ist geheim und gehört nie in den Code.
5. **Seite einschalten:** In `web/5d-map/teilnahme/index.html` `SUPABASE_URL` und `SUPABASE_ANON_KEY` eintragen. Der **anon**-Schlüssel ist öffentlich und darf ins Repository. Dann committen. Nach dem Pages-Deployment ist die Spende aktiv.
6. **Testen:** Einmal selbst teilnehmen und spenden, die Zeile im Dashboard prüfen, freigeben, den Export starten und den Test danach wieder löschen.

## Pausieren vermeiden

Supabase pausiert Gratis-Projekte nach etwa einer Woche ohne Nutzung. Der Export-Workflow läuft alle drei Tage und fragt dabei die Datenbank ab, das hält das Projekt aktiv. Ist es trotzdem pausiert, reaktivierst du es im Dashboard, spätestens bevor der Aufruf, z. B. bei SurveyCircle, rausgeht. Hinweis: GitHub stoppt geplante Workflows in Repositories, in denen 60 Tage lang nichts passiert ist.

## Widerruf

Schickt jemand seinen Teilnahme-Code, löschst du die Zeile im Supabase-Dashboard. Beim nächsten Export verschwindet sie auch aus der CSV, denn die Datei wird jedes Mal komplett neu geschrieben.

## Löschfristen (so steht es auf der Seite)

- Nicht freigegebene Spenden: löschen
- Supabase-Datenbank: nach Ende der Pilotphase leeren, spätestens 12 Monate nach der Spende
- Öffentlicher Datensatz: nur freigegebene, anonyme Zahlenreihen

## Hinweise

- Die Datenschutztexte sind ein sorgfältiger Entwurf, keine Rechtsberatung.
- In der Spalte `aufmerksamkeit_ok` steht 0, wenn die Aufmerksamkeitsfrage falsch beantwortet wurde. Diese Datensätze werden laut Präregistrierung bei der Auswertung ausgeschlossen, nicht beim Export.
- Die Daten passen zu H1, H2 und #572 (IRT). `cluster_analysis.py` (#571) erwartet ein anderes Format und muss dafür angepasst werden.
- `scripts/pilot_import.py` enthält die gemeinsamen Prüfregeln und kann lokal einzelne alte Spenden-Codes (`5DP1.…`) einlesen.
