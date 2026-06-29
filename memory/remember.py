"""Memory ingestion pipeline for MemoryOS.

This module provides wrappers around Cognee's remember capabilities
to ingest text or structured data into either session memory or permanent memory
along with relevant context metadata.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import cognee

logger = logging.getLogger("memory.remember")

async def remember_data(
    data: str,
    dataset_name: str = "main_dataset",
    session_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    **kwargs: Any
) -> Any:
    """Ingest data into Cognee memory.

    If session_id is provided, it stores data in the session cache.
    Otherwise, it builds/adds to the permanent knowledge graph.

    Args:
        data: The text content to store.
        dataset_name: Target dataset. Defaults to "main_dataset".
        session_id: Optional user session ID.
        metadata: Custom metadata dictionary (timestamp, source, specialist, etc.).
        **kwargs: Additional parameters for Cognee remember.

    Returns:
        The result of the remember operation.
    """
    logger.info(f"Remembering data (preview: '{data[:60]}...') in dataset '{dataset_name}' (session_id={session_id})")

    # Enforce and enrich metadata (Task 4)
    enriched_metadata = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "source": "api_call",
        "importance": "medium",
        "confidence": 1.0,
        **(metadata or {})
    }

    try:
        result = await cognee.remember(
            data=data,
            dataset_name=dataset_name,
            session_id=session_id,
            **kwargs
        )
        logger.info(f"Successfully triggered remember: status={getattr(result, 'status', 'N/A')}")
        return result
    except Exception as e:
        logger.error(f"Error in remember_data: {e}")
        raise e
