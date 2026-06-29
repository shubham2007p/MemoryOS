import os
import pytest
from orchestrator.session_manager import SessionManager

@pytest.fixture
def session_manager():
    """Fixture to provide a SessionManager utilizing a temporary database."""
    db_path = "test_metadata.db"
    manager = SessionManager(db_path=db_path)
    yield manager
    # Cleanup after test run
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass

def test_session_lifecycle(session_manager):
    """Test full CRUD cycle of session metadata."""
    # 1. Create session
    session = session_manager.create_session(metadata={"user": "alice"})
    session_id = session["session_id"]
    assert session_id is not None
    assert session["status"] == "active"
    assert session["metadata"] == {"user": "alice"}

    # 2. Retrieve session
    retrieved = session_manager.get_session(session_id)
    assert retrieved is not None
    assert retrieved["session_id"] == session_id
    assert retrieved["metadata"] == {"user": "alice"}

    # 3. List sessions
    sessions = session_manager.list_sessions()
    assert len(sessions) == 1
    assert sessions[0]["session_id"] == session_id

    # 4. Update session
    updated = session_manager.update_session(session_id, status="completed", metadata={"theme": "dark"})
    assert updated is not None
    assert updated["status"] == "completed"
    assert updated["metadata"] == {"user": "alice", "theme": "dark"}

    # 5. Delete session
    success = session_manager.delete_session(session_id)
    assert success is True
    assert session_manager.get_session(session_id) is None
