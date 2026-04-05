import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import (
    CORS_ORIGINS,
    FLASK_HOST,
    FLASK_PORT,
    CHAT_RATE_LIMIT,
    RATE_LIMIT_ENABLED,
    DISABLE_INGEST,
    INGEST_SECRET,
    HIDE_INTERNAL_ERRORS,
)
from database import init_db, save_message, get_history
from errors import api_error
from rag_service import chat, ingest_docs
from safety import (
    ed_refusal_reply,
    ed_sensitive_message,
    medical_sensitive_message,
    safety_refusal_reply,
)

app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[],
    enabled=RATE_LIMIT_ENABLED,
)


@app.before_request
def _ensure_db():
    init_db()


def _client_error_message(detail: str) -> str:
    if HIDE_INTERNAL_ERRORS:
        return "Something went wrong. Please try again in a moment."
    return detail


@app.route("/api/chat", methods=["POST"])
@limiter.limit(
    CHAT_RATE_LIMIT,
    methods=["POST"],
    error_message="Too many requests. Please wait a moment and try again.",
)
def api_chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify(api_error("Missing 'message' in body", "validation_error")), 400
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify(api_error("Message cannot be empty", "validation_error")), 400

    conversation_id = (data.get("conversation_id") or "").strip() or str(uuid.uuid4())

    if ed_sensitive_message(message):
        reply = ed_refusal_reply()
        try:
            save_message(conversation_id, "user", message)
            save_message(conversation_id, "assistant", reply)
        except Exception:
            pass
        return jsonify({"reply": reply, "conversation_id": conversation_id})

    if medical_sensitive_message(message):
        reply = safety_refusal_reply()
        try:
            save_message(conversation_id, "user", message)
            save_message(conversation_id, "assistant", reply)
        except Exception:
            pass
        return jsonify({"reply": reply, "conversation_id": conversation_id})

    try:
        reply = chat(message)
    except RuntimeError as e:
        return jsonify(api_error(str(e), "ollama_unavailable")), 503
    except Exception as e:
        return (
            jsonify(
                api_error(
                    _client_error_message(f"RAG error: {e}"),
                    "rag_error",
                )
            ),
            500,
        )

    try:
        save_message(conversation_id, "user", message)
        save_message(conversation_id, "assistant", reply)
    except Exception:
        pass

    return jsonify({"reply": reply, "conversation_id": conversation_id})


@app.route("/api/ingest", methods=["POST"])
def api_ingest():
    """Ingest sample_docs into Chroma. Optionally accept a file or text in the body."""
    if DISABLE_INGEST:
        return (
            jsonify(
                api_error(
                    "Document ingest is disabled on this server.",
                    "ingest_disabled",
                )
            ),
            403,
        )
    if INGEST_SECRET:
        sent = (request.headers.get("X-Ingest-Secret") or "").strip()
        if sent != INGEST_SECRET:
            return (
                jsonify(
                    api_error(
                        "Ingest requires a valid secret.",
                        "ingest_forbidden",
                    )
                ),
                403,
            )
    try:
        if request.files:
            count = ingest_docs()
        elif request.get_data():
            count = ingest_docs()
        else:
            count = ingest_docs()
        return jsonify({"ingested": count})
    except RuntimeError as e:
        return jsonify(api_error(str(e), "ollama_unavailable")), 503
    except Exception as e:
        return (
            jsonify(
                api_error(
                    _client_error_message(f"Ingest error: {e}"),
                    "rag_error",
                )
            ),
            500,
        )


@app.route("/api/history/<conversation_id>", methods=["GET"])
def api_history(conversation_id):
    limit = request.args.get("limit", default=50, type=int)
    limit = min(max(1, limit), 100)
    messages = get_history(conversation_id, limit=limit)
    return jsonify({"messages": messages})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.errorhandler(429)
def _rate_limit_exceeded(e):
    return jsonify(api_error(getattr(e, "description", None) or "Too many requests", "rate_limited")), 429


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
