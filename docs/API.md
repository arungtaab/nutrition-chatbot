# REST API contract

Base URL (local default): `http://localhost:5000`

All JSON responses use UTF-8. Error responses always include an `error` string. They may include a `code` string for programmatic handling in the UI.

## Success and error shape

**Chat success (200)**

```json
{ "reply": "string", "conversation_id": "uuid-or-string" }
```

**Ingest success (200)**

```json
{ "ingested": 42 }
```

**History success (200)**

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

**Health (200)**

```json
{ "status": "ok" }
```

**Error (non-2xx)**

```json
{
  "error": "Human-readable message",
  "code": "optional_machine_code"
}
```

| HTTP | `code` (typical) | When |
|------|------------------|------|
| 400 | `validation_error` | Missing or empty `message`, malformed JSON |
| 503 | `ollama_unavailable` | Ollama unreachable or model/embed failure surfaced as `RuntimeError` |
| 500 | `rag_error` | Unexpected server/RAG failure |

## Endpoints

### `POST /api/chat`

**Body**

```json
{
  "message": "User text (required)",
  "conversation_id": "optional; omit to start a new conversation"
}
```

**Behavior:** Runs RAG (retrieve from Chroma, generate via Ollama), persists user + assistant messages when persistence succeeds.

### `POST /api/ingest`

**Body:** Optional. Re-embeds `backend/sample_docs/*.txt` into Chroma (replaces existing collection content for the configured collection name).

### `GET /api/history/<conversation_id>?limit=50`

Returns recent messages for that conversation, oldest first. `limit` capped at 100.

### `GET /health`

Liveness check for the Flask process (does not verify Ollama).
