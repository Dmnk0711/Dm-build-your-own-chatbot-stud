import requests

# URL auf localhost anpassen für lokale Windows-Installation
OLLAMA_GEN_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3"

def generate_answer(context: str, question: str) -> str:
    print(f"DEBUG: Der übergebene Kontext ist: {context}")
    # Ein "System Prompt" sorgt dafür, dass das Modell sich an die Regeln hält
    prompt = f"""
Du bist ein präziser League of Legends Patch Assistant. 
Deine Aufgabe ist es, Fragen basierend auf den bereitgestellten Patch-Informationen zu beantworten.

REGELN:
1. Nutze AUSSCHLIESSLICH die unten stehenden Patch-Informationen.
2. Wenn die Antwort nicht in den Informationen enthalten ist, antworte: "Dazu liegen mir für diesen Patch keine Informationen vor."
3. Erfinde keine Änderungen, die nicht im Text stehen.
4. Antworte kurz und präzise auf Deutsch.

Patch-Informationen:
{context}

Frage des Users:
{question}

Antwort:
"""
    try:
        response = requests.post(
            OLLAMA_GEN_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                # Wir stellen die Temperatur niedrig ein, damit er weniger "kreativ" wird
                "options": {
                    "temperature": 0.1
                }
            },
            timeout=90
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Fehler bei der Antwortgenerierung: {e}"