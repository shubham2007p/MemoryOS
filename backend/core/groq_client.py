"""Singleton Groq client for MemoryOS.

Provides a centralized, reusable Groq client instance.
All specialists and services should import `get_groq_client()` instead of
creating their own client.
"""

import logging
from groq import Groq
from config.settings import settings

logger = logging.getLogger("backend.core.groq_client")

_groq_client: Groq | None = None


def get_groq_client() -> Groq:
    """Return the singleton Groq client, creating it on first call.

    Returns:
        A configured Groq client instance.

    Raises:
        RuntimeError: If GROQ_API_KEY is not set.
    """
    global _groq_client
    if _groq_client is not None:
        return _groq_client

    if not settings.validate_groq_key():
        raise RuntimeError(
            "Cannot create Groq client: GROQ_API_KEY is missing or placeholder. "
            "Set it in .env or as an environment variable."
        )

    _groq_client = Groq(api_key=settings.groq_api_key)
    logger.info("Groq client initialized successfully.")
    return _groq_client


def check_groq_connectivity() -> dict:
    """Verify Groq API connectivity by listing models.

    Returns:
        Dict with connectivity status and model count.
    """
    try:
        client = get_groq_client()
        models = client.models.list()
        model_ids = [m.id for m in models.data] if hasattr(models, "data") else []
        return {
            "status": "connected",
            "models_available": len(model_ids),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }
