# REST API

Base URL locally: `http://localhost:5000`. In production, `VITE_API_BASE_URL` should match the deployed API origin.

UTF-8 JSON everywhere. Errors always carry an `error` string; sometimes a `code` so the UI can branch without parsing prose.

## Shapes

**Chat — 200**

```json
{ "reply": "string", "conversation_id": "uuid-or-string" }
```

**Ingest — 200**

```json
{ "ingested": 42 }
```

**History — 200**

```json
{
  "messages": [
    {
      "id": 1,
      "conversation_id": "...",
      "role": "user",
      "content": "...",
      "created_at": "..."
    }
  ]
}
```

**Health — 200**

```json
{ "status": "ok" }
```

**Error — non-2xx**

```json
{
  "error": "Human-readable message",
  "code": "optional_machine_code"
}
```

| HTTP | Typical `code` | When |
|------|----------------|------|
| 400 | `validation_error` | Missing/empty `message`, bad JSON |
| 403 | `ingest_disabled` | `DISABLE_INGEST` is enabled |
| 403 | `ingest_forbidden` | `INGEST_SECRET` set but `X-Ingest-Secret` missing or wrong |
| 429 | `rate_limited` | Too many `POST /api/chat` (when rate limiting is on) |
| 503 | `ollama_unavailable` | Ollama down or embed/generate blew up |
| 500 | `rag_error` | RAG/server failure (generic text if `HIDE_INTERNAL_ERRORS` is on) |

## Endpoints

### `POST /api/chat`

Body:

```json
{
  "message": "User text (required)",
  "conversation_id": "optional; omit for new thread"
}
```

Runs retrieval + generation, then (when persistence works) stores user + assistant rows.

### `POST /api/ingest`

Body optional. Re-reads `backend/sample_docs/*.txt`, chunks, embeds, replaces the configured Chroma collection content.

**Production:** Set `DISABLE_INGEST=true` to return **403**, or set `INGEST_SECRET` and call with header `X-Ingest-Secret` (see [backend/.env.example](../backend/.env.example)).

### `GET /api/history/<conversation_id>?limit=50`

Messages for that conversation, oldest first. `limit` max **100**.

### `GET /health`

Flask liveness. It does **not** prove Ollama is happy—only that the API process answered.
