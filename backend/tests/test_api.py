import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_ai_assist():
    response = client.post(
        "/api/ai/assist",
        json={
            "question": "What is the capital of France?",
            "context": "General knowledge"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "answer" in response.json()

def test_transcribe_audio():
    response = client.post(
        "/api/transcribe",
        json={
            "audio": "base64encoded_audio_data"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "transcript" in response.json()

def test_login():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "access_token" in response.json()

def test_create_meeting():
    response = client.post(
        "/api/meetings",
        json={
            "title": "Test Meeting",
            "user_id": "test_user_id"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "meeting_id" in response.json()

def test_get_meeting():
    # Assuming a meeting with ID "mock_meeting_id_123" exists from previous test or setup
    response = client.get("/api/meetings/mock_meeting_id_123")
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert response.json()["meeting_id"] == "mock_meeting_id_123"

def test_register_user():
    response = client.post(
        "/api/users/register",
        json={
            "email": "newuser@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "user_id" in response.json()

def test_subscribe():
    response = client.post(
        "/api/billing/subscribe",
        json={
            "plan": "premium",
            "user_id": "test_user_id"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "Successfully subscribed" in response.json()["message"]
