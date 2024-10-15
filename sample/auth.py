""" User filtering example """

from conf.settings import BOT_TOKEN_TEST, AUTHORIZED_IDS
from functools import wraps
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


def authorized_only(handler):
    """Decorator to restrict command handlers to authorized users only."""

    @wraps(handler)  # Ensures the original handler's name and docstring are preserved
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        if update.effective_user is None:
            raise ValueError("No user found in the update.")
        user_id = update.effective_user.id
        if user_id in AUTHORIZED_IDS:
            return await handler(update, context, *args, **kwargs)
        else:
            if update.message:
                await update.message.reply_text(
                    "Sorry, you are not authorized to use this bot."
                )

    return wrapper


@authorized_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Hello! You are authorized.")


@authorized_only
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(f"Logged {update.message.text} push-ups")


def main():
    application = Application.builder().token(BOT_TOKEN_TEST).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
