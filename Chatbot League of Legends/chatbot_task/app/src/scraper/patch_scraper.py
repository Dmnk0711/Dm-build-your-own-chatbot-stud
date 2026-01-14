import os
from bs4 import BeautifulSoup
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(SCRIPT_DIR, "patch.html")
SAVE_PATH = r"C:\Users\Dominik\Dm-build-your-own-chatbot-stud\Chatbot League of Legends\chatbot_task\app\src\data\patch_scraped.json"

def clean_text(text):
    # Entfernt [edit] und bereinigt Leerzeichen
    cleaned = re.sub(r'\[.*?\]', '', text)
    # Entfernt mehrfache Leerzeichen, die durch Icons entstehen können
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def scrape_league_wiki():
    print("--- WIKI-SPECIFIC SCAN START ---")
    
    if not os.path.exists(HTML_FILE):
        print(f"Fehler: {HTML_FILE} nicht gefunden.")
        return

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    patch_data = {"patch": "26.01", "content": {}}
    current_category = "Allgemein"
    current_entry = None
    
    # Wir suchen h3 (Kategorien), dt (Champions/Items) und ul (Änderungen)
    for tag in soup.find_all(['h3', 'dt', 'ul', 'p']):
        
        # 1. Kategorie (z.B. Champions, Items)
        if tag.name == 'h3':
            name = clean_text(tag.get_text())
            if name in ["Contents", "Navigation", "References"]: continue
            current_category = name
            if current_category not in patch_data["content"]:
                patch_data["content"][current_category] = {}
            current_entry = None 
            print(f"\nKategorie: {current_category}")

        # 2. Champion / Item Name (dt)
        elif tag.name == 'dt':
            entry_name = clean_text(tag.get_text())
            if entry_name:
                current_entry = entry_name
                patch_data["content"][current_category][current_entry] = ""
                print(f"  -> {current_entry}")

        # 3. Die eigentlichen Änderungen (ul oder p)
        elif tag.name in ['ul', 'p'] and current_entry:
            txt = tag.get_text(" ", strip=True)
            if txt:
                existing = patch_data["content"][current_category][current_entry]
                # Wir hängen den Text an den Champion an
                patch_data["content"][current_category][current_entry] = (existing + " " + txt).strip()

    # Speichern
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(patch_data, f, indent=4, ensure_ascii=False)

    # Erfolgskontrolle
    count = sum(len(entries) for entries in patch_data["content"].values())
    print(f"\n--- FERTIG ---")
    print(f"Einträge gefunden: {count}")

if __name__ == "__main__":
    scrape_league_wiki()