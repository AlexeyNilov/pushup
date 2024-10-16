import pytest
from bot.conversation import join_command


@pytest.mark.asyncio
async def test_join_command(msg, update, context):
    # Arrange
    expected_reply = "Hello! Please tell me your age."
    expected_next_state = "ask_age"

    # Act
    result = await join_command(update, context)

    # Assert
    msg.reply_text.assert_called_once_with(expected_reply)
    assert result == expected_next_state
