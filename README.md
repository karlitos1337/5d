# 5D Intelligenz System

Dieses Repository sammelt die Formeln, Einsichten und Strukturen eines 5D‑Verständnisses von Intelligenz, Bildung, Ethik und menschlichem Potenzial.[web:3][web:6]
## IMP-Score: Berechnungsmethode

Basis-Formel (multiplikativ):

```
IMP = A × IM × R × SP × Au
```

Beispiel (5D-Modellschule):

- A (Autonomie) = 0.95
- IM (Motivation) = 0.88
- R (Resilienz) = 0.82
- SP (Partizipation) = 0.79
- Au (Authentizität) = 0.91

Ergebnis: IMP = 0.95 × 0.88 × 0.82 × 0.79 × 0.91 ≈ 0.52

Hinweis: Falls ein adjustierter Score (z. B. 0.77) verwendet wird, ist dies eine
gewichtete/normierte Variante. Details siehe `models/imp.py` (`calculate_imp_verified`).

Vergleich:

- Dänemark (geschätzt): IMP ≈ 0.45 (basierend auf 7,8% Dropout, OECD 2023)
- 5D-Modell (theoretisch): IMP ≈ 0.52 (+16% vs. DK)
## Nutzung

Im Tab „Manifeste“ ist die transparente IMP-Berechnung integriert (multiplikativ, gewichtet, normalisiert) sowie Filter/Suche und externe Referenzen.
## Changelog

Siehe `CHANGELOG.md` für eine Liste der Änderungen und Versionen.
# 5d
# 5D Intelligenz System

Dieses Repository sammelt die Formeln, Einsichten und Strukturen eines 5D‑Verständnisses von Intelligenz, Bildung, Ethik und menschlichem Potenzial.[web:3][web:6]

# 5D-Intelligenz: Dezentrale Bildung & Potenzialentfaltung

**5D = 5 Dimensionale Intelligenz**  
Kein statischer IQ-Trait, sondern emergenter Prozess der Organism-Environment-Kopplung. Anwendbar auf zwanglose/natürliche Systeme und Begrenzungen der Wahrnehmung.[attached_file:ae85ab2d][file:13]

## Definition [file:13][file:14]
1D: Reptiliengehirn – Reflexiv
2D: Limbisch – Bewusst lokal
3D: PFC+Polyvagal – Reflektiv, multiperspektivisch
4D: Netzwerk – Emergent, dezentral
5D: Meta-Intelligenz – Selbstreflexion, Transformation

## Mission

- Intelligenz weg vom IQ-Test hin zu Interesse, Bewusstheit und Verantwortung verschieben.[web:3]
- Bildung als Aktivierung von interessenbasiertem Potenzial statt als Anpassung an starre Systeme denken.[web:12]
- Menschen Werkzeuge geben, um sich selbst, andere und Systeme klarer zu sehen und würdevoll zu handeln.

## Kernideen

- Mensch = interessensorientiertes Potenzialwesen, nicht IQ‑Wert.[web:12]
- Interesse aktiviert Intelligenz (neurobiologisch), nicht umgekehrt.[web:4]
- Ethisches Minimum: Solange du niemandem schadest und niemandem aktiv im Weg stehst, ist dein Handeln grundsätzlich okay.[web:6]
- Liebe beginnt dort, wo etwas/jemand wichtiger wird als das eigene Ego – ohne Selbstvernichtung.[web:5]

## Struktur

- GRID.md – Überblick über alle Formeln mit Kurzbeschreibung.
- formeln/001-050-systemkritik.md – System, Institutionen, Macht.
- formeln/051-100-familie-liebe.md – Familie, Mutter/Vater, Kind, Beziehung.
- formeln/101-150-bildung-revolution.md – Bildung, Potenzial, 5D‑Intelligenz.
- formeln/151-157-ethik-freiheit.md – Ethik, Freiheit, Nicht‑Schädigung.

## Nutzung

- Lesen: als Reflexionswerkzeug, nicht als Dogma.
- Erweitern: eigene Formeln ergänzen, umbenennen, präzisieren.
- Anwenden: auf Schule, Therapie, Elternschaft, Organisationsdesign.
BEgrenzt: IQ misst 2D (logisch-verbal)
5D: Erweitert auf 5 Dimensionen
ZWANGLOSE Systeme aktivieren ALLE Ebenen automatisch




