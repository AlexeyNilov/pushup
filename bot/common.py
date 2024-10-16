"""
This module contains utility functions for the bot.
"""

from telegram import Chat, Update
from telegram.ext import ContextTypes, ConversationHandler
from service import repo
from functools import wraps
import logging
from typing import Callable, Any
import traceback
from conf.settings import DEVELOPER_CHAT_ID
import json
import html
from telegram.constants import ParseMode


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    chat_id = context.job.chat_id
    if isinstance(chat_id, int):
        await context.bot.send_message(
            chat_id=chat_id, text=f"Beep! {context.job.data} seconds are over!"
        )
    else:
        logging.error(f"Invalid chat_id: {chat_id}")


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
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    logging.error(f"Error: {context.error}")
    logging.error(f"{tb_string}")
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


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
