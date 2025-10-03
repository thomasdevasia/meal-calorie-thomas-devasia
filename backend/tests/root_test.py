import pytest

from fastapi.testclient import TestClient
from app.main import app


def test_root():
	client = TestClient(app)
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"message": "Welcome to the Meal Calorie API"}

def test_health_check():
	client = TestClient(app)
	response = client.get("/health")
	assert response.status_code == 200
	assert response.json() == {"status": "healthy"}
