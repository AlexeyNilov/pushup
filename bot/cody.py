from conf.settings import BOT_TOKEN
from functools import wraps
import random
from telegram import Chat, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)
from service import repo
from service.idea import get_idea
from service.warmup import get_warmup
from service.cooldown import get_cool_down
from service.workout import get_workout
from data.logger import set_logging


set_logging()


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


@authorized_only
async def stop_training_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo.deactivate_training(user_id=update.effective_user.id)
    await update.message.reply_text("Training program deactivated")


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


@authorized_only
async def change_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please tell me your age.")
    return "ask_age"


@authorized_only
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        f"""
👋 Greetings, {update.effective_user.full_name}! Let's get you started with this bot. Here's how you can use it:

📌 **Main Feature: Push-ups Logging**
Simply enter the number of push-ups you've done (e.g., *20*), and I'll save it! 📝
You can check your stats later with:
- `/stats` - See today's stats 📊
- `/record` - View your all-time best 🏆

💡 **Need Inspiration?**
Use `/practice` to receive a **random warm-up, workout, and cooldown** recommendation 🏃‍♂️💪🧘.

🏅 **Prefer a Systematic Training Program?**
Here's how to activate and follow the program:
1️. **`/activate`** - Start the training program 🎯
2️. **`/practice`** - Get your current workout 🔄
3️. **Log your push-ups** by entering the number 💪
4️. **`/done`** - Mark the workout as complete ✅ (This will move you to the next workout in the sequence)

⚡ **Enjoy your fitness journey and have fun!** 🎉🏋️‍♀️
"""
    )


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a list of available commands to the user."""
    commands = (
        "/activate - Activate training program\n"
        "/age - Change your age\n"
        "/done - Complete workout\n"
        "/info - How to use the bot\n"
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


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the cancellation of the conversation."""
    await update.message.reply_text("Okay, conversation cancelled.")
    return ConversationHandler.END  # End the conversation


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler to catch exceptions."""
    pass


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    join_handler = ConversationHandler(
        entry_points=[CommandHandler("join", join_command)],
        states={
            "ask_age": [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],  # Handle cancellations
    )

    activate_handler = ConversationHandler(
        entry_points=[CommandHandler("activate", start_training_program)],
        states={
            "ask_max_set": [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_max_set)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],  # Handle cancellations
    )

    change_age_handler = ConversationHandler(
        entry_points=[CommandHandler("age", change_age)],
        states={
            "ask_age": [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],  # Handle cancellations
    )

    application.add_handler(join_handler)
    application.add_handler(activate_handler)
    application.add_handler(change_age_handler)
    application.add_handler(CommandHandler("done", complete_workout))
    application.add_handler(CommandHandler("stats", stats_for_today))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("record", stats_all_time))
    application.add_handler(CommandHandler("practice", get_practice))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, parse_message)
    )
    application.add_handler(MessageHandler(filters.ALL, start_private_chat))
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
