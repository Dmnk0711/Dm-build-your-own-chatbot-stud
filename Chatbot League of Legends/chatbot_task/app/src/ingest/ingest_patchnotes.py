import json
import requests
import chromadb
import os

# --- 1. PFADE AUTOMATISCH ERMITTELN ---
# Ermittelt den Ordner, in dem das Projekt liegt (chatbot_task)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pfad zur JSON-Datei (liegt im Ordner 'data' im Hauptverzeichnis)
PATCH_FILE = os.path.join(BASE_DIR, "data", "patch_14_2.json")

# Pfad zur Datenbank (wird im Hauptverzeichnis erstellt)
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

# --- 2. KONFIGURATION ---
COLLECTION_NAME = "patchnotes"
# WICHTIG: 127.0.0.1 statt 'ollama', da wir lokal auf Windows sind
OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"
EMBED_MODEL = "nomic-embed-text"

print(f"--- DEBUG INFOS ---")
print(f"Projekt-Verzeichnis: {BASE_DIR}")
print(f"Suche JSON-Datei in: {PATCH_FILE}")
print(f"Datenbank wird gespeichert in: {CHROMA_PATH}")
print(f"Nutze Ollama URL: {OLLAMA_EMBED_URL}")
print(f"-------------------\n")

# --- 3. DATENBANK VORBEREITEN ---
# Falls der Ordner nicht existiert, wird er von Chroma automatisch erstellt
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# --- 4. JSON LADEN ---
if not os.path.exists(PATCH_FILE):
    print(f"FEHLER: Die Datei {PATCH_FILE} wurde nicht gefunden!")
else:
    with open(PATCH_FILE, "r", encoding="utf-8") as f:
        patch_data = json.load(f)

    patch_version = patch_data.get("patch", "unknown")
    print(f"Starte Ingestion für Patch {patch_version}...")

    # --- 5. DATEN VERARBEITEN UND SPEICHERN ---
    for champion, changes in patch_data.get("champions", {}).items():
        # Text zusammenbauen
        text = f"Champion: {champion}. Changes: " + " ".join(changes)
        
        print(f"Erstelle Embedding für {champion}...")

        try:
            # Embedding von Ollama holen
            response = requests.post(
                OLLAMA_EMBED_URL,
                json={"model": EMBED_MODEL, "input": text},
                timeout=120
            )
            response.raise_for_status()
            embedding = response.json()["embeddings"][0]

            # In ChromaDB speichern
            collection.add(
                documents=[text],
                metadatas=[{"champion": champion, "patch": patch_version}],
                ids=[f"{champion}_{patch_version}"],
                embeddings=[embedding]
            )
        except Exception as e:
            print(f"Fehler bei Champion {champion}: {e}")

    print(f"\n✅ Ingestion abgeschlossen!")
    print(f"Anzahl der Dokumente in der Datenbank: {collection.count()}")
    print(f"Daten sind jetzt bereit für den Retriever.")