"""Learner Specialist for MemoryOS.

This specialist accepts information, extracts structured facts,
and registers them into user session memory via Cognee remember.
"""

import logging
from typing import Any, Dict
from memory.remember import remember_data
from specialists.learner.config import LEARNER_MODEL, TEMPERATURE
from specialists.learner.tools import clean_input_text, count_approximate_tokens
from config.prompts import load_specialist_prompt

logger = logging.getLogger("specialists.learner.workflow")

class LearnerSpecialist:
    """Specialist responsible for parsing raw information and ingesting it into memory."""

    def __init__(self) -> None:
        self.model_name = LEARNER_MODEL
        self.temperature = TEMPERATURE
        self.system_prompt = load_specialist_prompt("learner")

    async def learn_fact(self, text: str, session_id: str) -> Dict[str, Any]:
        """Learn a new fact and register it in the session's memory.

        Args:
            text: Raw input information to learn.
            session_id: Active user session ID.

        Returns:
            Dict containing ingestion status and metadata.
        """
        logger.info(f"LearnerSpecialist processing fact for session {session_id}")
        cleaned_text = clean_input_text(text)
        if not cleaned_text:
            raise ValueError("Empty text provided to learn_fact")

        token_count = count_approximate_tokens(cleaned_text)

        # Better metadata extraction: scan for technical context keywords (Milestone 7)
        critical_keywords = ["fastapi", "cognee", "database", "sqlite", "groq", "gemini", "setup", "config", "model", "always", "must", "critical"]
        text_lower = cleaned_text.lower()
        is_critical = any(kw in text_lower for kw in critical_keywords)
        importance_level = "high" if is_critical or token_count > 15 else "medium"

        # Structured metadata for the ingested memory
        metadata = {
            "source": "user_input",
            "specialist": "learner",
            "importance": importance_level,
            "confidence": 1.0 if is_critical else 0.85,
            "session_id": session_id,
            "topics": [kw for kw in critical_keywords if kw in text_lower]
        }

        # Ingest data using the remember pipeline wrapper
        result = await remember_data(
            data=cleaned_text,
            session_id=session_id,
            custom_prompt=self.system_prompt,
            metadata=metadata
        )

        # Log memory entry to local SQLite metadata store (Task 2)
        from orchestrator.session_manager import SessionManager
        session_mgr = SessionManager()
        log_res = session_mgr.add_memory_log(
            session_id=session_id,
            specialist="learner",
            text=cleaned_text,
            metadata=metadata
        )

        return {
            "status": "remembered",
            "facts_extracted": [cleaned_text],
            "memory_id": log_res["memory_id"],
            "details": {
                "elapsed": getattr(result, "elapsed_seconds", 0.0),
                "dataset": getattr(result, "dataset_name", "main_dataset"),
                "token_estimate": token_count,
                "metadata": metadata
            }
        }
