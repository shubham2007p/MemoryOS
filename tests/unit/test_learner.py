import pytest
from unittest.mock import AsyncMock, patch
from specialists.learner.workflow import LearnerSpecialist

@pytest.mark.asyncio
async def test_learner_specialist_success():
    """Verify that LearnerSpecialist properly triggers remember_data."""
    mock_result = AsyncMock()
    mock_result.elapsed_seconds = 1.5
    mock_result.dataset_name = "test_dataset"

    with patch("specialists.learner.workflow.remember_data", return_value=mock_result) as mock_remember:
        learner = LearnerSpecialist()
        result = await learner.learn_fact(
            text="MemoryOS is built on Cognee.",
            session_id="session-123"
        )

        mock_remember.assert_called_once()
        called_kwargs = mock_remember.call_args[1]
        assert called_kwargs["data"] == "MemoryOS is built on Cognee."
        assert called_kwargs["session_id"] == "session-123"
        assert "metadata" in called_kwargs
        assert "custom_prompt" in called_kwargs
        assert result["status"] == "remembered"
        assert result["facts_extracted"] == ["MemoryOS is built on Cognee."]
        assert result["details"]["dataset"] == "test_dataset"
