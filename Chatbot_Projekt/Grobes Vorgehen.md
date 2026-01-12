Patchnotes können nicht nicht alsAPI abgerufen werden aber von der Webseite als HTML / Markdown / JSON runtergeladen werden
-> Patchnotes Scraper
Patches erst mal manuel anlegen:
JSON
patch_14_2.json
....
{
    "patch": "14.2",
    "champions": {
        "Ahri": [
            "Q Damage increast from 400 to 500"
            "Cooldown reduced by 1 secc"
        ]
    }
}
---> vlt vektorisieren ??

--------------------------------------------

Datenverarbeitung
Patch erscheint
->
Scraper lädt Patchnotes
->
Parser extrahiert Champions / Items / Systems
->
Speicherung (DB)
->
LLM nutzt Daten für Antwort

-----------------------------------------------

Logik kann entweder über prompt ober über Vektor DB gemacht werden---> Patchnotes vectorisieren und damit arbeiten


Patchnotes-> Vektor DB ( Chroma oder FAISS )
User frägt und Bot sucht relevante Patchnotes
diese werden dann LLM als Kontext gegeben

-------- ODER über PROMPT ----------------
Prompt schreiben ----> Wichtig
Bsp.
You are a League of Legends patch analysis assistant.
Use ONLY the provided patch data.
Explain changes in a simple and player-friendly way.
If the champion is not mentioned, say so clearly.

.... im code dann

context = get_patch_notes("Ahri")
prompt = f"""
Patch context:
{context}

User question:
{quetion}
"""

----------------------------------------------


Was wollen wir loggen ? also für RIOT interessant ??
Champion
Role
Builds
Patch
Intent (Change/Buff/Nerf/Meta)
Timestamp

--> Beispiel Datenbank
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY,
    champion TEXT,
    intent TEXT,
    path TEXT,
    timestamp DATETIME
);
--> Beispiel Chat:
log_interactions(
    champion="Ahri",
    intent="buff_explanation",
    patch="14.2"
)

-----------------------------------------------



Docker aufbau kann sein:
services:
    chatbot:
        build: .
        depends_on:
         - ollama
    ollama:
        image: ollama/ollama

-------------------------------------------------

Jetzt	LoL-Version
AI_Book.pdf	Patchnotes (JSON / Markdown / HTML)
Buch-Wissen	Champion / Item / System Changes
statische Quelle	versionierte Patches
neutraler Prompt	LoL-Experten-Prompt

-------------------------------------------------