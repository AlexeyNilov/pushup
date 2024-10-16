import pytest
from bot.conversation import join_bot, start_training_program, receive_max_set


@pytest.mark.asyncio
async def test_join_bot(msg, update, context):
    # Arrange
    expected_reply = "Hello! Please tell me your age."
    expected_next_state = "ask_age"

    # Act
    result = await join_bot(update, context)

    # Assert
    msg.reply_text.assert_called_once_with(expected_reply)
    assert result == expected_next_state


@pytest.mark.asyncio
async def test_start_training_program(msg, update, context):
    await start_training_program(update, context)
    msg.reply_text.assert_called_once_with(
        "Please tell me how much push-ups you can do in one go?"
    )


@pytest.mark.asyncio
async def test_receive_max_set(msg, update, context):
    context.user_data["MAX_SET_COLLECTION"] = True
    update.message.text = "10"
    await receive_max_set(update, context)
    msg.reply_text.assert_called_once_with(
        "Training program activated, call /practice to get recommended workout"
    )
