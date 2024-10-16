import pytest
from telegram import Chat
from bot.message import start_private_chat, parse_message
from bot.conversation import receive_max_set


@pytest.mark.asyncio
async def test_parse_message(msg, update, context):
    # Test for input "10"
    update.message.text = "10"
    await parse_message(update, context)
    update.message.set_reaction.assert_called_with("👍")
    msg.reply_text.assert_any_call("Good job!")


@pytest.mark.asyncio
async def test_parse_message_race(msg, update, context):
    update.message.text = "10"
    await receive_max_set(update, context)
    await parse_message(update, context)
    update.message.set_reaction.assert_called_with("👍")


@pytest.mark.asyncio
async def test_parse_message_fail(msg, update, context):
    update.message.text = "test"
    await parse_message(update, context)
    msg.reply_text.assert_not_called()


@pytest.mark.asyncio
async def test_start_private_chat_private(update, context):
    context.bot_data = {}

    # Act
    await start_private_chat(update, context)

    # Assert
    update.effective_message.reply_html.assert_called_once()
    assert 123456 in context.bot_data.get("user_ids", set())
    assert "Welcome TestUser!" in update.effective_message.reply_html.call_args[0][0]


@pytest.mark.asyncio
async def test_start_private_chat_non_private(update, context):
    update.effective_chat.type = Chat.GROUP
    context.bot_data = {}

    # Act
    await start_private_chat(update, context)

    # Assert
    update.effective_message.reply_html.assert_not_called()
    assert "user_ids" not in context.bot_data


@pytest.mark.asyncio
async def test_start_private_chat_existing_user(update, context):
    context.bot_data = {"user_ids": {123456}}

    # Act
    await start_private_chat(update, context)

    # Assert
    update.effective_message.reply_html.assert_not_called()
    assert 123456 in context.bot_data["user_ids"]


@pytest.mark.asyncio
async def test_start_private_chat_message_content(update, context):
    context.bot_data = {}

    # Act
    await start_private_chat(update, context)

    # Assert
    called_with = update.effective_message.reply_html.call_args[0][0]
    assert "Welcome TestUser!" in called_with
    assert "Important Information:" in called_with
    assert "This bot provides <b>general fitness suggestions only</b>" in called_with
    assert "Press /join to start" in called_with
