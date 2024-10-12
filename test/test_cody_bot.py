import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, User, Message

import os

os.environ["PUSHUP_DB_PATH"] = "db/test_empty.sqlite"

from bot import cody as bot
from data.fastlite_db import recreate_db


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
    recreate_db()
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
async def test_stats_command(msg, authorized_update):
    context = MagicMock()
    await bot.stats_for_today(authorized_update, context)
    msg.reply_text.assert_called_once_with("Today sum: 0, max: 0")


@pytest.mark.asyncio
async def test_stats_command_fail(msg, illegal_update):
    context = MagicMock()
    await bot.stats_for_today(illegal_update, context)
    msg.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot."
    )


@pytest.mark.asyncio
async def test_parse_message(msg, authorized_update):
    context = MagicMock()
    authorized_update.message.text = "10"
    await bot.parse_message(authorized_update, context)
    msg.reply_text.assert_called_once_with("Logged 10 push-ups")


@pytest.mark.asyncio
async def test_parse_message_fail(msg, authorized_update):
    context = MagicMock()
    authorized_update.message.text = "test"
    await bot.parse_message(authorized_update, context)
    msg.reply_text.assert_called_once_with("Response is not implemented")


@pytest.mark.asyncio
async def test_record(msg, authorized_update):
    context = MagicMock()
    await bot.stats_all_time(authorized_update, context)
    msg.reply_text.assert_called_once_with("Record set: 0")
