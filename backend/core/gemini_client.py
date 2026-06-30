"""Singleton Gemini client for MemoryOS.

Provides a centralized, reusable Gemini client instance/configuration.
"""

import logging
import google.generativeai as genai
from config.settings import settings

logger = logging.getLogger("backend.core.gemini_client")

_gemini_configured = False


def configure_gemini() -> None:
    """Configure the google-generativeai package with the settings API key."""
    global _gemini_configured
    if _gemini_configured:
        return

    if not settings.gemini_api_key or settings.gemini_api_key.startswith("your_"):
        raise RuntimeError(
            "Cannot configure Gemini client: GEMINI_API_KEY is missing or placeholder. "
            "Set it in .env or as an environment variable."
        )

    genai.configure(api_key=settings.gemini_api_key)
    _gemini_configured = True
    logger.info("Gemini client initialized and configured successfully.")


def get_gemini_model(model_name: str = "gemini-1.5-flash") -> genai.GenerativeModel:
    """Get a GenerativeModel instance for the specified model name."""
    configure_gemini()
    return genai.GenerativeModel(model_name)


def check_gemini_connectivity() -> dict:
    """Verify Gemini API connectivity by generating a simple test completion.

    Returns:
        Dict with connectivity status.
    """
    try:
        model = get_gemini_model()
        response = model.generate_content("ping")
        if response.text:
            return {
                "status": "connected",
                "message": "Gemini API successfully connected."
            }
        return {
            "status": "error",
            "error": "No response text received from Gemini API."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }
