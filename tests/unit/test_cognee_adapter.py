import pytest
from memory.cognee_adapter import setup_cognee

@pytest.mark.asyncio
async def test_setup_cognee():
    """Verify that setup_cognee initializes and runs migrations successfully."""
    try:
        await setup_cognee()
    except Exception as e:
        pytest.fail(f"setup_cognee raised an exception: {e}")
