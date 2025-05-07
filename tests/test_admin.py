import pytest
from fastapi.testclient import TestClient
from main import app
from models import Challenge, TestCase
from database import SessionLocal

# Dependency override for testing
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test challenge creation
def test_create_challenge():
    response = client.post("/admin/challenges", json={
        "title": "Test Challenge",
        "description": "A test challenge for unit testing",
        "input_format": "Input format",
        "output_format": "Output format",
        "sample_input": "Sample input",
        "sample_output": "Sample output"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Challenge"

# Test test case addition
def test_add_test_case():
    # First, create a challenge
    challenge_response = client.post("/admin/challenges", json={
        "title": "Another Test Challenge",
        "description": "Adding test case to this challenge",
        "input_format": "Input format",
        "output_format": "Output format",
        "sample_input": "Sample input",
        "sample_output": "Sample output"
    })
    challenge_id = challenge_response.json()["id"]
    
    # Add test cases to the created challenge
    response = client.post(f"/admin/challenges/{challenge_id}/testcases", json={
        "input_data": "Test case input",
        "expected_output": "Test case output"
    })
    assert response.status_code == 201
    assert "input_data" in response.json()
    assert response.json()["input_data"] == "Test case input"
