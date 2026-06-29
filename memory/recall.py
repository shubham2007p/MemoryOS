"""Memory retrieval pipeline for MemoryOS.

This module provides wrappers around Cognee's recall capabilities
to query session cache or the permanent memory graph.
"""

import logging
from typing import Any, Optional, List
import cognee

logger = logging.getLogger("memory.recall")

async def recall_data(
    query: str,
    session_id: Optional[str] = None,
    **kwargs: Any
) -> List[Any]:
    """Retrieve relevant memories from Cognee.

    If session_id is provided, it searches session cache directly.
    Otherwise, it queries the permanent knowledge graph.

    Args:
        query: The natural language search query.
        session_id: Optional user session ID.
        **kwargs: Additional parameters for Cognee recall.

    Returns:
        List of matching memory entries.
    """
    logger.info(f"Recalling memory for query: '{query}' (session_id={session_id})")
    try:
        results = await cognee.recall(
            query_text=query,
            session_id=session_id,
            **kwargs
        )
        logger.info(f"Successfully recalled {len(results)} memory entries.")
        return results
    except Exception as e:
        logger.error(f"Error in recall_data: {e}")
        raise e
