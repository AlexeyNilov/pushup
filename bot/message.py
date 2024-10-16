"""
This module contains message handlers for the bot.
"""

import random
from telegram import Update, Chat
from telegram.ext import ContextTypes
from bot.common import authorized_only
from service import repo
from service.idea import get_idea
from service.util import is_number, convert_to_int


async def generate_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.randint(1, 5) == 1:
        await update.message.reply_text(get_idea())


async def praise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    max_all_time = repo.get_max_all_time(user_id=update.effective_user.id)
    if convert_to_int(update.message.text) > max_all_time:
        await update.message.reply_text("Good job!")
    else:
        await generate_idea(update=update, context=context)


@authorized_only
async def parse_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text and not is_number(update.message.text):
        return

    await praise(update=update, context=context)
    repo.save_pushup(
        value=convert_to_int(update.message.text), user_id=update.effective_user.id
    )
    await update.message.reply_text(f"Logged {update.message.text} push-ups")
    repo.sync_profile(user_id=update.effective_user.id)


async def start_private_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_name = update.effective_user.full_name
    chat = update.effective_chat
    if chat.type != Chat.PRIVATE or chat.id in context.bot_data.get("user_ids", set()):
        return

    context.bot_data.setdefault("user_ids", set()).add(chat.id)

    await update.effective_message.reply_html(
        f"""👋 Welcome {user_name}! 💪 Before you start using the workout recommendations, please note:

⚠️ <b>Important Information:</b>
- 🏋️ This bot provides <b>general fitness suggestions only</b>.
- 🚑 <b>It is not a substitute for professional medical advice, diagnosis, or treatment.</b>
- 🧠 Always <b>listen to your body</b> and use <b>common sense</b> when exercising.
- ⚕️ If you have any <b>medical conditions, injuries, or concerns</b>, consult with a healthcare provider.
- ⚠️ <b>By using this bot, you agree that you do so at your own risk.</b>
- ❌ The bot <b>is not responsible</b> for any injury or health issues that may arise.

✅ <b>Stay safe, know your limits, and enjoy your workout!</b> 🏋️‍♂️

👉 Press /join to start
"""
    )
