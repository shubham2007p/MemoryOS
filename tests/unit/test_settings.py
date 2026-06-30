"""Tests for settings loading and validation."""

from unittest.mock import patch
from config.settings import Settings, settings


def test_settings_load():
    """Verify that settings load with expected defaults."""
    assert settings.db_provider in ["sqlite", "postgres"]
    assert settings.learner_model is not None
    assert settings.developer_model is not None


def test_settings_new_model_defaults():
    """Verify the updated model mappings are correctly set."""
    assert settings.planner_model == "openai/gpt-oss-120b"
    assert settings.developer_model == "openai/gpt-oss-120b"
    assert settings.learner_model == "qwen/qwen3-32b"
    assert settings.classifier_model == "qwen/qwen3-32b"


def test_validate_groq_key_with_real_key():
    """Verify that validate_groq_key returns True when a real key is set."""
    s = Settings(groq_api_key="gsk_realkey123")
    assert s.validate_groq_key() is True


def test_validate_groq_key_placeholder():
    """Verify that validate_groq_key returns False for placeholder keys."""
    s = Settings(groq_api_key="your_groq_key_here")
    assert s.validate_groq_key() is False


def test_validate_groq_key_missing():
    """Verify that validate_groq_key returns False when key is None."""
    s = Settings(groq_api_key=None)
    assert s.validate_groq_key() is False
