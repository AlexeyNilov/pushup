"""Simple bot to greet users automatically in private chats."""

from conf.settings import BOT_TOKEN_TEST

from telegram import Chat, Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)


async def start_private_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Greets the user and records that they started a chat with the bot if it's a private chat.
    Since no `my_chat_member` update is issued when a user starts a private chat with the bot
    for the first time, we have to track it explicitly here.
    """
    user_name = update.effective_user.full_name
    chat = update.effective_chat
    if chat.type != Chat.PRIVATE or chat.id in context.bot_data.get("user_ids", set()):
        return

    print("%s started a private chat with the bot", user_name)
    context.bot_data.setdefault("user_ids", set()).add(chat.id)

    await update.effective_message.reply_text(
        f"""Welcome {user_name}! 💪 Before you start using the workout recommendations, please note:\n
* This bot is designed to provide general fitness suggestions only.\n
* It is not a substitute for professional medical advice, diagnosis, or treatment.\n
* Always listen to your body and use common sense when performing exercises.\n
* If you have any medical conditions, injuries, or concerns, please consult with a healthcare provider.\n
* By using this bot, you agree that you do so at your own risk.
* The bot is not responsible for any injury or health issues that may arise.

Stay safe, know your limits, and enjoy your workout! 🏋️‍♂️

Press /join to start
        """
    )


def main() -> None:
    application = Application.builder().token(BOT_TOKEN_TEST).build()
    application.add_handler(MessageHandler(filters.ALL, start_private_chat))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
