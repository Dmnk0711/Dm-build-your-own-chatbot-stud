import requests
from chromadb.api import ClientAPI
import chromadb
import os

OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"
EMBED_MODEL = "nomic-embed-text"
CHROMA_HOST_NAME = os.environ.get("CHROMA_HOST_NAME", "localhost")
# Chroma Client (temporär)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = r"C:\Users\Dominik\Dm-build-your-own-chatbot-stud\Chatbot League of Legends\chatbot_task\app\src\chroma_db"
print(f"DEBUG: Retriever sucht Datenbank hier: {CHROMA_PATH}")


client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name="patchnotes")

def retrieve_context(question: str, n_results: int = 3):
    # Frage in Embedding umwandeln
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "input": question
        },
        timeout=60
    )
    response.raise_for_status()
    query_emb = response.json()["embeddings"][0]

    # Ähnliche Dokumente abrufen
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=n_results
    )
    

    # Nur die Texte zurückgeben
    documents = results["documents"][0]  # List of matched patchnote texts
    print(f"--- GEFUNDENER KONTEXT AUS CHROMA: ---\n{documents}\n----------------------------------")
    return " ".join(documents)
