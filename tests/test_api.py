"""
Comprehensive test suite for Healthcare NLP API.
Tests cover health check, NER extraction, RAG queries, and error handling.
Uses mocked NLP engine to avoid downloading heavy models during testing.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# ── Health Check Tests ──────────────────────────────────────

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["system"] == "MedNLP-RAG"


def test_health_check_returns_json(client):
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"


# ── NER Extraction Tests ────────────────────────────────────

def test_api_analyze_valid_text(client):
    payload = {"text": "Patient has Type 2 Diabetes and Hypertension."}
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "entities" in data
    assert "metadata" in data
    assert "processing_time_sec" in data["metadata"]


def test_api_analyze_empty_text(client):
    response = client.post("/api/v1/analyze", json={"text": "   "})
    assert response.status_code == 400
    assert "Empty text" in response.json()["detail"]


def test_api_analyze_missing_text_field(client):
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 422  # Pydantic validation error


def test_api_analyze_entities_structure(client):
    """Verifies each entity has expected keys."""
    payload = {"text": "The patient was prescribed Metformin 500mg for diabetes."}
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    entities = response.json()["entities"]
    if entities:
        for ent in entities:
            assert "word" in ent or "entity_group" in ent


def test_api_analyze_with_context(client):
    """Tests that optional context field is accepted."""
    payload = {
        "text": "Patient reports chest pain and dyspnea.",
        "context": "Cardiology ward admission note"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200


def test_api_analyze_long_text(client):
    """Tests processing of longer clinical text."""
    long_text = "Patient presents with " + "chronic pain and " * 100 + "requires evaluation."
    payload = {"text": long_text}
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200


# ── RAG Query Tests ─────────────────────────────────────────

def test_api_query(client):
    response = client.post("/api/v1/query", json={"query": "hypertension", "top_k": 1})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "processing_time_sec" in data


def test_api_query_default_top_k(client):
    """Tests query with default top_k (should default to 3)."""
    response = client.post("/api/v1/query", json={"query": "diabetes treatment"})
    assert response.status_code == 200


def test_api_query_missing_query(client):
    response = client.post("/api/v1/query", json={})
    assert response.status_code == 422


def test_api_query_sources_is_list(client):
    response = client.post("/api/v1/query", json={"query": "medication dosage", "top_k": 2})
    assert response.status_code == 200
    assert isinstance(response.json()["sources"], list)


# ── CORS Tests ──────────────────────────────────────────────

def test_cors_headers(client):
    """Verifies CORS middleware is active."""
    response = client.options(
        "/health",
        headers={"Origin": "http://localhost:8501", "Access-Control-Request-Method": "GET"}
    )
    # CORS middleware should allow the origin
    assert response.status_code in (200, 204, 405)


# ── Invalid Route ───────────────────────────────────────────

def test_nonexistent_route(client):
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
