import pytest
from unittest.mock import AsyncMock, patch
from memory.triggers import trigger_manual_remember, trigger_end_of_session

@pytest.mark.asyncio
async def test_trigger_manual_remember():
    """Verify trigger_manual_remember correctly forwards call parameters."""
    with patch("memory.triggers.remember_data", new_callable=AsyncMock) as mock_rem:
        await trigger_manual_remember("some fact", session_id="123")
        mock_rem.assert_called_once_with(
            data="some fact",
            session_id="123",
            metadata={"trigger_type": "manual_remember"}
        )

@pytest.mark.asyncio
async def test_trigger_end_of_session():
    """Verify trigger_end_of_session initiates correct consolidation flow."""
    with patch("memory.triggers.improve_memory", new_callable=AsyncMock) as mock_imp:
        await trigger_end_of_session("session-123")
        mock_imp.assert_called_once_with(session_ids=["session-123"])
