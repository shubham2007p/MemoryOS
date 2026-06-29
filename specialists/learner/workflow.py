"""Learner Specialist for MemoryOS.

This specialist accepts information, extracts structured facts,
and registers them into user session memory via Cognee remember.
"""

import logging
from typing import Any, Dict
from memory.remember import remember_data

logger = logging.getLogger("specialists.learner.workflow")

class LearnerSpecialist:
    """Specialist responsible for parsing raw information and ingesting it into memory."""

    async def learn_fact(self, text: str, session_id: str) -> Dict[str, Any]:
        """Learn a new fact and register it in the session's memory.

        Args:
            text: Raw input information to learn.
            session_id: Active user session ID.

        Returns:
            Dict containing ingestion status and metadata.
        """
        logger.info(f"LearnerSpecialist processing fact for session {session_id}")
        if not text.strip():
            raise ValueError("Empty text provided to learn_fact")

        # Ingest data using the remember pipeline wrapper
        result = await remember_data(
            data=text,
            session_id=session_id
        )

        return {
            "status": "remembered",
            "facts_extracted": [text],
            "details": {
                "elapsed": getattr(result, "elapsed_seconds", 0.0),
                "dataset": getattr(result, "dataset_name", "main_dataset")
            }
        }
