"""Workflow engine and orchestrator for MemoryOS.

This module coordinates interactions between user sessions, specialists,
and the Cognee memory system.
"""

import logging
from typing import Any, Dict
from orchestrator.session_manager import SessionManager

logger = logging.getLogger("orchestrator.workflow_engine")

class WorkflowEngine:
    """Orchestrates workflows between sessions and specialists."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def execute_learner_flow(self, session_id: str, text: str) -> Dict[str, Any]:
        """Execute the Learning Specialist workflow: Ingest info into memory."""
        logger.info(f"Running learner flow for session {session_id}")
        session = self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Import dynamically to avoid circular dependencies
        from specialists.learner.workflow import LearnerSpecialist
        learner = LearnerSpecialist()
        result = await learner.learn_fact(text, session_id=session_id)

        # Update session metadata
        self.session_manager.update_session(
            session_id,
            metadata={"last_learned_text": text}
        )
        return result

    async def execute_developer_flow(self, session_id: str, query: str) -> Dict[str, Any]:
        """Execute the Developer Specialist workflow: Recall and generate answer."""
        logger.info(f"Running developer flow for session {session_id}")
        session = self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Import dynamically to avoid circular dependencies
        from specialists.developer.workflow import DeveloperSpecialist
        developer = DeveloperSpecialist()
        result = await developer.resolve_query(query, session_id=session_id)

        # Update session metadata
        self.session_manager.update_session(
            session_id,
            metadata={"last_query": query}
        )
        return result
