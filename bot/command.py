"""
This module contains command handlers for the bot.
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.common import authorized_only, remove_job_if_exists, alarm
from service import repo
from service.warmup import get_warmup
from service.cooldown import get_cool_down
from service.workout import get_workout
from service.training import increment_training_day, deactivate_training
from service.fitness_test import get_rating


@authorized_only
async def get_practice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    workout_plan = get_workout(user_id=user_id)

    if "rest</i>" in workout_plan.lower():
        await update.message.reply_html(f"<b>Today's Practice</b>:\n{workout_plan}")
    else:
        messages = [
            ("<b>Warm up</b>", get_warmup()),
            ("<b>Workout</b>", workout_plan),
            ("<b>Cool down</b>", get_cool_down()),
        ]
        for title, content in messages:
            await update.message.reply_html(f"{title}:\n{content}")


@authorized_only
async def stats_for_today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    sum_for_today = repo.get_sum_for_today(user_id=user_id)
    max_for_today = repo.get_max_for_today(user_id=user_id)
    await update.message.reply_text(f"Today sum: {sum_for_today}, max: {max_for_today}")


@authorized_only
async def stats_all_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    max_all_time = repo.get_max_all_time(user_id=user_id)
    max_sum = repo.get_max_sum(user_id=user_id)
    await update.message.reply_text(
        f"Record set: {max_all_time}, sum per day: {max_sum}"
    )


@authorized_only
async def stop_training_program(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    deactivate_training(user_id=update.effective_user.id)
    await update.message.reply_text("Training program deactivated")


@authorized_only
async def complete_workout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    increment_training_day(user_id=update.effective_user.id)
    await update.message.reply_text("Workout completed!")


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a list of available commands to the user with a keyboard menu."""
    commands = [
        ["/practice", "/done"],
        ["/stats", "/record"],
        ["/set", "/help"],
    ]

    keyboard = ReplyKeyboardMarkup(commands, resize_keyboard=True, is_persistent=True)

    message = (
        "Here are the available commands:\n\n"
        "/activate 🎯 - Activate training program\n"
        "/age 🎂 - Change your age\n"
        "/deactivate 🎯 - Deactivate training program\n"
        "/done ✅ - Complete workout\n"
        "/info 💡 - How to use the bot\n"
        "/help ❓ - Show this help message\n"
        "/practice 💪 - Get workout recommendation\n"
        "/rating 🏅 - Get your fitness rating\n"
        "/record 🏆 - Show achievements\n"
        "/set 🕒 - Set timer for 60 seconds\n"
        "/stats 📊 - Show today's statistics\n\n"
        "You can use the keyboard below for quick access to commands."
    )

    await update.message.reply_text(message, reply_markup=keyboard)


@authorized_only
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    info_text = f"""
👋 Greetings, {update.effective_user.full_name}! Let's get you started with this bot. Here's how you can use it:

📌 <b>Main Feature: Push-ups Logging</b>
Simply enter the number of push-ups you've done (e.g., 20), and I'll save it! 📝
You can check your stats later with:
- /stats - See today's stats 📊
- /record - View your all-time best 🏆

💡 <b>Need Inspiration?</b>
Use /practice to receive a random warm-up, workout, and cooldown recommendation 🏃‍♂️💪🧘.

🏅 <b>Prefer a Systematic Training Program?</b>
Here's how to activate and follow the program:
1. /activate - Start the training program 🎯
2. /practice - Get your current workout 🔄
3. Log your push-ups by entering the number 💪
4. /done - Mark the workout as complete ✅ (This will move you to the next workout in the sequence)

⚡ Enjoy your fitness journey and have fun! 🎉🏋️‍♀️
"""
    await update.effective_message.reply_html(info_text)


@authorized_only
async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    due = 60.0

    remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

    await update.effective_message.reply_text("Timer successfully set!")


@authorized_only
async def rating_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    army_rating, civil_rating = get_rating(update.effective_user.id)
    await update.message.reply_html(
        f""""💪 Based on your <b>max set</b> and <b>age</b>,
the <b>US Army</b> says: <i>{army_rating}</i> 🪖.
📊 Compared to the <b>general population</b>, your fitness level is: <i>{civil_rating}</i> 🏃‍♂️."""
    )
