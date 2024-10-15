"""
This module contains utility functions for the bot.
"""

from telegram import Chat, Update
from telegram.ext import ContextTypes, ConversationHandler
from service import repo
from functools import wraps


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the cancellation of the conversation."""
    await update.message.reply_text("Okay, conversation cancelled.")
    return ConversationHandler.END  # End the conversation


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler to catch exceptions."""
    pass


def authorized_only(handler):
    """Decorator to restrict command handlers to authorized users only."""

    @wraps(handler)  # Ensures the original handler's name and docstring are preserved
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):

        chat = update.effective_chat
        if chat.type != Chat.PRIVATE:
            await update.message.reply_text("Please use private chat.")
            return

        if repo.has_profile(update.effective_user.id):
            return await handler(update, context, *args, **kwargs)
        else:
            await update.message.reply_text(
                "Sorry, you are not authorized to use this bot, /join first"
            )

    return wrapper
