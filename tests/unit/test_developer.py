import pytest
from unittest.mock import AsyncMock, patch
from specialists.developer.workflow import DeveloperSpecialist

@pytest.mark.asyncio
async def test_developer_specialist_success():
    """Verify that DeveloperSpecialist queries recall_data and returns formatted answer."""
    mock_memories = [{"text": "MemoryOS is built on Cognee."}]

    with patch("specialists.developer.workflow.recall_data", return_value=mock_memories) as mock_recall:
        developer = DeveloperSpecialist()
        result = await developer.resolve_query(
            query="What is MemoryOS built on?",
            session_id="session-123"
        )

        mock_recall.assert_called_once_with(
            query="What is MemoryOS built on?",
            session_id="session-123"
        )
        assert "MemoryOS is built on Cognee." in result["answer"]
        assert result["context_used"] == mock_memories
