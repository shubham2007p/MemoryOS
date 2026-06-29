"""Memory evolution / improvement pipeline for MemoryOS.

This module wraps Cognee's improve functionality, allowing session feedback,
Q&A histories, and distilled learnings to be consolidated back into the permanent graph.
"""

import logging
from typing import Any, Optional, List
import cognee

logger = logging.getLogger("memory.improve")

async def improve_memory(
    dataset_name: str = "main_dataset",
    session_ids: Optional[List[str]] = None,
    **kwargs: Any
) -> Any:
    """Consolidate, summarize, and enrich memory elements in Cognee.

    If session_ids is provided, it bridges user session metadata and Q&A content
    into the permanent knowledge graph, updating node/edge feedback weights.

    Args:
        dataset_name: Dataset name or UUID to process. Defaults to "main_dataset".
        session_ids: Optional list of session IDs whose feedback/Q&A should be consolidated.
        **kwargs: Additional parameters for Cognee improve.

    Returns:
        The pipeline run info.
    """
    logger.info(f"Improving memory for dataset '{dataset_name}' (session_ids={session_ids})")
    try:
        result = await cognee.improve(
            dataset=dataset_name,
            session_ids=session_ids,
            **kwargs
        )
        logger.info("Successfully completed memory improvement pipeline.")
        return result
    except Exception as e:
        logger.error(f"Error in improve_memory: {e}")
        raise e
