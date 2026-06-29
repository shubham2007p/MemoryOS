"""Settings and environment configuration for MemoryOS."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    learner_model: str = "groq/llama3-8b-8192"
    developer_model: str = "groq/llama3-70b-8192"
    classifier_model: str = "groq/llama3-8b-8192"

# Instantiate settings singleton
settings = Settings()
