import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, User, Message
from sample import filter_user as bot


@pytest.fixture
def authorized_user():
    return User(id=123456789, is_bot=False, first_name="TestUser")


@pytest.fixture
def illegal_user():
    return User(id=111111111, is_bot=False, first_name="TestUser")


@pytest.fixture
def msg():
    message = MagicMock(spec=Message)
    message.reply_text = AsyncMock()
    return message


@pytest.fixture
def authorized_update(authorized_user, msg):
    upd = MagicMock(spec=Update)
    upd.effective_user = authorized_user
    upd.message = msg
    return upd


@pytest.fixture
def illegal_update(illegal_user, msg):
    upd = MagicMock(spec=Update)
    upd.effective_user = illegal_user
    upd.message = msg
    return upd


@pytest.mark.asyncio
async def test_start_command(msg, authorized_update):
    context = MagicMock()
    await bot.start(authorized_update, context)
    msg.reply_text.assert_called_once_with("Hello! You are authorized.")


@pytest.mark.asyncio
async def test_start_command_fail(msg, illegal_update):
    context = MagicMock()
    await bot.start(illegal_update, context)
    msg.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot."
    )
