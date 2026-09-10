from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_session_api():
    response = client.post("/api/v1/sessions")
    assert response.status_code == 200
    data = response.json()
    assert "session_token" in data
    assert "lead_state" in data
    assert data["lead_state"] == "idle"


def test_chat_nonexistent_session():
    response = client.post(
        "/api/v1/chat",
        json={
            "session_token": "nonexistent_token_12345",
            "message": "Hello",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_lead_capture_nonexistent_session():
    response = client.post(
        "/api/v1/lead-capture",
        json={
            "session_token": "nonexistent_token_12345",
            "field": "full_name",
            "value": "John Doe",
        },
    )
    assert response.status_code == 404


def test_lead_capture_flow():
    # 1. Create session
    sess_res = client.post("/api/v1/sessions")
    assert sess_res.status_code == 200
    session_token = sess_res.json()["session_token"]

    # 2. Capture invalid name
    bad_name = client.post(
        "/api/v1/lead-capture",
        json={
            "session_token": session_token,
            "field": "full_name",
            "value": "1",
        },
    )
    assert bad_name.status_code == 200
    assert bad_name.json()["success"] is False

    # 3. Capture valid name
    good_name = client.post(
        "/api/v1/lead-capture",
        json={
            "session_token": session_token,
            "field": "full_name",
            "value": "Sarah Connor",
        },
    )
    assert good_name.status_code == 200
    assert good_name.json()["success"] is True
    assert good_name.json()["lead_state"] == "collecting_email"
