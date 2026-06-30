"""Developer Specialist for MemoryOS.

This specialist queries Cognee memory for context and returns synthesized answers
or generated code using the recalled memories.
"""

import logging
from typing import Any, Dict
from memory.recall import recall_data
from specialists.developer.config import DEVELOPER_MODEL, TEMPERATURE
from specialists.developer.tools import validate_python_code
from config.prompts import load_specialist_prompt

logger = logging.getLogger("specialists.developer.workflow")

class DeveloperSpecialist:
    """Specialist responsible for querying memory and generating answers or code."""

    def __init__(self) -> None:
        self.model_name = "gemini-2.5-flash"
        self.temperature = TEMPERATURE
        self.system_prompt = load_specialist_prompt("developer")

    async def resolve_query(self, query: str, session_id: str) -> Dict[str, Any]:
        """Query memory and return a synthesized response.

        Args:
            query: The natural language question or instruction.
            session_id: Active user session ID.

        Returns:
            Dict containing the answer, context used, syntax checks, and model settings.
        """
        logger.info(f"DeveloperSpecialist resolving query '{query}' for session {session_id}")
        if not query.strip():
            raise ValueError("Empty query provided to resolve_query")

        search_metadata = {
            "specialist": "developer",
            "session_id": session_id
        }

        # Recall relevant memories from Cognee
        recalled_memories = await recall_data(
            query=query,
            session_id=session_id,
            metadata=search_metadata
        )

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

        # Synthesize answer from recalled facts using centralized Gemini client
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
            
            try:
                from backend.core.gemini_client import get_gemini_model
                import asyncio
                
                model = get_gemini_model("gemini-2.5-flash")
                prompt = (
                    f"System Instructions:\n{self.system_prompt}\n\n"
                    f"User Query: {query}\n\n"
                    f"Recalled Memory Context:\n{fact_summary}\n\n"
                    f"Synthesize a helpful answer based on the recalled memory context. "
                    f"If the context does not contain enough info, politely guide the user."
                )
                
                # Avoid getting stuck by using an async call with a timeout
                response = await asyncio.wait_for(
                    model.generate_content_async(prompt),
                    timeout=10.0
                )
                answer = response.text
            except asyncio.TimeoutError:
                logger.error("DeveloperSpecialist LLM reasoning timed out after 10s")
                answer = f"Synthesizing timed out. Based on my memory, I found the following relevant facts:\n- {fact_summary}"
            except Exception as e:
                logger.error(f"Error in DeveloperSpecialist LLM reasoning: {e}")
                # Fallback to pure memory echo on API failure
                answer = f"Based on my memory, I found the following relevant facts:\n- {fact_summary}"

        # Validate python code syntax if code block is found in answer
        code_valid = None
        if "```python" in answer:
            parts = answer.split("```python")
            if len(parts) > 1:
                code_block = parts[1].split("```")[0]
                code_valid = validate_python_code(code_block)

        # Log memory entry to local SQLite metadata store (Task 2)
        from orchestrator.session_manager import SessionManager
        session_mgr = SessionManager()
        log_res = session_mgr.add_memory_log(
            session_id=session_id,
            specialist="developer",
            text=f"Query: {query} -> Answer: {answer}",
            metadata={
                "query": query,
                "answer": answer,
                "code_syntax_valid": code_valid
            }
        )

        return {
            "answer": answer,
            "context_used": context_used,
            "code_syntax_valid": code_valid,
            "memory_id": log_res["memory_id"],
            "model_metadata": {
                "model_used": self.model_name,
                "temperature": self.temperature,
                "system_prompt_length": len(self.system_prompt)
            }
        }
