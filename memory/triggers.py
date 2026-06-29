"""Memory lifecycle triggers for MemoryOS.

This module provides handlers that automatically orchestrate the lifecycle
of memory (ingesting session cache, consolidating cache to graph, and scheduled refinement).
"""

import logging
from typing import Any, Optional
from memory.remember import remember_data
from memory.improve import improve_memory

logger = logging.getLogger("memory.triggers")

async def trigger_manual_remember(data: str, session_id: Optional[str] = None) -> Any:
    """Manually ingest a fact or statement into the memory system."""
    logger.info("Executing manual remember trigger")
    return await remember_data(
        data=data,
        session_id=session_id,
        metadata={"trigger_type": "manual_remember"}
    )

async def trigger_end_of_session(session_id: str) -> Any:
    """Consolidate all session-cache facts into the permanent knowledge graph.

    This is triggered automatically when a session is set to completed.
    """
    logger.info(f"Executing end-of-session memory trigger for session: {session_id}")
    # Call improve_memory for this session to bridge it into the permanent graph
    return await improve_memory(session_ids=[session_id])

async def trigger_completed_learning(dataset_name: str = "main_dataset") -> Any:
    """Trigger graph consolidation after learning is complete."""
    logger.info(f"Executing completed learning trigger for dataset: {dataset_name}")
    return await improve_memory(dataset_name=dataset_name)

async def trigger_scheduled_improvement(dataset_name: str = "main_dataset") -> Any:
    """Trigger scheduled overall graph optimization and embedding refinement."""
    logger.info(f"Executing scheduled improvement trigger for dataset: {dataset_name}")
    return await improve_memory(
        dataset_name=dataset_name,
        build_global_context_index=True
    )