## Kernkomponenten IMP (multiplikativ) [file:13]
- **A**utonomie × **IM**otivation × **R**esilienz × **SP**artizipation × **Au**thentizität = Potenzial

## Anwendungen
- **Bildung**: Schulabbrecherquote 7,8% → 2% (Dänemark-Modell + Learning-by-Doing)
- **Natürliche Systeme**: Autopoiesis (Maturana), Emergenz (Kauffman)
- **Wahrnehmung**: Polyvagal-Theorie (Porges) – Ventral Vagal als Denkvoraussetzung

## Struktur
- [GRID.md](GRID.md) – 158 Formeln
- [formeln/](formeln/) – Themenbündel
- [manifest/](manifest/) – Volltexte (MEGA-5D etc.)



Autor: Karl  
Status: laufende Arbeit  
Stand: 27.11.2025

## Quickstart (Tools & Apps)

- Voraussetzungen: Python 3.10+

- Installation:

```bash
pip install -r requirements_extended.txt
```

- Komplettlauf (Extraktion → Research → GitHub → Dashboard):

```bash
chmod +x RUN_ALL.sh
./RUN_ALL.sh
```

### PrivateGPT Integration (lokales RAG über 5d-Daten)

- Voraussetzungen:
	- Abhängigkeiten von `private-gpt-main` installiert (z. B. im Dev-Container: `python -m pip install -e private-gpt-main`)
	- Optional lokales LLM (Ollama oder LlamaCPP) gemäß `private-gpt-main/settings-local.yaml`
- Python-Version-Hinweis:
	- PrivateGPT verlangt Python 3.11.x. Bevorzugter Weg: `.venv-pgpt` via Setup‑Skript:
	```bash
	bash integrations/setup_pgpt_venv.sh
	# danach
	PGPT_PROFILES=5d-minimal bash integrations/private_gpt_5d.sh all
	```
	- Manuell (Alternative):
	```bash
	sudo apt update && sudo apt install -y python3.11 python3.11-venv
	python3.11 -m venv .venv-pgpt
	. .venv-pgpt/bin/activate
	python -m pip install -U pip
	python -m pip install fastapi uvicorn injector python-multipart "gradio==4.44.0" \
	  chromadb "llama-index-core>=0.13,<0.15" llama-index-embeddings-huggingface llama-index-vector-stores-chroma \
	  sentence-transformers einops
	python -m pip install -e private-gpt-main
	```
- Ingest + Server starten:
	```bash
	PGPT_PROFILES=local bash integrations/private_gpt_5d.sh all
	# Oder getrennt:
	PGPT_PROFILES=local bash integrations/private_gpt_5d.sh ingest
	PGPT_PROFILES=local bash integrations/private_gpt_5d.sh serve
	```
- Standard-URL: `http://localhost:8001` (UI aktiviert). Das Skript setzt `PGPT_PROFILES=local` und aktiviert lokale Ingestion.

- Einzelne Komponenten:
	- Extractor: `python 5d_extractor.py`
	- Research: `python 5d_research_scraper.py`
	- GitHub Explorer: `python 5d_github_api.py`
	- Dashboard: `streamlit run 5d_dashboard.py`

- Game of Life (Streamlit Demo):

```bash
streamlit run gol_streamlit.py
```

	- Optionaler Export (GIF/MP4):
		- Zusätzliche Pakete sind bereits in `requirements_extended.txt` enthalten (`imageio`, `imageio-ffmpeg`).
		- System-FFmpeg kann für MP4 nötig sein:

```bash
sudo apt update && sudo apt install -y ffmpeg
```

- Zwanglosigkeits‑Modell (Streamlit):

```bash
streamlit run zwi_streamlit.py
```

- Autopoietische Klasse (Streamlit):

```bash
streamlit run autopoietic_streamlit.py
```

- Partizipations‑Netzwerke (Streamlit):

```bash
streamlit run partnet_streamlit.py
```

- Discord‑Bot (separat, benötigt Token):

```bash
export DISCORD_TOKEN=... 
python 5d_discord_bot.py
```

Hinweise:
- JSON‑Schemas und deutschsprachige Keys bitte beibehalten (Dashboard/Bot erwarten sie).
- Optional: Externe Repos unter `external/` via Submodule einbinden und mit `merge_external_solutions.py` mergen.
- Optional: Ein Mapping von Resonanz → IMP kann in `mapping_resonance_imp.md` dokumentiert werden; ein separates Skript kann daraus nicht‑invasiv Vorschläge generieren.