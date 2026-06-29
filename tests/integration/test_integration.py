import os
import pytest
from unittest.mock import AsyncMock, patch
from orchestrator.session_manager import SessionManager
from orchestrator.workflow_engine import WorkflowEngine

@pytest.fixture
def temp_session_manager():
    """Fixture to provide a temporary SessionManager for integration testing."""
    db_path = "test_integration.db"
    manager = SessionManager(db_path=db_path)
    yield manager
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass

@pytest.mark.asyncio
async def test_end_to_end_specialist_workflow(temp_session_manager):
    """Test the end-to-end interaction flow of specialists, sessions, and routing."""
    workflow_engine = WorkflowEngine(session_manager=temp_session_manager)

    # 1. Create a session
    session = temp_session_manager.create_session(metadata={"client": "integration_test"})
    session_id = session["session_id"]
    assert session_id is not None

    # 2. Ingest information using Learner Specialist via Route Request
    mock_remember_res = AsyncMock()
    mock_remember_res.status = "completed"

    with patch("cognee.remember", return_value=mock_remember_res) as mock_remember:
        # Route a statement -> should run learner flow
        learn_result = await workflow_engine.route_request(
            session_id=session_id,
            text="MemoryOS is built using FastAPI and Streamlit."
        )

        assert learn_result["status"] == "remembered"
        mock_remember.assert_called_once()
        called_kwargs = mock_remember.call_args[1]
        assert called_kwargs["data"] == "MemoryOS is built using FastAPI and Streamlit."
        assert called_kwargs["session_id"] == session_id

    # Verify session metadata was updated with the last learned text
    updated_session = temp_session_manager.get_session(session_id)
    assert updated_session["metadata"]["last_learned_text"] == "MemoryOS is built using FastAPI and Streamlit."

    # 3. Retrieve context and answer question using Developer Specialist via Route Request
    mock_recalled = [{"text": "MemoryOS is built using FastAPI and Streamlit."}]

    with patch("cognee.recall", return_value=mock_recalled) as mock_recall:
        # Route a question -> should run developer flow
        query_result = await workflow_engine.route_request(
            session_id=session_id,
            text="What is MemoryOS built on?"
        )

        assert "MemoryOS is built using FastAPI and Streamlit." in query_result["answer"]
        mock_recall.assert_called_once()
        called_kwargs = mock_recall.call_args[1]
        assert called_kwargs["query_text"] == "What is MemoryOS built on?"
        assert called_kwargs["session_id"] == session_id

    # Verify session metadata was updated with the last query
    final_session = temp_session_manager.get_session(session_id)
    assert final_session["metadata"]["last_query"] == "What is MemoryOS built on?"

    # 4. Complete session and trigger consolidation
    with patch("memory.triggers.improve_memory", new_callable=AsyncMock) as mock_improve:
        complete_res = await workflow_engine.complete_session(session_id)
        assert complete_res["status"] == "completed"
        mock_improve.assert_called_once_with(session_ids=[session_id])

    # Verify session status is updated to completed
    completed_session = temp_session_manager.get_session(session_id)
    assert completed_session["status"] == "completed"
