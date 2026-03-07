import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "system": "MedNLP-RAG"}

def test_api_analyze_empty_text(client):
    response = client.post("/api/v1/analyze", json={"text": "   "})
    assert response.status_code == 400
    assert "Empty text" in response.json()["detail"]

def test_api_query(client):
    # Because we don't load huge models in test env implicitly by default
    # The NLP Engine should mock responses or handle gracefully.
    response = client.post("/api/v1/query", json={"query": "hypertension", "top_k": 1})
    
    # We expect a success code and mock default string as defined in nlp_engine.py 
    # if it runs without heavy model.
    assert response.status_code == 200
    assert "answer" in response.json()
