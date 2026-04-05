import pytest


@pytest.fixture
def client():
    from app import app as flask_app

    flask_app.config["TESTING"] = True
    return flask_app.test_client()


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_chat_missing_message(client):
    r = client.post("/api/chat", json={})
    assert r.status_code == 400
    body = r.get_json()
    assert body["code"] == "validation_error"
    assert "message" in body["error"].lower()


def test_chat_empty_message(client):
    r = client.post("/api/chat", json={"message": "   "})
    assert r.status_code == 400
    assert r.get_json()["code"] == "validation_error"


def test_chat_happy_path_mocked(client, monkeypatch):
    monkeypatch.setattr("app.chat", lambda _m: "Mocked grounded reply.")

    r = client.post("/api/chat", json={"message": "Ideas for lunch?"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["reply"] == "Mocked grounded reply."
    assert data.get("conversation_id")


def test_ed_query_refusal_no_llm(client, monkeypatch):
    called = []

    def _fail(_m):
        called.append(True)
        raise AssertionError("LLM should not run for ED-sensitive prompts")

    monkeypatch.setattr("app.chat", _fail)

    r = client.post(
        "/api/chat",
        json={"message": "How do I purge after dinner without anyone noticing?"},
    )
    assert r.status_code == 200
    body = r.get_json()
    assert not called
    assert "eating" in body["reply"].lower() or "disorder" in body["reply"].lower()
    assert "neda" in body["reply"].lower() or "988" in body["reply"]
    assert body.get("conversation_id")


def test_normal_meal_question_not_blocked_as_ed(client, monkeypatch):
    monkeypatch.setattr("app.chat", lambda _m: "Here is lunch.")

    r = client.post(
        "/api/chat",
        json={"message": "How many calories are in a banana roughly?"},
    )
    assert r.status_code == 200
    assert r.get_json()["reply"] == "Here is lunch."


def test_medical_query_refusal_no_llm(client, monkeypatch):
    called = []

    def _fail(_m):
        called.append(True)
        raise AssertionError("LLM should not run for medical-style prompts")

    monkeypatch.setattr("app.chat", _fail)

    r = client.post(
        "/api/chat",
        json={"message": "Do I have diabetes based on these symptoms?"},
    )
    assert r.status_code == 200
    body = r.get_json()
    assert not called
    assert "medical" in body["reply"].lower() or "diagnosis" in body["reply"].lower()
    assert body.get("conversation_id")


def test_ingest_disabled_returns_403(client, monkeypatch):
    monkeypatch.setattr("app.DISABLE_INGEST", True)
    r = client.post("/api/ingest")
    assert r.status_code == 403
    assert r.get_json()["code"] == "ingest_disabled"


def test_ingest_secret_required(client, monkeypatch):
    monkeypatch.setattr("app.DISABLE_INGEST", False)
    monkeypatch.setattr("app.INGEST_SECRET", "test-secret")
    monkeypatch.setattr("app.ingest_docs", lambda: 3)

    r = client.post("/api/ingest")
    assert r.status_code == 403
    assert r.get_json()["code"] == "ingest_forbidden"

    r2 = client.post("/api/ingest", headers={"X-Ingest-Secret": "test-secret"})
    assert r2.status_code == 200
    assert r2.get_json() == {"ingested": 3}


def test_rag_error_message_hidden_when_configured(client, monkeypatch):
    monkeypatch.setattr("app.HIDE_INTERNAL_ERRORS", True)

    def _boom(_m):
        raise ValueError("internal_db_secret_xyz")

    monkeypatch.setattr("app.chat", _boom)
    r = client.post("/api/chat", json={"message": "What is fiber?"})
    assert r.status_code == 500
    err = r.get_json()["error"]
    assert "internal_db_secret" not in err
    assert "try again" in err.lower() or "wrong" in err.lower()


def test_history_returns_messages(client, monkeypatch):
    monkeypatch.setattr("app.chat", lambda _m: "Reply one.")
    cid = "test-conv-uuid"
    client.post("/api/chat", json={"message": "Hello", "conversation_id": cid})
    r = client.get(f"/api/history/{cid}")
    assert r.status_code == 200
    msgs = r.get_json()["messages"]
    assert len(msgs) >= 2
    assert msgs[0]["role"] == "user"
    assert msgs[0]["content"] == "Hello"
    assert msgs[1]["role"] == "assistant"
