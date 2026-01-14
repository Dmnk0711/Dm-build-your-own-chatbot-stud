# LoL Patch Notes AI Chatbot (RAG-System)

Ein intelligentes Assistenz-System, das aktuelle League of Legends Patchnotes analysiert und Fragen dazu präzise beantwortet. Das System nutzt **RAG (Retrieval Augmented Generation)**, um Halluzinationen zu vermeiden und ausschließlich auf Basis verifizierter Wiki-Daten zu antworten.

##  Features

* **Automatisches Wiki-Scraping:** Extrahiert strukturierte Daten (Champions, Items, Game-Mechanics) direkt aus dem League of Legends Wiki.
* **Vektor-Datenbank (ChromaDB):** Speichert Patch-Informationen als hochdimensionale Vektoren für semantische Suche.
* **Hybrid-Retriever:** Kombiniert Keyword-Filtering (für exakte Champion-Zuordnung) mit Vektor-Ähnlichkeit (für inhaltliche Relevanz).
* **Lokale LLM-Inferenz:** Nutzt **Ollama** mit dem **Llama 3** Modell für maximale Datensicherheit und lokale Ausführung.
* **Streamlit UI:** Ein benutzerfreundliches Chat-Interface zur Interaktion mit den Patch-Daten.

---

##  System-Architektur (C4-Modell Ansatz)

Das System folgt einer klassischen RAG-Pipeline:

1. **Data Ingestion:** Der Scraper wandelt HTML-Wiki-Daten in ein strukturiertes JSON um.
2. **Embedding & Storage:** Das Ingest-Skript erzeugt Embeddings via `nomic-embed-text` und speichert sie in ChromaDB.
3. **Retrieval:** Bei einer User-Anfrage sucht der Retriever nach den Top-K relevantesten Dokumenten.
4. **Augmentation & Generation:** Das LLM erhält die Frage zusammen mit dem gefundenen Kontext und generiert eine Antwort auf Deutsch.

---

##  Installation & Setup

### Voraussetzungen

* Python 3.10+
* [Ollama](https://ollama.ai/) installiert und aktiv.
* Benötigte Modelle in Ollama:
```bash
ollama pull llama3
ollama pull nomic-embed-text

```



### Python-Umgebung einrichten

```bash
pip install streamlit chromadb requests beautifulsoup4

```

### Projekt starten

1. **Scraping:** Patch-HTML in den Ordner legen und `scraper.py` ausführen.
2. **Ingest:** Datenbank befüllen:
```bash
python src/rag/ingest.py

```


3. **UI starten:**
```bash
streamlit run main.py

```



---

##  Projektstruktur

* `app/src/data/`: Enthält die HTML-Quelldaten und die extrahierte `patch_scraped.json`.
* `app/src/rag/`:
* `retriever.py`: Logik für die Hybrid-Suche (Vektor + Keyword).
* `llm.py`: Schnittstelle zu Ollama und Prompt-Engineering.
* `ingest.py`: Skript zur Initialisierung der ChromaDB.


* `app/src/chroma_db/`: Die persistente Vektor-Datenbank.
* `main.py`: Streamlit Applikation.

---

##  Analyse des Nutzerverhaltens (Ausblick)

Für die zukünftige Auswertung des Nutzerverhaltens ist folgende Erweiterung geplant:

* **Logging-Komponente:** Speicherung jeder `user_query` und der zugehörigen `extracted_entity` in einer SQL-Datenbank.
* **Metriken:**
* *Popularität:* Welche Champions/Items werden am häufigsten angefragt?
* *Genauigkeit:* Feedback-Loop über "Helpful/Not Helpful" Buttons in der UI.
* *Coverage:* Identifikation von Fragen, zu denen kein Kontext gefunden wurde.



---

##  Regeln für das LLM (System Prompt)

Der Bot ist durch strikte Regeln instruiert:

1. Nutze **ausschließlich** den bereitgestellten Kontext.
2. Erfinde keine Werte (keine Halluzinationen).
3. Antworte kurz, präzise und auf Deutsch.
4. Falls keine Info vorliegt, kommuniziere dies transparent.

---

**Entwickelt als Teil eines Chatbot-Studienprojekts 2026.**

---