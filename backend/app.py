import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import CORS_ORIGINS, FLASK_HOST, FLASK_PORT
from database import init_db, save_message, get_history
from rag_service import chat, ingest_docs

app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)


@app.before_request
def _ensure_db():
    init_db()


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in body"}), 400
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    conversation_id = (data.get("conversation_id") or "").strip() or str(uuid.uuid4())

    try:
        reply = chat(message)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"RAG error: {e}"}), 500

    try:
        save_message(conversation_id, "user", message)
        save_message(conversation_id, "assistant", reply)
    except Exception:
        pass

    return jsonify({"reply": reply, "conversation_id": conversation_id})


@app.route("/api/ingest", methods=["POST"])
def api_ingest():
    """Ingest sample_docs into Chroma. Optionally accept a file or text in the body."""
    try:
        if request.files:
            # Optional: save uploaded file and ingest (simplified: just run sample_docs)
            count = ingest_docs()
        elif request.get_data():
            # Optional: raw text in body - for now still use sample_docs
            count = ingest_docs()
        else:
            count = ingest_docs()
        return jsonify({"ingested": count})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"Ingest error: {e}"}), 500


@app.route("/api/history/<conversation_id>", methods=["GET"])
def api_history(conversation_id):
    limit = request.args.get("limit", default=50, type=int)
    limit = min(max(1, limit), 100)
    messages = get_history(conversation_id, limit=limit)
    return jsonify({"messages": messages})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
