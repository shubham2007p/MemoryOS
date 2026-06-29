"""Developer Specialist for MemoryOS.

This specialist queries Cognee memory for context and returns synthesized answers
or generated code using the recalled memories.
"""

import logging
from typing import Any, Dict
from memory.recall import recall_data

logger = logging.getLogger("specialists.developer.workflow")

class DeveloperSpecialist:
    """Specialist responsible for querying memory and generating answers or code."""

    async def resolve_query(self, query: str, session_id: str) -> Dict[str, Any]:
        """Query memory and return a synthesized response.

        Args:
            query: The natural language question or instruction.
            session_id: Active user session ID.

        Returns:
            Dict containing the answer and context used to generate it.
        """
        logger.info(f"DeveloperSpecialist resolving query '{query}' for session {session_id}")
        if not query.strip():
            raise ValueError("Empty query provided to resolve_query")

        # Recall relevant memories from Cognee
        recalled_memories = await recall_data(query=query, session_id=session_id)

        # Format context used
        context_used = []
        for entry in recalled_memories:
            if isinstance(entry, dict):
                context_used.append(entry)
            else:
                context_used.append({
                    "type": type(entry).__name__,
                    "str_val": str(entry)
                })

        # Synthesize answer from recalled facts
        if not context_used:
            answer = "I could not find any relevant memories to answer your question."
        else:
            facts = []
            for ctx in context_used:
                if "text" in ctx:
                    facts.append(ctx["text"])
                elif "str_val" in ctx:
                    facts.append(ctx["str_val"])
                else:
                    facts.append(str(ctx))

            fact_summary = "\n- ".join(facts)
            answer = f"Based on my memory, I found the following relevant facts:\n- {fact_summary}"

        return {
            "answer": answer,
            "context_used": context_used
        }
