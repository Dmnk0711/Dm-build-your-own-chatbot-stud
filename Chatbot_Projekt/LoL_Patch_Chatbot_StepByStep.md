
# League of Legends Patch Chatbot – Schritt-für-Schritt Anleitung

## Ziel
Umbau eines bestehenden RAG-Chatbots (LangChain + ChromaDB + Ollama) zu einem **League-of-Legends-spezialisierten Patch-Chatbot**, der:
- Patchnotes ausliest
- Champion-Änderungen erklärt
- Nutzerinteraktionen anonymisiert loggt
- einfache Analysen ermöglicht

---

## Voraussetzungen
- Docker & Docker Compose
- Python 3.10+
- Ollama (lokal oder im Docker)
- Bestehender Chatbot-Code (wie bereitgestellt)

---

## Schritt 1 – Projektziel klar definieren
**Was der Bot kann:**
- Fragen zu Champion-Änderungen beantworten
- Nur auf Basis von Patchnotes antworten (RAG)
- Keine Halluzinationen

**Was der Bot nicht kann (bewusst):**
- Kein echtes Live-Scraping
- Keine kommerzielle Nutzung
- Keine personenbezogenen Daten

---

## Schritt 2 – Patchnotes vorbereiten
Erstelle eine Datei z. B.:

`src/data/patch_14_2.json`

```json
{
  "patch": "14.2",
  "champions": {
    "Ahri": [
      "Q damage increased from 40-120 to 45-125",
      "Cooldown reduced by 1 second"
    ],
    "Zed": [
      "R cooldown increased",
      "Base armor reduced"
    ]
  }
}
```

---

## Schritt 3 – PDF-Loader durch Patchnote-Loader ersetzen

### Entfernen
```python
from langchain_community.document_loaders import PyPDFLoader
```

### Neuer Indexer
```python
from langchain_core.documents import Document
import json
from uuid import uuid4

def _index_data_to_vector_db(self):
    with open("src/data/patch_14_2.json") as f:
        patch = json.load(f)

    documents = []
    for champ, changes in patch["champions"].items():
        text = f"Patch {patch['patch']} changes for {champ}:\n"
        text += "\n".join(changes)

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "champion": champ,
                    "patch": patch["patch"],
                    "type": "champion_change"
                }
            )
        )

    self.vector_db.add_documents(
        documents=documents,
        ids=[str(uuid4()) for _ in documents]
    )
```

---

## Schritt 4 – Prompt auf League of Legends anpassen

```text
You are a League of Legends patch analysis assistant.

Rules:
- Use ONLY the provided patch context.
- Explain champion changes in simple, player-friendly language.
- If a champion is not in the context, say:
  "There are no changes for this champion in the selected patch."

Context:
{context}

Question: {question}

Answer in max. 3–4 sentences.
```

---

## Schritt 5 – Champion-Erkennung für Analytics

```python
KNOWN_CHAMPIONS = ["Ahri", "Zed", "Jinx", "Yasuo"]

def extract_champion(question: str):
    for champ in KNOWN_CHAMPIONS:
        if champ.lower() in question.lower():
            return champ
    return "Unknown"
```

Nur für Logging, **nicht** fürs Retrieval.

---

## Schritt 6 – Analytics Logging einbauen

### SQLite Schema
```sql
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    champion TEXT,
    intent TEXT,
    patch TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Logger
```python
def log_interaction(champion, intent, patch):
    ...
```

### Beim Chat-Aufruf
```python
champion = extract_champion(question)

log_interaction(
    champion=champion,
    intent="patch_question",
    patch="14.2"
)
```

---

## Schritt 7 – Analyse-Skript

```python
SELECT champion, COUNT(*)
FROM interactions
GROUP BY champion;
```

Ergebnis:
- Meistgefragte Champions
- Interesse pro Patch

---

## Schritt 8 – Docker & Demo
- Ollama + Chroma + API via docker-compose
- Demo-Fragen vorbereiten:
  - „Was hat sich bei Ahri im Patch 14.2 geändert?“
  - „Wurde Zed generft?“

---

## Schritt 9 – Abgabe & Präsentation (Buzzwords)
- Retrieval-Augmented Generation (RAG)
- Domain-Specific Assistant
- Privacy-by-Design
- Data-Driven Feedback
- Edge AI (lokales LLM)

---

## Optional (nur konzeptionell erwähnen)
- Riot Games API
- Meta-Trend-Erkennung
- Community Feedback Analyse

---

## Fazit
Mit minimalem Umbau wird aus eurem bestehenden Chatbot ein:
**League-of-Legends Patch Analysis Assistant**  
technisch modern, realistisch und uni-tauglich.
