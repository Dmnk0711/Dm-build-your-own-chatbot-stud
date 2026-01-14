# Präsentation: RAG-basiert LoL Patch-Chatbot

**Projektstatus:** Core-System läuft & Automatisierung (Scraper) implementiert.

## Folie 1: Vision & Ziel

* **Problem:** Patchnotes sind lang, unübersichtlich und ändern sich alle 2 Wochen.
* **Lösung:** Ein lokaler KI-Chatbot, der die neuesten Daten selbstständig aus dem Web lädt und präzise Fragen dazu beantwortet.
* **Besonderheit:** 100% lokal (Datenschutz & keine Kosten) durch Nutzung von Ollama.

---

## Folie 2: Die 3 Säulen der Architektur

Das System ist in drei logische Module unterteilt:

1. **Der Scraper (Die Datenquelle):**
* Extrahiert automatisch Informationen von der offiziellen Riot Games Webseite.
* Nutzt `BeautifulSoup`, um HTML-Strukturen (H3/H4-Tags) in saubere JSON-Daten zu verwandeln.


2. **Der Ingest (Das Gehirn):**
* Liest die JSON-Dateien ein.
* Verwandelt Text in Vektoren (Zahlenformate) und speichert sie in der `ChromaDB`.


3. **Das Frontend (Die Schnittstelle):**
* `Streamlit`-Weboberfläche für den Benutzer.
* RAG-Logik: Sucht erst in der Datenbank und lässt dann das LLM (Ollama) antworten.



---

## Folie 3: Aktueller Funktionsstand ("Was kann er?")

* **Web-Scraping:** Erkennt Champions und ordnet ihnen ihre spezifischen Fähigkeiten (Passiv, Q, W, E, R) hierarchisch zu.
* **Automatisierte Ablage:** Speichert Daten im korrekten Pfad (`app/src/data/patch_scraped.json`).
* **Intelligente Suche:** Dank Vektordatenbank findet der Bot Informationen auch dann, wenn die Frage nicht exakt die gleichen Wörter wie der Patchnote-Text nutzt.
* **Lokale LLM-Anbindung:** Nutzt die Power von Modellen wie Llama3 oder Mistral über die Ollama-Schnittstelle.

---

## Folie 4: Technische Highlights (Dein Lernfortschritt)

* **State-Machine-Logik:** Der Scraper "merkt" sich den aktuellen Champion, während er die Unterpunkte liest.
* **Fehlertoleranz:** Einsatz von Absoluten Pfaden (`r"C:\Users\..."`), um Windows-Pfadprobleme zu umgehen.
* **Vektorisierung:** Verstehen, dass Daten nicht nur gespeichert, sondern für die KI "auffindbar" gemacht werden müssen.

---

## Folie 5: Demo-Szenario (Beispiel)

1. **Input:** User startet Scraper für Patch 14.2/26.1.
2. **Verarbeitung:** Scraper findet "Kayle" -> "Passiv – Göttlicher Aufstieg" -> "Änderung XY".
3. **Abfrage:** User fragt: "Wie wurde Kayles Passiv verändert?"
4. **Bot-Antwort:** "Bei Kayles Passiv wurde das Angriffstempo pro Steigerung von X auf Y angepasst."

---

## Folie 6: Roadmap (Wie geht es weiter?)

* **Vollautomatisierung:** Der Bot prüft beim Start selbstständig, ob ein neuer Patch online ist.
* **Multi-Source:** Scraping von weiteren Quellen (z.B. LoL-Wiki für Hintergrundinfos).
* **UI-Polishing:** Den Chatverlauf schöner gestalten und Champion-Bilder einblenden.

---

### Dein nächster Schritt (wenn du wieder einsteigst):

Wir müssen als Nächstes die **"Verbindungsschraube"** festziehen:
Das Ingest-Skript muss so eingestellt werden, dass es immer die Datei nimmt, die der Scraper gerade frisch erzeugt hat.

**Soll ich dir zum Abschluss noch eine kurze "Checkliste für den Neustart" schreiben, damit du morgen weißt, welche 3 Befehle du nacheinander drücken musst?**

----------------------------------------------------------
Was fehlt : 

Loggen der Antworten
Einbinden Riot API für fachwörter
vorgehen logger :
Dashboard-Komponente: Ein separates Streamlit-Tab, das nur für Admins sichtbar ist und Diagramme (Plotly/Streamlit Charts) über die meistgesuchten Champions anzeigt.

Feedback-Loop: Ein "War das hilfreich?"-Button direkt unter der Bot-Antwort. Das ist der wertvollste Datenpunkt für die Evaluation der RAG-Qualität.

Anonymisierung: Ein Modul, das sicherstellt, dass keine personenbezogenen Daten geloggt werden (DSGVO-Konformität).

A. Datenerfassung (Logging)
Du erstellst eine einfache Datenbank (oder eine CSV/JSON-Datei), in die bei jeder Anfrage folgende Felder geschrieben werden:

Timestamp: Wann wurde gefragt?

User Query: Was war die exakte Frage?

Extracted Entity: Welcher Champion/Item wurde erkannt (z. B. "Akshan")?

Sentiment/Feedback: Ein Daumen-hoch/runter Button in Streamlit.

Response Time: Wie lange hat Ollama gebraucht?

B. Auswertung (Analytics)
Mit diesen Daten kannst du folgende Fragen beantworten:

Trend-Analyse: Welche Champions werden nach einem Patch am häufigsten abgefragt? (Meta-Interesse)

Knowledge Gaps: Wo gibt der Bot die Antwort "Dazu liegen mir keine Informationen vor"? (Hier fehlen Daten im Scraper).

User Intent: Suchen Nutzer eher nach Zahlen (Stats) oder nach Erklärungen (Mechaniken)?