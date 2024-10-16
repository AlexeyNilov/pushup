import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram.ext import ConversationHandler
from bot import common
from telegram.constants import ParseMode
from conf.settings import DEVELOPER_CHAT_ID


@pytest.mark.asyncio
async def test_alarm(context):
    context.job = MagicMock()
    context.job.chat_id = 123456
    context.job.data = 10
    context.bot.send_message = AsyncMock()

    await common.alarm(context)

    context.bot.send_message.assert_called_once_with(
        chat_id=123456, text="Beep! 10 seconds are over!"
    )


def test_remove_job_if_exists(context):
    job_name = "test_job"
    mock_job = MagicMock()
    context.job_queue.get_jobs_by_name.return_value = [mock_job]

    result = common.remove_job_if_exists(job_name, context)

    assert result is True
    mock_job.schedule_removal.assert_called_once()


def test_remove_job_if_exists_no_job(context):
    job_name = "non_existent_job"
    context.job_queue.get_jobs_by_name.return_value = []

    result = common.remove_job_if_exists(job_name, context)

    assert result is False


@pytest.mark.asyncio
async def test_cancel(update, context):
    result = await common.cancel(update, context)

    update.message.reply_text.assert_called_once_with("Okay, conversation cancelled.")
    assert result == ConversationHandler.END


@pytest.mark.asyncio
async def test_error_handler(update, context):
    context.error = Exception("Test error")
    context.bot.send_message = AsyncMock()

    # Mock the update.to_dict() method to return a serializable object
    update.to_dict = MagicMock(return_value={"update_id": 123456})

    await common.error_handler(update, context)

    context.bot.send_message.assert_called_once()
    args, kwargs = context.bot.send_message.call_args
    assert kwargs["chat_id"] == DEVELOPER_CHAT_ID
    assert "Test error" in kwargs["text"]
    assert kwargs["parse_mode"] == ParseMode.HTML

    # Additional assertions to check for serializable content
    assert "123456" in kwargs["text"]


@pytest.mark.asyncio
async def test_authorized_only_decorator(update, context):
    @common.authorized_only
    async def test_handler(update, context):
        return "Success"

    result = await test_handler(update, context)

    assert result == "Success"


@pytest.mark.asyncio
async def test_authorized_only_decorator_unauthorized(illegal_update, context):
    @common.authorized_only
    async def test_handler(update, context):
        return "Success"

    await test_handler(illegal_update, context)

    illegal_update.message.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot, /join first"
    )


@pytest.mark.asyncio
async def test_authorized_only_decorator_non_private_chat(update, context):
    update.effective_chat.type = "group"

    @common.authorized_only
    async def test_handler(update, context):
        return "Success"

    await test_handler(update, context)

    update.message.reply_text.assert_called_once_with("Please use private chat.")
