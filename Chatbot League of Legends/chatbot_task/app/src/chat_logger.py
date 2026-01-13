# src/chat_logger.py
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

LOG_FILE = Path("chat_logs.jsonl")  # wird im Projekt-Root angelegt

def save_chat_log(
    session_id: str,
    user_message: str,
    bot_reply: str,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Speichert einen Chat-Datensatz als einzelne Zeile im JSONL-Format.
    Jede Zeile ist ein gültiges JSON-Objekt.
    """
    if meta is None:
        meta = {}

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": session_id,
        "user_message": user_message,
        "bot_reply": bot_reply,
        "meta": meta,
    }

    # Sicherheitsnetz: Ordner anlegen, falls nötig
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
