"""
This module contains utility functions for the bot.
"""

from telegram import Chat, Update
from telegram.ext import ContextTypes, ConversationHandler
from service import repo
from functools import wraps
import logging
from typing import Callable, Any


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(
        job.chat_id, text=f"Beep! {job.data} seconds are over!"
    )


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the cancellation of the conversation."""
    await update.message.reply_text("Okay, conversation cancelled.")
    return ConversationHandler.END


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler to catch exceptions."""
    logging.error(f"Error: {context.error}")


def authorized_only(handler: Callable) -> Callable:
    """Decorator to restrict command handlers to authorized users only."""

    @wraps(handler)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        if update.effective_chat.type != Chat.PRIVATE:
            await update.message.reply_text("Please use private chat.")
            return

        if not repo.has_profile(update.effective_user.id):
            await update.message.reply_text(
                "Sorry, you are not authorized to use this bot, /join first"
            )
            return

        return await handler(update, context)

    return wrapper
