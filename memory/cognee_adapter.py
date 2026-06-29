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
        await cognee.run_migrations()
        logger.info("Cognee initialization and migrations completed successfully.")
    except Exception as e:
        logger.error(f"Error initializing Cognee: {e}")
        raise e
