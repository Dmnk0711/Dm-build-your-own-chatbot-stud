import requests
import chromadb
import os

# --- KONFIGURATION ---
OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"
EMBED_MODEL = "nomic-embed-text"

# Wir nutzen deinen absoluten Pfad, um sicherzugehen
CHROMA_PATH = r"C:\Users\Dominik\Dm-build-your-own-chatbot-stud\Chatbot League of Legends\chatbot_task\app\src\chroma_db"


def retrieve_context(question: str, n_results: int = 10):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name="patchnotes")

    # 1. Namen aus der Frage extrahieren (simpel)
    # Wir schauen, ob Wörter in der Frage vorkommen, die als 'name' in der DB existieren
    all_metas = collection.get(include=['metadatas'])['metadatas']
    existing_names = list(set([m['name'] for m in all_metas]))
    
    found_name = None
    for name in existing_names:
        if name.lower() in question.lower():
            found_name = name
            break

    # 2. Embedding für die Vektorsuche erstellen
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={"model": EMBED_MODEL, "input": question},
        timeout=60
    )
    query_emb = response.json()["embeddings"][0]

    # 3. Suche ausführen
    if found_name:
        # Wenn wir einen Namen gefunden haben, filtern wir EXAKT danach
        print(f"DEBUG: Keyword-Treffer gefunden: {found_name}. Filter wird angewendet.")
        results = collection.query(
            query_embeddings=[query_emb],
            n_results=n_results,
            where={"name": found_name} # Das ist der "Hard-Filter"
        )
    else:
        # Falls kein Name erkannt wurde, normale Vektorsuche
        results = collection.query(
            query_embeddings=[query_emb],
            n_results=n_results
        )

    documents = results.get("documents", [[]])[0]
    return "\n\n---\n\n".join(documents)