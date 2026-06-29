import os
import pytest
from orchestrator.session_manager import SessionManager

import uuid

@pytest.fixture
def session_manager():
    """Fixture to provide a SessionManager utilizing a temporary database."""
    db_path = f"test_metadata_{uuid.uuid4().hex}.db"
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

def test_memory_logging(session_manager):
    """Test memory log creation, listing, searching, and deletion."""
    session = session_manager.create_session()
    session_id = session["session_id"]

    # 1. Log a memory
    mem1 = session_manager.add_memory_log(
        session_id=session_id,
        specialist="learner",
        text="The capital of Spain is Madrid.",
        metadata={"relevance": "geography"}
    )
    assert mem1["memory_id"] is not None
    assert mem1["specialist"] == "learner"

    # Log another memory
    mem2 = session_manager.add_memory_log(
        session_id=session_id,
        specialist="developer",
        text="FastAPI is a modern web framework.",
        metadata={"category": "web"}
    )

    # 2. List memories
    all_memories = session_manager.list_memories()
    assert len(all_memories) == 2
    assert all_memories[0]["text"] == "FastAPI is a modern web framework."

    # Filtered by session
    session_memories = session_manager.list_memories(session_id=session_id)
    assert len(session_memories) == 2

    # 3. Search memories
    search_res = session_manager.search_memories(query="Spain")
    assert len(search_res) == 1
    assert search_res[0]["text"] == "The capital of Spain is Madrid."

    # Search with no matches
    assert len(session_manager.search_memories(query="NonExistentKeyword")) == 0

    # 4. Delete memory log
    del_ok = session_manager.delete_memory_log(mem1["memory_id"])
    assert del_ok is True
    assert len(session_manager.list_memories()) == 1

