from config.settings import settings

def test_settings_load():
    """Verify that settings load with expected defaults."""
    assert settings.db_provider in ["sqlite", "postgres"]
    assert settings.learner_model is not None
    assert settings.developer_model is not None
