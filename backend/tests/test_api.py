"""
API endpoint tests using FastAPI TestClient.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_session_lifecycle():
    # 1. Start Session
    response = client.post("/start-session")
    assert response.status_code == 200
    start_data = response.json()
    assert "session_id" in start_data
    assert "plot width" in start_data["reply"].lower()

    session_id = start_data["session_id"]

    # 2. Send width
    chat_response = client.post("/chat", json={
        "session_id": session_id,
        "message": "30"
    })
    assert chat_response.status_code == 200
    chat_data = chat_response.json()
    assert chat_data["requirements"]["plot_width"] == 30
    assert "plot length" in chat_data["reply"].lower()
