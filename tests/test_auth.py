from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_public_info():
    response = client.get("/public/info")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome stranger! This info is public."}

def test_protected_profile_unauthorized_missing_token():
    response = client.get("/protected/profile")
    assert response.status_code == 401
    assert response.json() == {"error": "Access token required"}

def test_protected_profile_invalid_token():
    response = client.get(
        "/protected/profile",
        headers={"Authorization": "Bearer invalid_token_xyz"}
    )
    assert response.status_code == 401
    assert response.json() == {"error": "Invalid or expired token"}

def test_signup_validation_missing_fields():
    response = client.post("/auth/signup", json={"email": ""})
    assert response.status_code == 400
    assert response.json() == {"error": "Email and password are required"}

def test_login_validation_missing_fields():
    response = client.post("/auth/login", json={"email": "user@test.com"})
    assert response.status_code == 400
    assert response.json() == {"error": "Email and password are required"}

def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"error": "Invalid login credentials"}

@patch("app.dependencies.supabase.auth.get_user")
def test_protected_profile_valid_token(mock_get_user):
    mock_user = MagicMock()
    mock_user.id = "user-123"
    mock_user.email = "test@example.com"
    mock_user.created_at = "2026-10-08T00:00:00Z"
    mock_user.app_metadata = {}
    mock_user.user_metadata = {}

    mock_response = MagicMock()
    mock_response.user = mock_user
    mock_get_user.return_value = mock_response

    response = client.get(
        "/protected/profile",
        headers={"Authorization": "Bearer valid_mock_token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "user-123"
    assert data["email"] == "test@example.com"

@patch("app.dependencies.supabase.auth.get_user")
def test_protected_dashboard_valid_token(mock_get_user):
    mock_user = MagicMock()
    mock_user.id = "user-123"
    mock_user.email = "test@example.com"

    mock_response = MagicMock()
    mock_response.user = mock_user
    mock_get_user.return_value = mock_response

    response = client.get(
        "/protected/dashboard",
        headers={"Authorization": "Bearer valid_mock_token"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to your dashboard, test@example.com!"

@patch("app.dependencies.supabase.auth.get_user")
@patch("app.dependencies.supabase.auth.sign_out")
def test_logout_valid_token(mock_sign_out, mock_get_user):
    mock_user = MagicMock()
    mock_user.id = "user-123"
    mock_user.email = "test@example.com"

    mock_response = MagicMock()
    mock_response.user = mock_user
    mock_get_user.return_value = mock_response

    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer valid_mock_token"}
    )
    assert response.status_code == 204
