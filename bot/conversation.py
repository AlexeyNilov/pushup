"""
This module contains conversation handlers for the bot.
"""

from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from service import repo
from bot.utils import authorized_only, cancel


async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo.sync_profile(user_id=update.effective_user.id)
    await update.message.reply_text("Hello! Please tell me your age.")
    return "ask_age"


@authorized_only
async def receive_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler to receive the user's age and respond back."""
    age = repo.convert_to_int(update.message.text)  # Get the user's response
    await update.message.reply_text(f"Thank you! Your age is {age}.")
    profile = repo.get_profile(user_id=update.effective_user.id)
    profile.age = age
    repo.update_profile(dict(profile))
    await update.message.reply_text("Press /info to see what I can do for you")
    return ConversationHandler.END


join_handler = ConversationHandler(
    entry_points=[CommandHandler("join", join_command)],
    states={
        "ask_age": [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_age)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],  # Handle cancellations
)


@authorized_only
async def change_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please tell me your age.")
    return "ask_age"


change_age_handler = ConversationHandler(
    entry_points=[CommandHandler("age", change_age)],
    states={
        "ask_age": [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_age)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],  # Handle cancellations
)


@authorized_only
async def start_training_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please tell me how much push-ups you can do in one go?"
    )
    return "ask_max_set"


@authorized_only
async def receive_max_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    max_set = repo.convert_to_int(update.message.text)
    repo.activate_training(user_id=update.effective_user.id, max_set=max_set)
    await update.message.reply_text(
        "Training program activated, call /practice to get recommended workout"
    )
    return ConversationHandler.END


activate_handler = ConversationHandler(
    entry_points=[CommandHandler("activate", start_training_program)],
    states={
        "ask_max_set": [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_max_set)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],  # Handle cancellations
)
