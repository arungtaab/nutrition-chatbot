# Product scope

## Phase A — what this repo actually ships

Phase A is the **MVP I can run on my laptop**, show on a portfolio, and use for **vegetarian meal planning** in my own lane (**no meat, poultry, fish, or eggs**), plus pantry math and “what should I cook?”—without pretending it’s a medical device.

The same stack works for **other people** if they ingest different text and describe their own rules in chat; the **origin story** stays “I needed better vegetarian home-cooking support,” the **shape** is general-purpose RAG + chat.

- **Chat** with a nutrition-oriented Food Planner tone; answers should lean on **retrieved** text.
- **RAG:** embed the query, similarity search in Chroma, pass context into Ollama.
- **Generation:** local model via Ollama + a fixed system prompt (explain swaps, stay on topic, don’t play doctor).
- **Ingest:** `backend/sample_docs/*.txt` → chunk → embed → store (`POST /api/ingest` or equivalent you document).
- **Persistence:** SQLite for `conversations` / `messages` keyed by `conversation_id`.
- **API:** Flask REST, CORS for local Vite (and later your prod origins), structured error JSON.

**Explicitly not** in Phase A:

- Multi-tenant SaaS, auth walls, billing.
- Verified calorie databases or clinical pathways.
- The bigger **Life Planner** vision (habits, weekly rhythm UI)—that’s Phase B unless a job description drags it forward.

## Phase B — “life planner” (later, maybe)

If this grows, pick **one** spine first; nobody needs another generic productivity OS.

- **Option 1:** Weekly intentions + light rhythm (prep blocks next to meals, sleep notes—adjacent, not central).
- **Option 2:** Food-tied habits (Sunday batch, “did I eat breakfast protein?” stubs).

Same API style; document Phase B under **Future work** until something ships.
