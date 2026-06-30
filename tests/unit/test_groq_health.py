"""Tests for Groq client singleton and health endpoint."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_groq_client_singleton():
    """Verify the Groq client returns the same instance on repeated calls."""
    import backend.core.groq_client as gc

    # Reset singleton for isolation
    gc._groq_client = None

    with patch("backend.core.groq_client.settings") as mock_settings:
        mock_settings.validate_groq_key.return_value = True
        mock_settings.groq_api_key = "gsk_test123"

        with patch("backend.core.groq_client.Groq") as MockGroq:
            mock_instance = MagicMock()
            MockGroq.return_value = mock_instance

            client1 = gc.get_groq_client()
            client2 = gc.get_groq_client()
            assert client1 is client2
            MockGroq.assert_called_once_with(api_key="gsk_test123")

    # Reset after test
    gc._groq_client = None


def test_groq_client_missing_key():
    """Verify RuntimeError when API key is missing."""
    import backend.core.groq_client as gc
    gc._groq_client = None

    with patch("backend.core.groq_client.settings") as mock_settings:
        mock_settings.validate_groq_key.return_value = False
        with pytest.raises(RuntimeError, match="GROQ_API_KEY is missing"):
            gc.get_groq_client()

    gc._groq_client = None


def test_health_endpoint():
    """Verify /api/health returns expected structure."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["backend"] == "running"
    assert "groq" in data
    assert "models" in data
    assert data["models"]["planner"] == "openai/gpt-oss-120b"
    assert data["models"]["developer"] == "openai/gpt-oss-120b"
    assert data["models"]["learner"] == "qwen/qwen3-32b"
    assert data["models"]["classifier"] == "qwen/qwen3-32b"
    assert "database" in data
    assert "cognee" in data
