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
    """Test the end-to-end interaction flow of specialists and sessions."""
    workflow_engine = WorkflowEngine(session_manager=temp_session_manager)

    # 1. Create a session
    session = temp_session_manager.create_session(metadata={"client": "integration_test"})
    session_id = session["session_id"]
    assert session_id is not None

    # 2. Ingest information using Learner Specialist
    mock_remember_res = AsyncMock()
    mock_remember_res.status = "completed"

    with patch("cognee.remember", return_value=mock_remember_res) as mock_remember:
        learn_result = await workflow_engine.execute_learner_flow(
            session_id=session_id,
            text="MemoryOS is built using FastAPI and Streamlit."
        )

        assert learn_result["status"] == "remembered"
        mock_remember.assert_called_once_with(
            data="MemoryOS is built using FastAPI and Streamlit.",
            dataset_name="main_dataset",
            session_id=session_id
        )

    # Verify session metadata was updated with the last learned text
    updated_session = temp_session_manager.get_session(session_id)
    assert updated_session["metadata"]["last_learned_text"] == "MemoryOS is built using FastAPI and Streamlit."

    # 3. Retrieve context and answer question using Developer Specialist
    mock_recalled = [{"text": "MemoryOS is built using FastAPI and Streamlit."}]

    with patch("cognee.recall", return_value=mock_recalled) as mock_recall:
        query_result = await workflow_engine.execute_developer_flow(
            session_id=session_id,
            query="What is MemoryOS built on?"
        )

        assert "MemoryOS is built using FastAPI and Streamlit." in query_result["answer"]
        mock_recall.assert_called_once_with(
            query_text="What is MemoryOS built on?",
            session_id=session_id
        )

    # Verify session metadata was updated with the last query
    final_session = temp_session_manager.get_session(session_id)
    assert final_session["metadata"]["last_query"] == "What is MemoryOS built on?"
