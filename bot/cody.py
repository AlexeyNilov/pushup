from conf.settings import BOT_TOKEN, AUTHORIZED_IDS
from functools import wraps
import random
from telegram import Chat, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from service import repo
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

        chat = update.effective_chat
        if chat.type != Chat.PRIVATE:
            await update.message.reply_text("Please use private chat.")
            return

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
    sum_for_today = repo.get_sum_for_today(user_id=update.effective_user.id)
    max_for_today = repo.get_max_for_today(user_id=update.effective_user.id)
    await update.message.reply_text(f"Today sum: {sum_for_today}, max: {max_for_today}")


@authorized_only
async def stats_all_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    max_all_time = repo.get_max_all_time(user_id=update.effective_user.id)
    max_sum = repo.get_max_sum(user_id=update.effective_user.id)
    await update.message.reply_text(
        f"Record set: {max_all_time}, sum per day: {max_sum}"
    )


async def generate_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.randint(1, 5) == 1:
        await update.message.reply_text(get_idea())


async def praise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    max_all_time = repo.get_max_all_time(user_id=update.effective_user.id)
    if repo.convert_to_int(update.message.text) > max_all_time:
        await update.message.reply_text("Good job!")
    else:
        await generate_idea(update=update, context=context)


@authorized_only
async def start_training_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo.activate_training(user_id=update.effective_user.id)
    await update.message.reply_text(
        "Training program activated, call /advice to get recommended workout"
    )


@authorized_only
async def parse_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text and not repo.is_number(update.message.text):
        await update.message.reply_text("Response is not implemented")
        return

    await praise(update=update, context=context)
    repo.save_pushup(
        value=repo.convert_to_int(update.message.text), user_id=update.effective_user.id
    )
    await update.message.reply_text(f"Logged {update.message.text} push-ups")
    repo.sync_profile(user_id=update.effective_user.id)


@authorized_only
async def get_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(f"<b>Warm up</b>:\n{get_warmup()}")
    await update.message.reply_html(
        f"<b>Workout</b>:\n{get_workout(user_id=update.effective_user.id)}"
    )
    await update.message.reply_html(f"<b>Cool down</b>:\n{get_cool_down()}")


@authorized_only
async def complete_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo.increment_training_day(user_id=update.effective_user.id)
    await update.message.reply_text("Workout completed!")


async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a list of available commands to the user."""
    commands = (
        "/activate - Activate training program\n"
        "/done - Complete workout\n"
        "/help - Show this help message\n"
        "/practice - Get workout recommendation\n"
        "/record - Show achievements\n"
        "/stats - Show today's statistics"
    )
    await update.message.reply_text(commands)


async def start_private_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_name = update.effective_user.full_name
    chat = update.effective_chat
    if chat.type != Chat.PRIVATE or chat.id in context.bot_data.get("user_ids", set()):
        return

    context.bot_data.setdefault("user_ids", set()).add(chat.id)

    await update.effective_message.reply_text(
        f"""Welcome {user_name}! 💪 Before you start using the workout recommendations, please note:
* This bot is designed to provide general fitness suggestions only.
* It is not a substitute for professional medical advice, diagnosis, or treatment.
* Always listen to your body and use common sense when performing exercises.
* If you have any medical conditions, injuries, or concerns, please consult with a healthcare provider.
* By using this bot, you agree that you do so at your own risk.
* The bot is not responsible for any injury or health issues that may arise.

Stay safe, know your limits, and enjoy your workout! 🏋️‍♂️

Press /join to start
        """
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("done", complete_workout))
    application.add_handler(CommandHandler("activate", start_training_program))
    application.add_handler(CommandHandler("stats", stats_for_today))
    application.add_handler(CommandHandler("record", stats_all_time))
    application.add_handler(CommandHandler("practice", get_practice))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("join", join_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, parse_message)
    )

    application.add_handler(MessageHandler(filters.ALL, start_private_chat))

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
