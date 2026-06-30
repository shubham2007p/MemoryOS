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

        # Direct SQLite recall fallback/complement
        import sqlite3
        import json
        from orchestrator.session_manager import DB_PATH

        sqlite_memories = []
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                if session_id:
                    cursor.execute(
                        "SELECT memory_id, specialist, text, metadata_json FROM memories WHERE session_id = ?",
                        (session_id,)
                    )
                else:
                    cursor.execute("SELECT memory_id, specialist, text, metadata_json FROM memories")
                rows = cursor.fetchall()
                for r in rows:
                    sqlite_memories.append({
                        "memory_id": r[0],
                        "specialist": r[1],
                        "text": r[2],
                        "metadata": json.loads(r[3])
                    })
        except Exception as sqle:
            logger.error(f"Failed to query SQLite memories: {sqle}")

        sqlite_permanent = []
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT node_id, label, type, text FROM permanent_nodes")
                rows = cursor.fetchall()
                for r in rows:
                    sqlite_permanent.append({
                        "node_id": r[0],
                        "label": r[1],
                        "type": r[2],
                        "text": r[3] or ""
                    })
        except Exception as sqle:
            logger.error(f"Failed to query SQLite permanent nodes: {sqle}")

        # Compute keyword overlap score
        query_words = [w.strip(".,?!();:\"'").lower() for w in query.split()]
        stop_words = {
            "what", "is", "who", "the", "a", "an", "and", "or", "in", "on", "at", "for", "to", "of", "with", "about", 
            "are", "you", "to", "be", "was", "were", "has", "have", "had", "been", "will", "would", 
            "shall", "should", "can", "could", "may", "might", "must", "us", "we", "i", "my", "me", 
            "he", "she", "they", "them", "it", "its", "their", "his", "her", "as", "by", "from", "into",
            "out", "over", "under", "again", "then", "once", "here", "there", "when", "where", "why", 
            "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", 
            "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", 
            "just", "don", "should", "now", "using", "used", "make", "made", "does", "do", "did"
        }
        query_keywords = {w for w in query_words if w not in stop_words and len(w) > 2}

        extra_results = []
        for mem in sqlite_memories:
            mem_text = mem["text"]
            mem_words = {w.strip(".,?!();:\"'").lower() for w in mem_text.split()}
            overlap = len(query_keywords.intersection(mem_words)) if query_keywords else 0
            if overlap > 0 or not query_keywords:
                score = 1.0 + overlap * 0.5
                extra_results.append((score, {
                    "memory_id": mem["memory_id"],
                    "text": mem_text,
                    "specialist": mem["specialist"],
                    "metadata": mem["metadata"]
                }))

        for node in sqlite_permanent:
            node_label = node["label"]
            node_text = node["text"]
            combined_text = f"{node_label} {node_text}"
            node_words = {w.strip(".,?!();:\"'").lower() for w in combined_text.split()}
            overlap = len(query_keywords.intersection(node_words)) if query_keywords else 0
            if overlap > 0 or not query_keywords:
                score = 1.0 + overlap * 0.5
                extra_results.append((score, {
                    "node_id": node["node_id"],
                    "text": f"Concept: {node_label} ({node['type']}) - {node_text}" if node_text else f"Concept: {node_label} ({node['type']})",
                    "specialist": "permanent_store",
                    "metadata": {"label": node_label, "type": node["type"]}
                }))

        # Merge, sort and deduplicate
        combined_ranked = ranked_results + extra_results
        combined_ranked.sort(key=lambda x: x[0], reverse=True)
        
        seen_texts = set()
        deduped_results = []
        for score, item in combined_ranked:
            text_val = ""
            if isinstance(item, dict):
                text_val = item.get("text", "")
            else:
                text_val = getattr(item, "text", getattr(item, "__dict__", {}).get("text", str(item)))
            
            if text_val not in seen_texts:
                seen_texts.add(text_val)
                deduped_results.append(item)

        logger.info(f"Successfully recalled and ranked {len(deduped_results)} memory entries.")
        return deduped_results
    except Exception as e:
        logger.error(f"Error in recall_data: {e}")
        raise e
