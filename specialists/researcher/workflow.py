"""Research Specialist for MemoryOS.

This specialist queries Cognee memory to extract deep concepts, synthesize relationships,
and write high-quality research insights.
"""

import logging
from typing import Any, Dict
from memory.recall import recall_data
from config.settings import settings
from backend.core.groq_client import get_groq_client

logger = logging.getLogger("specialists.researcher.workflow")

class ResearcherSpecialist:
    """Specialist responsible for deep exploration and synthesis of concepts."""

    def __init__(self) -> None:
        self.model_name = settings.developer_model  # Uses gpt-oss-120b
        self.temperature = 0.4
        self.system_prompt = (
            "You are the Research Specialist for MemoryOS. "
            "Your job is to analyze recalled facts, extract underlying theoretical principles, "
            "and synthesize deep conceptual descriptions. Always highlight cross-domain connections."
        )

    async def run_research(self, query: str, session_id: str) -> Dict[str, Any]:
        """Perform research synthesis based on recalled memories.

        Args:
            query: The research topic or question.
            session_id: Active session ID.

        Returns:
            Dict containing the research results and context.
        """
        logger.info(f"ResearcherSpecialist running research for topic: '{query}'")

        # Recall memories from Cognee
        recalled_memories = await recall_data(
            query=query,
            session_id=session_id
        )

        context_used = []
        facts = []
        for entry in recalled_memories:
            if isinstance(entry, dict):
                context_used.append(entry)
                facts.append(entry.get("text", str(entry)))
            else:
                context_used.append({"type": type(entry).__name__, "str_val": str(entry)})
                facts.append(str(entry))

        fact_summary = "\n- ".join(facts) if facts else "No specific project memory found."

        try:
            client = get_groq_client()
            messages = [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Research Topic: {query}\n\n"
                        f"Recalled Context:\n{fact_summary}\n\n"
                        f"Write a deep, analytical summary exploring the topic, grounding it in the recalled facts."
                    )
                }
            ]

            completion = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature
            )
            answer = completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in ResearcherSpecialist LLM reasoning: {e}")
            answer = f"### Research Insights (Fallback)\nBased on context: {fact_summary}"

        # Log memory entry to SQLite metadata store
        from orchestrator.session_manager import SessionManager
        session_mgr = SessionManager()
        log_res = session_mgr.add_memory_log(
            session_id=session_id,
            specialist="researcher",
            text=f"Research: {query} -> Result: {answer}",
            metadata={
                "query": query,
                "answer": answer
            }
        )

        return {
            "answer": answer,
            "context_used": context_used,
            "memory_id": log_res["memory_id"],
            "model_metadata": {
                "model_used": self.model_name,
                "temperature": self.temperature
            }
        }
