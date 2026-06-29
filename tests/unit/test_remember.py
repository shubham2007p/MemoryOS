import pytest
from unittest.mock import AsyncMock, patch
from memory.remember import remember_data

@pytest.mark.asyncio
async def test_remember_data_success():
    """Verify that remember_data successfully forwards calls to cognee.remember."""
    mock_result = AsyncMock()
    mock_result.status = "completed"

    with patch("cognee.remember", return_value=mock_result) as mock_remember:
        result = await remember_data(
            data="Test information about MemoryOS",
            dataset_name="test_dataset",
            session_id="session-999"
        )

        mock_remember.assert_called_once_with(
            data="Test information about MemoryOS",
            dataset_name="test_dataset",
            session_id="session-999"
        )
        assert result.status == "completed"

@pytest.mark.asyncio
async def test_remember_data_failure():
    """Verify that remember_data propagates exceptions raised by cognee.remember."""
    with patch("cognee.remember", side_effect=RuntimeError("API Error")) as mock_remember:
        with pytest.raises(RuntimeError, match="API Error"):
            await remember_data("Test failed data")
