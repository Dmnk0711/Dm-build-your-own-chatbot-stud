import json
import requests
import chromadb
import os

# --- PFADE ---
# Die JSON-Datei, die dein Scraper gerade erstellt hat
PATCH_FILE = r"C:\Users\Dominik\Dm-build-your-own-chatbot-stud\Chatbot League of Legends\chatbot_task\app\src\data\patch_scraped.json"

# Der Pfad, wo die Datenbank liegen soll (zwei Ebenen über dem data-Ordner oder absolut)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = r"C:\Users\Dominik\Dm-build-your-own-chatbot-stud\Chatbot League of Legends\chatbot_task\app\src\chroma_db"

# --- KONFIGURATION ---
COLLECTION_NAME = "patchnotes"
OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"
EMBED_MODEL = "nomic-embed-text"

def ingest_data():
    print("--- INGESTION START ---")
    
    # 1. Datenbank initialisieren
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Alte Daten löschen, um sauber neu zu starten
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("Alte Datenbank-Collection gelöscht.")
    except:
        pass
    
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # 2. JSON laden
    if not os.path.exists(PATCH_FILE):
        print(f"FEHLER: Datei nicht gefunden unter {PATCH_FILE}")
        return

    with open(PATCH_FILE, "r", encoding="utf-8") as f:
        patch_data = json.load(f)

    patch_version = patch_data.get("patch", "26.01")
    content = patch_data.get("content", {})

    # 3. Durch Kategorien und Einträge loopen
    for category, entries in content.items():
        print(f"\nVerarbeite Kategorie: {category}")
        
        for name, details in entries.items():
            # Kontext-Text zusammenbauen
            
            clean_details = details[:4000]
            full_text = f"CHAMPION NAME: {name} {name} {name}\nKATEGORIE: {category}\nDETAILS: {clean_details}"
            
            print(f"  -> Erstelle Vektor für: {name}")

            try:
                # Embedding von Ollama anfordern
                response = requests.post(
                    OLLAMA_EMBED_URL,
                    json={"model": EMBED_MODEL, "input": full_text},
                    timeout=60
                )
                response.raise_for_status()
                embedding = response.json()["embeddings"][0]

                # In ChromaDB speichern
                collection.add(
                    documents=[full_text],
                    metadatas=[{"category": category, "name": name, "patch": patch_version}],
                    ids=[f"{category}_{name}_{patch_version}".replace(" ", "_")],
                    embeddings=[embedding]
                )
            except Exception as e:
                print(f"    ❌ Fehler bei {name}: {e}")

    print("\n--- INGESTION ERFOLGREICH BEENDET ---")
    print(f"Anzahl der Dokumente in der DB: {collection.count()}")

if __name__ == "__main__":
    ingest_data()