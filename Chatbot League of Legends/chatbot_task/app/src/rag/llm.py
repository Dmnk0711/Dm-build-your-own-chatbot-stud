import requests

# URL auf localhost anpassen für lokale Windows-Installation
OLLAMA_GEN_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3:latest"

def generate_answer(context: str, question: str) -> str:
    print(f"DEBUG: Der übergebene Kontext ist: {context}")
    # Ein "System Prompt" sorgt dafür, dass das Modell sich an die Regeln hält
    prompt = f"""
Du bist ein League of Legends Experte. Deine Aufgabe ist es, die bereitgestellten Patch-Informationen zusammenzufassen.

KONTEXT AUS DER DATENBANK:
{context}

ANWEISUNGEN:
1. Beantworte die Frage basierend auf dem KONTEXT. 
2. Wenn Informationen zu Champion-Änderungen (Stats, Fähigkeiten) im Text stehen, nenne die konkreten Werte.
3. Falls der KONTEXT absolut nichts mit der Frage zu tun hat, sag: "Dazu liegen mir für diesen Patch keine spezifischen Informationen vor."
4. Antworte auf Deutsch und sei präzise.
Patch-Informationen:
{context}

Frage des Users:
{question}

Antwort:
"""
    try:
        print("DEBUG: Sende Anfrage an Ollama...")
        response = requests.post(
            OLLAMA_GEN_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1
                }
            },
            timeout=90
        )
        response.raise_for_status()
        return response.json()["response"]
        print(f"DEBUG: Ollama Antwort erhalten: {full_res['response'][:100]}...") # Hinzufügen
    except Exception as e:
        return f"Fehler bei der Antwortgenerierung: {e}"