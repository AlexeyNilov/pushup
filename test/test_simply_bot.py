import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, User, Message
from bot.simply import start  # Import your start handler


@pytest.mark.asyncio
async def test_start_command():
    # Step 1: Create mock objects for User, Message, and Update
    user = User(id=123456789, is_bot=False, first_name="TestUser")
    message = MagicMock(spec=Message)
    message.reply_text = AsyncMock()  # Mock reply_text method

    # Step 2: Create a mock Update with the mocked user and message
    update = MagicMock(spec=Update)
    update.effective_user = user
    update.message = message

    # Step 3: Create a mock context (can be empty for now)
    context = MagicMock()

    # Step 4: Call the start handler function
    await start(update, context)

    # Step 5: Assert that reply_text was called with the expected message
    message.reply_text.assert_called_once_with("Hello! You are authorized.")
