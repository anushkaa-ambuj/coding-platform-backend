import pytest
from fastapi.testclient import TestClient
from main import app
from models import Challenge
from database import SessionLocal

# Dependency override for testing
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test list all challenges
def test_list_challenges():
    response = client.get("/candidate/challenges")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test fetching a specific challenge
def test_get_challenge_details():
    # First, create a challenge
    challenge_response = client.post("/admin/challenges", json={
        "title": "Fetch This Challenge",
        "description": "For testing challenge fetching",
        "input_format": "Input format",
        "output_format": "Output format",
        "sample_input": "Sample input",
        "sample_output": "Sample output"
    })
    challenge_id = challenge_response.json()["id"]
    
    response = client.get(f"/candidate/challenges/{challenge_id}")
    assert response.status_code == 200
    assert response.json()["id"] == challenge_id
