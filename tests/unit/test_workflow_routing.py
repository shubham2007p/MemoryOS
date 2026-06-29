import os
import pytest
from unittest.mock import AsyncMock, patch
from orchestrator.session_manager import SessionManager
from orchestrator.workflow_engine import WorkflowEngine

def test_classify_request():
    """Verify simple rule-based request classification in workflow engine."""
    engine = WorkflowEngine(session_manager=None)
    assert engine.classify_request("What is MemoryOS?") == "developer"
    assert engine.classify_request("Write code for binary search") == "developer"
    assert engine.classify_request("Einstein was born in Germany.") == "learner"

@pytest.mark.asyncio
async def test_route_request():
    """Verify route_request classified targets trigger correct execution flows."""
    db_path = "test_routing.db"
    manager = SessionManager(db_path=db_path)
    session = manager.create_session()
    session_id = session["session_id"]

    engine = WorkflowEngine(session_manager=manager)

    try:
        with patch.object(engine, "execute_developer_flow", new_callable=AsyncMock) as mock_dev, \
             patch.object(engine, "execute_learner_flow", new_callable=AsyncMock) as mock_learn:

            await engine.route_request(session_id, "What is Cognee?")
            mock_dev.assert_called_once_with(session_id, "What is Cognee?")
            mock_learn.assert_not_called()

            mock_dev.reset_mock()
            mock_learn.reset_mock()

            await engine.route_request(session_id, "MemoryOS is built on top of Cognee.")
            mock_learn.assert_called_once_with(session_id, "MemoryOS is built on top of Cognee.")
            mock_dev.assert_not_called()
    finally:
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
            except OSError:
                pass
