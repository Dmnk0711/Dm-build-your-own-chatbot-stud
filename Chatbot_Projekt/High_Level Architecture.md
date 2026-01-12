User
Frontend (Web/CLI/Discord-Bot)
Chatbot Backend (Docker) 
├── LLM (Ollama: Llama3/Mistal)
├── Patchnote Parser
├── Riot API Client
├── Context / Memory Layer
└── Analytics Logging
Datenbank



User
->
CLI oder Web-UI
-> 
FastAPI Backend
├── Ollama LLM
├── Patchnotes Loader (JSON)
├── Simple Retriever        
└── Analytics Logger
-> 
SQLite DB



CHATGPT:

LLM = Ollama
Backend = Python (Fast API)
Scraping = BeautifulSoup
DB = PostgreSQL/MongoDB
VectorDB = Chroma/FAISS
Analytics = Panda/Grafana
Container = Docker + Comspose
