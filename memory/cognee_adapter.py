"""Cognee adapter for MemoryOS.

This module configures Cognee and initializes the persistent memory graph
by running necessary migrations.
"""

import os
import logging
from dotenv import load_dotenv
import cognee

logger = logging.getLogger("memory.cognee_adapter")

async def setup_cognee() -> None:
    """Initialize Cognee settings and run database migrations."""
    load_dotenv()
    
    # Run migrations to initialize Cognee database schemas and vector store prerequisites
    logger.info("Initializing Cognee memory database and running migrations...")
    try:
        # Load API keys from environment settings
        from config.settings import settings
        
        # Configure Cognee to use Groq for reasoning
        cognee.config.set_llm_provider("groq")
        cognee.config.set_llm_api_key(settings.groq_api_key)
        
        # Configure Cognee to use Gemini for embeddings (non-OpenAI setup)
        cognee.config.set_embedding_provider("gemini")
        cognee.config.set_embedding_api_key(settings.gemini_api_key)
        
        await cognee.run_migrations()
        logger.info("Cognee initialization and migrations completed successfully.")
    except Exception as e:
        logger.error(f"Error initializing Cognee: {e}")
        raise e
