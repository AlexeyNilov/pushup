import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Chat, User, Message
from telegram.ext import ContextTypes
from bot.message import start_private_chat


@pytest.fixture
def update():
    upd = MagicMock(spec=Update)
    upd.effective_user = MagicMock(spec=User)
    upd.effective_user.full_name = "Test User"
    upd.effective_chat = MagicMock(spec=Chat)

    return upd


@pytest.fixture
def context():
    return MagicMock(spec=ContextTypes.DEFAULT_TYPE)


@pytest.mark.asyncio
async def test_start_private_chat_private(update, context):
    update.effective_chat.type = Chat.PRIVATE
    update.effective_chat.id = 123456
    update.effective_message = AsyncMock(spec=Message)
    context.bot_data = {}

    # Act
    await start_private_chat(update, context)

    # Assert
    update.effective_message.reply_html.assert_called_once()
    assert 123456 in context.bot_data.get("user_ids", set())
    assert "Welcome Test User!" in update.effective_message.reply_html.call_args[0][0]


@pytest.mark.asyncio
async def test_start_private_chat_non_private(update, context):
    update.effective_chat.type = Chat.GROUP
    update.effective_message = AsyncMock(spec=Message)
    context.bot_data = {}

    # Act
    await start_private_chat(update, context)

    # Assert
    update.effective_message.reply_html.assert_not_called()
    assert "user_ids" not in context.bot_data


@pytest.mark.asyncio
async def test_start_private_chat_existing_user(update, context):
    update.effective_chat.type = Chat.PRIVATE
    update.effective_chat.id = 123456
    update.effective_message = AsyncMock(spec=Message)
    context.bot_data = {"user_ids": {123456}}

    # Act
    await start_private_chat(update, context)

    # Assert
    update.effective_message.reply_html.assert_not_called()
    assert 123456 in context.bot_data["user_ids"]


@pytest.mark.asyncio
async def test_start_private_chat_message_content(update, context):
    update.effective_chat.type = Chat.PRIVATE
    update.effective_chat.id = 123456
    update.effective_message = AsyncMock(spec=Message)
    context.bot_data = {}

    # Act
    await start_private_chat(update, context)

    # Assert
    called_with = update.effective_message.reply_html.call_args[0][0]
    assert "Welcome Test User!" in called_with
    assert "Important Information:" in called_with
    assert "This bot provides <b>general fitness suggestions only</b>" in called_with
    assert "Press /join to start" in called_with
