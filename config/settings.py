"""Settings and environment configuration for MemoryOS."""

import sys
import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("config.settings")

class Settings(BaseSettings):
    """MemoryOS global configurations loaded from environment or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # LLM API keys
    groq_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

    # Cognee Database & Vector Store Settings
    cognee_api_key: Optional[str] = None
    db_provider: str = "sqlite"
    vector_db_provider: str = "lancedb"
    graph_db_provider: str = "kuzu"

    # Specialist LLM model mapping defaults
    planner_model: str = "openai/gpt-oss-120b"
    developer_model: str = "openai/gpt-oss-120b"
    learner_model: str = "qwen/qwen3-32b"
    classifier_model: str = "qwen/qwen3-32b"

    def validate_groq_key(self) -> bool:
        """Check that GROQ_API_KEY is set and non-placeholder."""
        if not self.groq_api_key or self.groq_api_key.startswith("your_"):
            return False
        return True

# Instantiate settings singleton
settings = Settings()


def verify_settings_on_startup() -> None:
    """Verify critical settings at startup. Logs model config, exits on fatal errors."""
    if not settings.validate_groq_key():
        logger.critical(
            "GROQ_API_KEY is missing or still set to placeholder. "
            "Set it in .env or as an environment variable."
        )
        sys.exit(1)

    logger.info("--- MemoryOS Configuration ---")
    logger.info(f"  Planner model    : {settings.planner_model}")
    logger.info(f"  Developer model  : {settings.developer_model}")
    logger.info(f"  Learner model    : {settings.learner_model}")
    logger.info(f"  Classifier model : {settings.classifier_model}")
    logger.info(f"  DB provider      : {settings.db_provider}")
    logger.info(f"  Vector DB        : {settings.vector_db_provider}")
    logger.info(f"  Graph DB         : {settings.graph_db_provider}")
    logger.info(f"  GROQ_API_KEY     : ...{settings.groq_api_key[-6:]}")
    logger.info("--- Configuration OK ---")
