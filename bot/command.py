"""
This module contains command handlers for the bot.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils import authorized_only
from service import repo
from service.warmup import get_warmup
from service.cooldown import get_cool_down
from service.workout import get_workout


@authorized_only
async def get_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    workout = get_workout(user_id=user_id)

    if "rest" in workout.lower():
        await update.message.reply_html(f"<b>Today's Practice</b>:\n{workout}")
    else:
        await update.message.reply_html(f"<b>Warm up</b>:\n{get_warmup()}")
        await update.message.reply_html(f"<b>Workout</b>:\n{workout}")
        await update.message.reply_html(f"<b>Cool down</b>:\n{get_cool_down()}")


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


@authorized_only
async def stop_training_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo.deactivate_training(user_id=update.effective_user.id)
    await update.message.reply_text("Training program deactivated")


@authorized_only
async def complete_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo.increment_training_day(user_id=update.effective_user.id)
    await update.message.reply_text("Workout completed!")


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a list of available commands to the user."""
    commands = (
        "/activate 🎯 - Activate training program\n"
        "/age 🎂 - Change your age\n"
        "/deactivate 🎯 - Deactivate training program\n"
        "/done ✅ - Complete workout\n"
        "/info 💡 - How to use the bot\n"
        "/help ❓ - Show this help message\n"
        "/practice 💪 - Get workout recommendation\n"
        "/record 🏆 - Show achievements\n"
        "/stats 📊 - Show today's statistics"
    )
    await update.message.reply_text(commands)


@authorized_only
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_html(
        f"""
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
    )