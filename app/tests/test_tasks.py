import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace YOUR_API_KEY with a valid token
    response = client.post(
        "/register", 
        json={"username": "testuglsker", "email": "uskegr1@example.com", "password": "testpass"},
        headers=headers
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_register_user_existing():
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace YOUR_API_KEY with a valid token
    response = client.post(
        "/register", 
        json={"username": "testuser","email": "uskegr1@example.com", "password": "testpass"},
        headers=headers
    )
    print(response.json())
    assert response.json()["status"] == "error"
    assert response.json()["error_code"] == 101  # Assuming duplicate user returns 101
