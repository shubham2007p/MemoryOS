"""Planner Specialist for MemoryOS.

This specialist queries Cognee memory for context and returns a structured step-by-step
implementation plan or roadmap based on recalled facts.
"""

import logging
from typing import Any, Dict
from memory.recall import recall_data
from config.settings import settings
from config.prompts import load_specialist_prompt
from backend.core.groq_client import get_groq_client

logger = logging.getLogger("specialists.planner.workflow")

class PlannerSpecialist:
    """Specialist responsible for organizing memories into execution plans."""

    def __init__(self) -> None:
        self.model_name = settings.developer_model  # Uses planner_model default
        self.temperature = 0.2
        # Fallback default prompt if custom markdown file is skeleton
        self.system_prompt = (
            "You are the Planner Specialist for MemoryOS. "
            "Your job is to organize recalled notes, system designs, and code snippets "
            "into structured, step-by-step execution plans or roadmaps."
        )

    async def generate_plan(self, query: str, session_id: str) -> Dict[str, Any]:
        """Recall context and generate a step-by-step roadmap.

        Args:
            query: User's goal or plan objective.
            session_id: Active user session ID.

        Returns:
            Dict containing the plan markdown answer and retrieved context.
        """
        logger.info(f"PlannerSpecialist generating plan for objective: '{query}'")
        
        # Recall relevant memories from Cognee
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
                        f"User Goal: {query}\n\n"
                        f"Recalled Context:\n{fact_summary}\n\n"
                        f"Generate a clear, step-by-step execution plan or checklist to achieve the goal based on the context."
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
            logger.error(f"Error in PlannerSpecialist LLM generation: {e}")
            answer = f"### Step-by-Step Plan (Fallback)\nBased on context: {fact_summary}"

        # Log memory entry to SQLite metadata store
        from orchestrator.session_manager import SessionManager
        session_mgr = SessionManager()
        log_res = session_mgr.add_memory_log(
            session_id=session_id,
            specialist="planner",
            text=f"Plan: {query} -> Result: {answer}",
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
