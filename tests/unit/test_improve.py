import pytest
from unittest.mock import AsyncMock, patch
from memory.improve import improve_memory

@pytest.mark.asyncio
async def test_improve_memory_success():
    """Verify that improve_memory successfully forwards calls to cognee.improve."""
    mock_info = {"status": "success"}

    with patch("cognee.improve", return_value=mock_info) as mock_improve:
        result = await improve_memory(
            dataset_name="test_dataset",
            session_ids=["session-1", "session-2"]
        )

        mock_improve.assert_called_once_with(
            dataset="test_dataset",
            session_ids=["session-1", "session-2"]
        )
        assert result == mock_info

@pytest.mark.asyncio
async def test_improve_memory_failure():
    """Verify that improve_memory propagates exceptions raised by cognee.improve."""
    with patch("cognee.improve", side_effect=RuntimeError("Improvement failed")) as mock_improve:
        with pytest.raises(RuntimeError, match="Improvement failed"):
            await improve_memory("test_dataset")
