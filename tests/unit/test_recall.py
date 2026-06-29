import pytest
from unittest.mock import AsyncMock, patch
from memory.recall import recall_data

@pytest.mark.asyncio
async def test_recall_data_success():
    """Verify that recall_data successfully forwards calls to cognee.recall."""
    mock_results = [{"text": "Einstein was born in Ulm.", "_source": "graph"}]

    with patch("cognee.recall", return_value=mock_results) as mock_recall:
        result = await recall_data(
            query="Where was Einstein born?",
            session_id="session-999"
        )

        mock_recall.assert_called_once_with(
            query_text="Where was Einstein born?",
            session_id="session-999"
        )
        assert len(result) == 1
        assert result[0]["text"] == "Einstein was born in Ulm."

@pytest.mark.asyncio
async def test_recall_data_failure():
    """Verify that recall_data propagates exceptions raised by cognee.recall."""
    with patch("cognee.recall", side_effect=RuntimeError("Search failed")) as mock_recall:
        with pytest.raises(RuntimeError, match="Search failed"):
            await recall_data("Test search query")
