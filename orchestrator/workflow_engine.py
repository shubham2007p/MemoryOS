"""Workflow engine and orchestrator for MemoryOS.

This module coordinates interactions between user sessions, specialists,
and the Cognee memory system, including dynamic routing and triggers.
"""

import logging
from typing import Any, Dict
from orchestrator.session_manager import SessionManager
from memory.triggers import trigger_end_of_session

logger = logging.getLogger("orchestrator.workflow_engine")

class WorkflowEngine:
    """Orchestrates workflows between sessions and specialists, applying dynamic routing."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    def classify_request(self, text: str) -> str:
        """Classify request type based on rule-based cues.

        Returns "developer" if it is a question or coding request,
        otherwise "learner".

        Args:
            text: Input user message.

        Returns:
            Specialist identifier string ("developer" or "learner").
        """
        text_lower = text.lower().strip()
        dev_cues = ["what", "how", "why", "who", "where", "write", "generate", "code", "implement", "create", "explain", "run"]
        is_question = text_lower.endswith("?") or any(text_lower.startswith(cue) for cue in dev_cues)
        return "developer" if is_question else "learner"

    async def route_request(self, session_id: str, text: str) -> Dict[str, Any]:
        """Automatically classify and route the incoming request to the correct specialist.

        Args:
            session_id: Active session ID.
            text: Input text content.

        Returns:
            Dict containing the specialist execution response.
        """
        specialist_type = self.classify_request(text)
        logger.info(f"Automatically routed request in session {session_id} to {specialist_type} specialist.")

        if specialist_type == "developer":
            return await self.execute_developer_flow(session_id, text)
        else:
            return await self.execute_learner_flow(session_id, text)

    async def execute_learner_flow(self, session_id: str, text: str) -> Dict[str, Any]:
        """Execute the Learning Specialist workflow: Ingest info into memory.

        Args:
            session_id: Active session ID.
            text: Information text to ingest.

        Returns:
            Dict containing Learner result payload.
        """
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
            metadata={"last_learned_text": text, "last_specialist": "learner"}
        )
        return result

    async def execute_developer_flow(self, session_id: str, query: str) -> Dict[str, Any]:
        """Execute the Developer Specialist workflow: Recall and generate answer.

        Args:
            session_id: Active session ID.
            query: Question or code instruction query.

        Returns:
            Dict containing Developer result payload.
        """
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
            metadata={"last_query": query, "last_specialist": "developer"}
        )
        return result

    async def complete_session(self, session_id: str) -> Dict[str, Any]:
        """Complete the session, transitioning status and triggering consolidation.

        Args:
            session_id: The session ID to finalize.

        Returns:
            Dict containing completion status details.
        """
        logger.info(f"Completing session {session_id}")
        session = self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Transition session state (Task 2 / 3)
        self.session_manager.update_session(session_id, status="completed")

        # Trigger lifecycle improvement (Task 5)
        improvement_result = await trigger_end_of_session(session_id)

        return {
            "session_id": session_id,
            "status": "completed",
            "consolidation_status": "triggered",
            "details": str(improvement_result)
        }
