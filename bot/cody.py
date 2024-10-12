from conf.settings import BOT_TOKEN, AUTHORIZED_IDS
from functools import wraps
import random
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from service.repo import (
    is_number,
    save_pushup,
    get_sum_for_today,
    get_max_for_today,
    get_max_all_time,
    get_average,
)
from service.idea import get_idea
from service.warmup import get_warmup
from service.cooldown import get_cool_down
from service.workout import get_workout


def authorized_only(handler):
    """Decorator to restrict command handlers to authorized users only."""

    @wraps(handler)  # Ensures the original handler's name and docstring are preserved
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        if update.effective_user is None:
            raise ValueError("No user found in the update.")
        if update.message is None:
            raise ValueError("No message found in the update")

        user_id = update.effective_user.id
        if user_id in AUTHORIZED_IDS:
            return await handler(update, context, *args, **kwargs)
        else:
            await update.message.reply_text(
                "Sorry, you are not authorized to use this bot."
            )

    return wrapper


@authorized_only
async def stats_for_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sum_for_today = get_sum_for_today(user_id=update.effective_user.id)
    max_for_today = get_max_for_today(user_id=update.effective_user.id)
    await update.message.reply_text(f"Today sum: {sum_for_today}, max: {max_for_today}")


@authorized_only
async def stats_all_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    max_all_time = get_max_all_time(user_id=update.effective_user.id)
    await update.message.reply_text(f"Record set: {max_all_time}")


async def generate_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.randint(1, 5) == 1:
        await update.message.reply_text(get_idea())


@authorized_only
async def parse_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text and is_number(update.message.text):
        max_all_time = get_max_all_time(user_id=update.effective_user.id)
        save_pushup(value=int(update.message.text), user_id=update.effective_user.id)
        await update.message.reply_text(f"Logged {update.message.text} push-ups")

        if int(update.message.text) > max_all_time:
            await update.message.reply_text("Good job!")
        else:
            await generate_idea(update=update, context=context)
    else:
        await update.message.reply_text("Response is not implemented")


@authorized_only
async def get_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(f"<b>Warm up</b>:\n{get_warmup()}")
    w = get_workout(
        avg_rep=get_average(user_id=update.effective_user.id),
        max_rep=get_max_all_time(user_id=update.effective_user.id),
    )
    await update.message.reply_html(f"<b>Workout</b>:\n{w}")
    await update.message.reply_html(f"<b>Cool down</b>:\n{get_cool_down()}")


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a list of available commands to the user."""
    commands = (
        "/stats - Show today's statistics\n"
        "/record - Show your records\n"
        "/advice - Get training advice\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(commands)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("stats", stats_for_today))
    application.add_handler(CommandHandler("record", stats_all_time))
    application.add_handler(CommandHandler("advice", get_advice))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, parse_message)
    )

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
