"""Prompts configuration and dynamic loaders for MemoryOS specialists."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_specialist_prompt(specialist_name: str) -> str:
    """Load the prompt.md file for the given specialist.

    If the file does not exist, a sensible default string is returned.

    Args:
        specialist_name: Directory name of the specialist under specialists/.

    Returns:
        The content of prompt.md or a fallback default prompt.
    """
    prompt_path = BASE_DIR / "specialists" / specialist_name / "prompt.md"
    if prompt_path.exists():
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass

    # Default fallback prompts if prompt.md is missing or unreadable
    if specialist_name == "learner":
        return (
            "You are the Learning Specialist. Analyze the user's input, "
            "and extract clean, structured facts and concepts. "
            "Filter out conversational filler."
        )
    elif specialist_name == "developer":
        return (
            "You are the Developer Specialist. Use the recalled context "
            "from persistent memory to formulate accurate answers, explanations, "
            "or code. If the recalled context is insufficient, state that."
        )
    return "You are a MemoryOS specialist reasoning system."
