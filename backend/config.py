import os

# Ollama API (embeddings and generation)
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.2")

# Chroma vector store (relative to backend dir)
CHROMA_PATH = os.environ.get("CHROMA_PATH", "chroma_db")
CHROMA_COLLECTION = "rag_docs"

# SQLite chat history
DB_PATH = os.environ.get("DB_PATH", "chat_history.db")

# Flask
FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.environ.get("FLASK_PORT", "5000"))
_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
CORS_ORIGINS = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", _default_origins).split(",")
    if o.strip()
]

# RAG
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5

# Sample docs path (relative to backend dir)
SAMPLE_DOCS_DIR = "sample_docs"
