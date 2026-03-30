# Product scope

## Phase A — MVP (in this repository)

Locked **Phase A** scope for portfolio and personal use:

- **Chat** with a nutrition-oriented Food Planner persona (RAG-grounded).
- **Retrieval**: embed query, similarity search over Chroma, context passed to Ollama.
- **Generation**: local LLM via Ollama with a fixed system prompt (explain recommendations; stay on topic).
- **Ingest**: load `backend/sample_docs/*.txt`, chunk, embed, store in Chroma (`POST /api/ingest` or documented equivalent).
- **Persistence**: SQLite for `conversations` and `messages` (`conversation_id`, roles, content).
- **API**: Flask REST with CORS for local Vite dev; documented error JSON for the UI.

Out of scope for Phase A:

- Hosted multi-user SaaS, accounts, or billing.
- Calorie databases or verified clinical workflows.
- Full **Life Planner** (habits, weekly rhythm UI) — see Phase B.

## Phase B — Life planner extension (future)

Pick **one** axis first; do not ship a generic productivity suite.

- **Option 1:** Weekly intentions + light rhythm (meal prep blocks, sleep/movement notes adjacent to nutrition).
- **Option 2:** Habit stubs tied to food (e.g. Sunday prep, protein at breakfast).

Phase B should reuse the same API style and remain optional in the README under **Future work**.
