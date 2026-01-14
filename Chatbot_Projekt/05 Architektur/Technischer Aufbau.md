# Technische Umsetzung – grobes Architekturkonzept
### Ziel deines Projekts
Ein Gaming-Chatbot, der:

- mit Usern über Games, Builds, Tipps etc. spricht

- dabei Profil-Daten & Nutzungsdaten sammelt

- diese Daten verarbeitet/aggregiert
und dann in aufbereiteter Form (Dashboards / Reports / API) zur Verfügung stellt
---


# Tech-Stack:

## Frontend / UI

- Web-App (React, Vue oder simple HTML/JS)

- Chatfenster + Login/Registrierung (Username, evtl. Pseudonym)

## Backend API (Python FastAPI oder Node.js)

- Authentifizierung & Userverwaltung

- Endpoint /chat → nimmt User-Message, ruft LLM/RAG auf, gibt Antwort zurück

- Endpoints zum Datenzugriff: /analytics/summary, /analytics/raw etc.

- Schreibt alle relevanten Events in Datenbanken

## LLM-Schicht

- Ollama mit lokalem Modell (z.B. llama3, mistral, phi)

- Optional: RAG mit ChromaDB:

## Gaming-Wissen (FAQs, Guides, Patch Notes) in ChromaDB indexieren

- Backend baut aus User-Frage eine Retrieval-Query, holt passende Passagen und gibt sie zusammen mit der Frage an das Modell

## Datenhaltung

- ChromaDB → nur für Wissensbasis (Kontexte für RAG)

- Relationale DB (z.B. Postgres / MySQL) → User, Profile, Sessions, Events

- Optional: Data Warehouse / Analytics DB (kann auch dieselbe DB sein, logisch getrennte Tabellen):

- Aggregierte Kennzahlen: Spielzeit, Themen-Interessen, Peak-Times etc.

## Datenverarbeitung / Analytics

- Batch-Jobs (z.B. Cron + Python-Skripte) oder ein kleiner Worker (Celery, RQ o.ä.)

Aufgaben:

- Rohdaten → aggregierte Metriken (z.B. pro User, pro Spiel, pro Zeitraum)

- Anonymisierung / Pseudonymisierung (IDs statt Klarnamen)

- Speichern der fertigen „Data Products“ (Tabellen oder CSV / Parquet)

## „Daten bereitstellen“ für Business Case

- Ein Dashboard (z.B. Grafana/Metabase oder selbstgebautes Frontend) für interne Nutzung

- Eine Export-Funktion:

- z.B. Download als CSV/Excel

- oder eine API /partner-data mit Auth-Token, die aggregierte/anonymisierte Daten liefert

## Deployment / Infrastruktur (Docker Desktop)

Docker-Compose mit Services:

- frontend

- backend-api

- ollama

- chromadb

- db (Postgres)

- optional analytics-worker

Lokal für das Projekt ausreichend

### Wichtig für euren Bericht: Erwähne Datenschutz / DSGVO:

Zustimmung (Opt-in) der User

Anonymisierung vor Weitergabe

Kein Klarname + Adresse + ultra sensible Datei