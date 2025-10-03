import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_success():
	payload = {
		"first_name": "John",
		"last_name": "Doe",
		"email": "john.doe@example.com",
		"password": "securepassword"
	}
	response = client.post("/auth/signup", json=payload)
	assert response.status_code == 201
	assert "token" in response.json()
	assert response.json()["message"] == "User signed up successfully"

def test_signup_duplicate():
	payload = {
		"first_name": "John",
		"last_name": "Doe",
		"email": "john.doe@example.com",
		"password": "securepassword"
	}
	response = client.post("/auth/signup", json=payload)
	assert response.status_code == 400
	assert response.json()["detail"] == "User with this Email already registered"

def test_login_success():
	payload = {
		"email": "john.doe@example.com",
		"password": "securepassword"
	}
	response = client.post("/auth/login", json=payload)
	assert response.status_code == 200
	assert "token" in response.json()
	assert response.json()["message"] == "User logged in successfully"

def test_login_wrong_password():
	payload = {
		"email": "john.doe@example.com",
		"password": "wrongpassword"
	}
	response = client.post("/auth/login", json=payload)
	assert response.status_code == 401
	assert response.json()["detail"] == "Invalid password"

def test_login_nonexistent_user():
	payload = {
		"email": "nonexistent@example.com",
		"password": "any"
	}
	response = client.post("/auth/login", json=payload)
	assert response.status_code == 401
	assert response.json()["detail"] == "The user does not exist. Please sign up first."
