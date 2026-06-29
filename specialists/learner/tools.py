"""Helper tools for the Learner Specialist."""

import re

def clean_input_text(text: str) -> str:
    """Preprocess and clean input text to remove extra whitespace and noise."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def count_approximate_tokens(text: str) -> int:
    """Provide a simple word-based token count estimation."""
    return len(text.split())
