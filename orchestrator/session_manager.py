"""Session manager for MemoryOS.

This module manages temporary user sessions and persists their metadata and
ingested memories in a local SQLite database, separate from Cognee's permanent memory store.
"""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

DB_PATH = "metadata.db"

class SessionManager:
    """Manages creation, retrieval, updates, and deletion of temporary sessions and memory logs."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Create the sessions, memories, and permanent graph tables if they do not exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata_json TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    memory_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    specialist TEXT NOT NULL,
                    text TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS permanent_nodes (
                    node_id TEXT PRIMARY KEY,
                    label TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL,
                    color TEXT NOT NULL,
                    text TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS permanent_edges (
                    edge_id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    edge_type TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES permanent_nodes(node_id),
                    FOREIGN KEY (target_id) REFERENCES permanent_nodes(node_id),
                    UNIQUE(source_id, target_id)
                )
            """)
            conn.commit()

    def create_session(self, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new user session."""
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        status = "active"
        meta_str = json.dumps(metadata or {})

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (session_id, status, created_at, updated_at, metadata_json) VALUES (?, ?, ?, ?, ?)",
                (session_id, status, now, now, meta_str)
            )
            conn.commit()

        return {
            "session_id": session_id,
            "status": status,
            "created_at": now,
            "updated_at": now,
            "metadata": metadata or {}
        }

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a session by its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT session_id, status, created_at, updated_at, metadata_json FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None

            return {
                "session_id": row[0],
                "status": row[1],
                "created_at": row[2],
                "updated_at": row[3],
                "metadata": json.loads(row[4])
            }

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions in the system."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT session_id, status, created_at, updated_at, metadata_json FROM sessions ORDER BY created_at DESC")
            rows = cursor.fetchall()

            return [
                {
                    "session_id": row[0],
                    "status": row[1],
                    "created_at": row[2],
                    "updated_at": row[3],
                    "metadata": json.loads(row[4])
                }
                for row in rows
            ]

    def update_session(self, session_id: str, status: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Update status and/or metadata for a session."""
        session = self.get_session(session_id)
        if not session:
            return None

        new_status = status if status is not None else session["status"]
        merged_meta = {**session["metadata"], **(metadata or {})}
        meta_str = json.dumps(merged_meta)
        now = datetime.now(timezone.utc).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sessions SET status = ?, metadata_json = ?, updated_at = ? WHERE session_id = ?",
                (new_status, meta_str, now, session_id)
            )
            conn.commit()

        return {
            "session_id": session_id,
            "status": new_status,
            "created_at": session["created_at"],
            "updated_at": now,
            "metadata": merged_meta
        }

    def delete_session(self, session_id: str) -> bool:
        """Delete a session by its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            deleted_sessions_count = cursor.rowcount
            cursor.execute("DELETE FROM memories WHERE session_id = ?", (session_id,))
            conn.commit()
            return deleted_sessions_count > 0

    # Memory Logging Operations (Task 1)
    def add_memory_log(self, session_id: str, specialist: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Log a remembered fact or query result inside the metadata store."""
        memory_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        meta_str = json.dumps(metadata or {})

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memories (memory_id, session_id, specialist, text, metadata_json, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (memory_id, session_id, specialist, text, meta_str, now)
            )
            conn.commit()

        return {
            "memory_id": memory_id,
            "session_id": session_id,
            "specialist": specialist,
            "text": text,
            "metadata": metadata or {},
            "created_at": now
        }

    def list_memories(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all memories logged, optionally filtered by session_id."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute(
                    "SELECT memory_id, session_id, specialist, text, metadata_json, created_at FROM memories WHERE session_id = ? ORDER BY created_at DESC",
                    (session_id,)
                )
            else:
                cursor.execute("SELECT memory_id, session_id, specialist, text, metadata_json, created_at FROM memories ORDER BY created_at DESC")
            
            rows = cursor.fetchall()
            return [
                {
                    "memory_id": row[0],
                    "session_id": row[1],
                    "specialist": row[2],
                    "text": row[3],
                    "metadata": json.loads(row[4]),
                    "created_at": row[5]
                }
                for row in rows
            ]

    def search_memories(self, query: str, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search logged memories using wildcards."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            like_pattern = f"%{query}%"
            if session_id:
                cursor.execute(
                    "SELECT memory_id, session_id, specialist, text, metadata_json, created_at FROM memories WHERE session_id = ? AND text LIKE ? ORDER BY created_at DESC",
                    (session_id, like_pattern)
                )
            else:
                cursor.execute(
                    "SELECT memory_id, session_id, specialist, text, metadata_json, created_at FROM memories WHERE text LIKE ? ORDER BY created_at DESC",
                    (like_pattern,)
                )
            
            rows = cursor.fetchall()
            return [
                {
                    "memory_id": row[0],
                    "session_id": row[1],
                    "specialist": row[2],
                    "text": row[3],
                    "metadata": json.loads(row[4]),
                    "created_at": row[5]
                }
                for row in rows
            ]

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Fetch all logs and events associated with a session."""
        return self.list_memories(session_id=session_id)

    def delete_memory_log(self, memory_id: str) -> bool:
        """Delete a single memory log by its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE memory_id = ?", (memory_id,))
            conn.commit()
            return cursor.rowcount > 0

    def add_permanent_node(self, label: str, node_type: str, color: str, text: str) -> str:
        """Add a node to the permanent graph, returning its node_id. Avoids label duplicates."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT node_id FROM permanent_nodes WHERE label = ?", (label,))
            row = cursor.fetchone()
            if row:
                return row[0]
            node_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO permanent_nodes (node_id, label, type, color, text) VALUES (?, ?, ?, ?, ?)",
                (node_id, label, node_type, color, text)
            )
            conn.commit()
            return node_id

    def add_permanent_edge(self, source_id: str, target_id: str, edge_type: str) -> None:
        """Add a link between permanent nodes."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO permanent_edges (edge_id, source_id, target_id, edge_type) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), source_id, target_id, edge_type)
            )
            conn.commit()

    def get_permanent_nodes(self) -> List[Dict[str, Any]]:
        """Return all permanent nodes."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT node_id, label, type, color, text FROM permanent_nodes")
            rows = cursor.fetchall()
            return [
                {
                    "node_id": row[0],
                    "label": row[1],
                    "type": row[2],
                    "color": row[3],
                    "text": row[4]
                }
                for row in rows
            ]

    def get_permanent_edges(self) -> List[Dict[str, Any]]:
        """Return all permanent edges."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT edge_id, source_id, target_id, edge_type FROM permanent_edges")
            rows = cursor.fetchall()
            return [
                {
                    "edge_id": row[0],
                    "source_id": row[1],
                    "target_id": row[2],
                    "edge_type": row[3]
                }
                for row in rows
            ]
