import pytest
from sample import filter_user as bot


@pytest.mark.asyncio
async def test_start_command(msg, update, context):
    await bot.start(update, context)
    msg.reply_text.assert_called_once_with("Hello! You are authorized.")


@pytest.mark.asyncio
async def test_start_command_fail(msg, illegal_update, context):
    await bot.start(illegal_update, context)
    msg.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot."
    )
