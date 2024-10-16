import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Chat, User, Message
from telegram.ext import ContextTypes
from bot.command import set_timer
from data.fastlite_db import recreate_db
from service.repo import update_profile


@pytest.fixture
def authorized_user() -> User:
    return User(id=123456789, is_bot=False, first_name="TestUser")


@pytest.fixture
def update(authorized_user) -> MagicMock:
    recreate_db()
    update_profile({"user_id": 123456789})
    upd = MagicMock(spec=Update)
    upd.effective_user = authorized_user
    upd.effective_message = AsyncMock(spec=Message)
    upd.effective_chat.type = Chat.PRIVATE
    return upd


@pytest.fixture
def context():
    ctx = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    ctx.job_queue = MagicMock()
    ctx.job_queue.run_once = MagicMock()
    ctx.job_queue.get_jobs_by_name = MagicMock(return_value=[])
    return ctx


@pytest.mark.asyncio
async def test_set_timer(update, context):
    # Act
    await set_timer(update, context)

    # Assert
    context.job_queue.run_once.assert_called_once()
    job_args = context.job_queue.run_once.call_args[0]
    job_kwargs = context.job_queue.run_once.call_args[1]

    assert job_args[1] == 60.0  # Check if the timer is set for 60 seconds
    assert job_kwargs["data"] == 60.0

    update.effective_message.reply_text.assert_called_once_with(
        "Timer successfully set!"
    )


@pytest.mark.asyncio
async def test_set_timer_removes_existing_job(update, context):
    # Arrange
    existing_job = MagicMock()
    context.job_queue.get_jobs_by_name.return_value = [existing_job]

    # Act
    await set_timer(update, context)

    # Assert
    existing_job.schedule_removal.assert_called_once()

    context.job_queue.run_once.assert_called_once()
    update.effective_message.reply_text.assert_called_once_with(
        "Timer successfully set!"
    )
