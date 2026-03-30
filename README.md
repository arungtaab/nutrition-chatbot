# Food Planner — Nutrition RAG Chatbot

A **portfolio-friendly**, **personally useful** assistant for nutrition-oriented meal planning. The backend is a **Flask** API with **SQLite** chat history, **Chroma** vector storage, and **Ollama** for embeddings and generation (RAG). The frontend is **React (Vite)** with a distinctive **Chrome Pantry** visual system (Y2K chrome, dark pantry palette, light grain texture). See [docs/STYLE_GUIDE.md](docs/STYLE_GUIDE.md).

**Disclaimer:** This app provides **informational** meal-planning ideas only. It is **not medical advice**. For medical conditions, allergies, or treatment decisions, consult a qualified professional.

## What it demonstrates

- Python API design, configuration, and structured JSON errors (`error` + optional `code`).
- RAG: chunking, embeddings, similarity search, grounded generation.
- Local-first AI with Ollama; optional extension to hosted backends later.
- Product scope split: Phase A MVP vs future “life planner” extension — [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md).

## Architecture

High-level diagram and modules: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). REST contract: [docs/API.md](docs/API.md).

## Prerequisites

- Python **3.10+**
- Node.js **18+** and npm
- [Ollama](https://ollama.com) installed and running locally

Pull models (defaults match `backend/config.py`):

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

You can override with environment variables: `OLLAMA_EMBED_MODEL`, `OLLAMA_CHAT_MODEL`, `OLLAMA_HOST`.

## Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

API listens on **http://localhost:5000** by default (`FLASK_HOST`, `FLASK_PORT`).

### Ingest sample documents (required before useful RAG)

With the server running:

```bash
curl -X POST http://localhost:5000/api/ingest
```

This reloads the `rag_docs` collection from `backend/sample_docs/*.txt`.

### Health check

```bash
curl http://localhost:5000/health
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. The dev server proxies nothing by default; CORS allows `localhost` and `127.0.0.1` on port 5173 (override with `CORS_ORIGINS` comma-separated list).

### API URL

Copy [frontend/.env.example](frontend/.env.example) to `frontend/.env.local` and set:

```bash
VITE_API_BASE_URL=http://localhost:5000
```

Use this when the API is on another host (e.g. future deployment).

## Environment variables (reference)

| Variable | Where | Purpose |
|----------|--------|---------|
| `OLLAMA_HOST` | backend | Default `http://localhost:11434` |
| `OLLAMA_EMBED_MODEL` | backend | Default `nomic-embed-text` |
| `OLLAMA_CHAT_MODEL` | backend | Default `llama3.2` |
| `CHROMA_PATH` | backend | Vector store directory (default `chroma_db` under `backend/`) |
| `DB_PATH` | backend | SQLite file (default `chat_history.db` under `backend/`) |
| `CORS_ORIGINS` | backend | Comma-separated origins (defaults include Vite dev URLs) |
| `VITE_API_BASE_URL` | frontend | Flask base URL for `fetch` |

## Working in VS Code

1. **Open folder:** repository root.
2. **Python:** select `backend/.venv` interpreter ([.vscode/settings.json](.vscode/settings.json) hints a default path).
3. **Terminals:** (a) Ollama running app-wide, (b) `python app.py` in `backend/`, (c) `npm run dev` in `frontend/`.
4. **Debug:** “Python: Flask app.py” in [.vscode/launch.json](.vscode/launch.json).
5. **Typical session:** health check → `POST /api/ingest` → use the chat UI.

## GitHub: source vs live demo

- **This repository** is intended as **source-of-truth** you can clone and run locally.
- **GitHub Pages** can host the **static** Vite build only; you would still need a separate reachable API and CORS configuration.
- For a **full hosted** stack later, use a small PaaS (Render, Railway, Fly.io, etc.) for Flask and persistent disk for Chroma/SQLite as appropriate.

## Portfolio assets (recommended)

Add when you are happy with the UI:

- **Screenshots:** empty state, successful grounded reply, error state (Ollama off), narrow mobile width.
- **Short video (60–90s):** ingest + sample chat conversation.

Embed or link these from your README or portfolio site.

## Troubleshooting

### `npm ERR! UNABLE_TO_GET_ISSUER_CERT_LOCALLY`

Common on networks with SSL inspection. Prefer fixing trust:

```bash
export NODE_EXTRA_CA_CERTS="/path/to/your/corp-root.pem"
```

Or `npm config set cafile /path/to/your/corp-root.pem`. Avoid leaving `strict-ssl false` in place long-term.

### Ollama errors in the UI

- Ensure Ollama is running and models are pulled.
- Check browser/API response body for `error` and `code` (`ollama_unavailable`).

### Empty or weak answers

- Run `/api/ingest` after clearing `chroma_db` or on first clone.
- Add richer content to `backend/sample_docs/`.

## License

Specify a license if you open-source publicly (e.g. MIT). This README does not impose one by default.
