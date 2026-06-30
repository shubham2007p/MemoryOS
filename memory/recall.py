"""Memory retrieval pipeline for MemoryOS.

This module provides wrappers around Cognee's recall capabilities
to query session cache or the permanent memory graph, applying ranking heuristics
based on recency, importance, and session relevance.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import cognee

logger = logging.getLogger("memory.recall")

async def recall_data(
    query: str,
    session_id: Optional[str] = None,
    **kwargs: Any
) -> List[Any]:
    """Retrieve relevant memories from Cognee.

    Applies custom ranking based on metadata (session relevance, importance, recency).

    Args:
        query: The natural language search query.
        session_id: Optional user session ID.
        **kwargs: Additional parameters for Cognee recall.

    Returns:
        List of matching memory entries sorted by calculated relevance score.
    """
    logger.info(f"Recalling memory for query: '{query}' (session_id={session_id})")
    try:
        # Filter out custom parameters not accepted by Cognee recall API
        cognee_kwargs = {k: v for k, v in kwargs.items() if k not in ["metadata"]}
        results = await cognee.recall(
            query_text=query,
            session_id=session_id,
            **cognee_kwargs
        )

        ranked_results = []
        for entry in results:
            # Normalize entry to a dict or handle object attributes safely
            entry_dict: Dict[str, Any] = {}
            if isinstance(entry, dict):
                entry_dict = entry
            else:
                # Fallback to copy dict if it is a class instance/schema model
                entry_dict = getattr(entry, "__dict__", {})

            # Calculate a custom relevance score
            # Higher score = more relevant
            score = 1.0

            # 1. Session Relevance Boost
            entry_session_id = entry_dict.get("session_id") or entry_dict.get("metadata", {}).get("session_id")
            if session_id and entry_session_id == session_id:
                score += 0.5

            # 2. Importance Boost
            importance = entry_dict.get("importance") or entry_dict.get("metadata", {}).get("importance", "medium")
            if importance == "high":
                score += 0.3
            elif importance == "low":
                score -= 0.2

            # 3. Recency Boost
            timestamp_str = entry_dict.get("timestamp") or entry_dict.get("metadata", {}).get("timestamp")
            if timestamp_str:
                try:
                    ts = datetime.fromisoformat(timestamp_str)
                    age_seconds = (datetime.now(timezone.utc) - ts).total_seconds()
                    # Boost recent memories (e.g. less than 1 hour old)
                    if age_seconds < 3600:
                        score += 0.4
                    elif age_seconds < 86400:
                        score += 0.2
                except Exception:
                    pass

            ranked_results.append((score, entry))

        # Sort entries by score descending
        ranked_results.sort(key=lambda x: x[0], reverse=True)
        final_results = [item[1] for item in ranked_results]

        logger.info(f"Successfully recalled and ranked {len(final_results)} memory entries.")
        return final_results
    except Exception as e:
        logger.error(f"Error in recall_data: {e}")
        raise e
