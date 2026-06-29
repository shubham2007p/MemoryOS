import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from backend.main import app

# We use the FastAPI TestClient to request endpoints synchronously
client = TestClient(app)

def test_read_root():
    """Verify that root endpoint returns API name and version."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"name": "MemoryOS API", "version": "0.1.0"}

def test_session_api_flow():
    """Verify session CRUD REST endpoints."""
    # 1. Create a session
    response = client.post("/api/sessions", json={"metadata": {"source": "unit_test"}})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    session_id = data["session_id"]

    # 2. List sessions
    list_response = client.get("/api/sessions")
    assert list_response.status_code == 200
    sessions = list_response.json()
    assert any(s["session_id"] == session_id for s in sessions)

    # 3. Delete session
    delete_response = client.delete(f"/api/sessions/{session_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted"}

@pytest.mark.asyncio
async def test_specialist_learner_api():
    """Verify POST request to Learner specialist triggers workflow engine."""
    with patch("orchestrator.workflow_engine.WorkflowEngine.execute_learner_flow", new_callable=AsyncMock) as mock_flow:
        mock_flow.return_value = {"status": "remembered", "facts_extracted": ["MemoryOS is persistent."]}

        response = client.post("/api/specialists/learner", json={
            "session_id": "session-mock",
            "text": "MemoryOS is persistent."
        })
        assert response.status_code == 200
        assert response.json()["status"] == "remembered"
        mock_flow.assert_called_once_with(session_id="session-mock", text="MemoryOS is persistent.")

@pytest.mark.asyncio
async def test_specialist_developer_api():
    """Verify POST request to Developer specialist triggers workflow engine."""
    with patch("orchestrator.workflow_engine.WorkflowEngine.execute_developer_flow", new_callable=AsyncMock) as mock_flow:
        mock_flow.return_value = {"answer": "It is persistent."}

        response = client.post("/api/specialists/developer", json={
            "session_id": "session-mock",
            "query": "Is MemoryOS persistent?"
        })
        assert response.status_code == 200
        assert response.json()["answer"] == "It is persistent."
        mock_flow.assert_called_once_with(session_id="session-mock", query="Is MemoryOS persistent?")
