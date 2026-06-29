"""Session manager for MemoryOS.

This module manages temporary user sessions and persists their metadata in a local
SQLite database, separate from Cognee's permanent memory store.
"""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

DB_PATH = "metadata.db"

class SessionManager:
    """Manages creation, retrieval, updates, and deletion of temporary sessions."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Create the sessions metadata table if it does not exist."""
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
            conn.commit()
            return cursor.rowcount > 0
