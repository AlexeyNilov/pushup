import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, User, Message, Chat

import os

os.environ["PUSHUP_DB_PATH"] = "db/test_empty.sqlite"

from bot import cody as bot
from bot.conversation import receive_max_set, start_training_program
from data.fastlite_db import recreate_db
from service.repo import update_profile


@pytest.fixture
def authorized_user() -> User:
    return User(id=123456789, is_bot=False, first_name="TestUser")


@pytest.fixture
def illegal_user() -> User:
    return User(id=111111111, is_bot=False, first_name="TestUser")


@pytest.fixture
def msg() -> MagicMock:
    message = MagicMock(spec=Message)
    message.reply_text = AsyncMock()
    return message


@pytest.fixture
def authorized_update(authorized_user, msg) -> MagicMock:
    recreate_db()
    update_profile({"user_id": 123456789})
    upd = MagicMock(spec=Update)
    upd.effective_user = authorized_user
    upd.message = msg
    upd.effective_chat.type = Chat.PRIVATE
    return upd


@pytest.fixture
def illegal_update(illegal_user, msg) -> MagicMock:
    upd = MagicMock(spec=Update)
    upd.effective_user = illegal_user
    upd.message = msg
    upd.effective_chat.type = Chat.PRIVATE
    return upd


@pytest.fixture
def context() -> MagicMock:
    return MagicMock()


@pytest.mark.asyncio
async def test_stats_command(msg, authorized_update, context):
    await bot.stats_for_today(authorized_update, context)
    msg.reply_text.assert_called_once_with("Today sum: 0, max: 0")


@pytest.mark.asyncio
async def test_stats_command_fail(msg, illegal_update, context):
    await bot.stats_for_today(illegal_update, context)
    msg.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot, /join first"
    )


@pytest.mark.asyncio
async def test_parse_message(msg, authorized_update, context):
    authorized_update.message.text = "10"
    await bot.parse_message(authorized_update, context)
    msg.reply_text.assert_any_call("Logged 10 push-ups")
    msg.reply_text.assert_any_call("Good job!")
    authorized_update.message.text = "5"
    await bot.parse_message(authorized_update, context)
    msg.reply_text.assert_any_call("Logged 5 push-ups")


@pytest.mark.asyncio
async def test_parse_message_race(msg, authorized_update, context):
    authorized_update.message.text = "10"
    await receive_max_set(authorized_update, context)
    await bot.parse_message(authorized_update, context)
    msg.reply_text.assert_any_call("Logged 10 push-ups")


@pytest.mark.asyncio
async def test_parse_message_fail(msg, authorized_update, context):
    authorized_update.message.text = "test"
    await bot.parse_message(authorized_update, context)
    msg.reply_text.assert_not_called()


@pytest.mark.asyncio
async def test_record(msg, authorized_update, context):
    await bot.stats_all_time(authorized_update, context)
    msg.reply_text.assert_called_once_with("Record set: 0, sum per day: 0")


@pytest.mark.asyncio
async def test_get_practice(msg, authorized_update, context):
    await bot.get_practice(authorized_update, context)
    msg.reply_html.assert_called()
    # msg.reply_html.assert_any_call("")


@pytest.mark.asyncio
async def test_start_training_program(msg, authorized_update, context):
    await start_training_program(authorized_update, context)
    msg.reply_text.assert_called_once_with(
        "Please tell me how much push-ups you can do in one go?"
    )


@pytest.mark.asyncio
async def test_complete_workout(msg, authorized_update, context):
    await bot.complete_workout(authorized_update, context)
    msg.reply_text.assert_called_once_with("Workout completed!")


@pytest.mark.asyncio
async def test_receive_max_set(msg, authorized_update, context):
    context.user_data["MAX_SET_COLLECTION"] = True
    authorized_update.message.text = "10"
    await receive_max_set(authorized_update, context)
    msg.reply_text.assert_called_once_with(
        "Training program activated, call /practice to get recommended workout"
    )


@pytest.mark.asyncio
async def test_stop_training_program(msg, authorized_update, context):
    await bot.stop_training_program(authorized_update, context)
    msg.reply_text.assert_called_once_with("Training program deactivated")
