"""Simple bot to greet users automatically in private chats."""

from conf.settings import BOT_TOKEN_TEST

from telegram import Chat, Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)


async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Please tell me your age.")
    # Set the state to wait for the user's age response
    context.user_data["AGE_COLLECTION"] = True


async def receive_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler to receive the user's age and respond back."""
    # Check if we are expecting an age response
    if context.user_data.get("AGE_COLLECTION"):
        age = int(update.message.text)  # Get the user's response
        await update.message.reply_text(f"Thank you! Your age is {age}.")

        # Clear the age collection state
        context.user_data["AGE_COLLECTION"] = False
        await update.message.reply_text("Press /help to see what I can do for you")


async def start_private_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Greets the user and records that they started a chat with the bot if it's a private chat.
    Since no `my_chat_member` update is issued when a user starts a private chat with the bot
    for the first time, we have to track it explicitly here.
    """
    print("start_private_chat")
    user_name = update.effective_user.full_name
    chat = update.effective_chat
    if chat.type != Chat.PRIVATE or chat.id in context.bot_data.get("user_ids", set()):
        return

    print("%s started a private chat with the bot", user_name)
    context.bot_data.setdefault("user_ids", set()).add(chat.id)

    await update.effective_message.reply_text(
        f"Welcome {user_name}! Press /join to start"
    )


def main() -> None:
    application = Application.builder().token(BOT_TOKEN_TEST).build()
    application.add_handler(CommandHandler("join", join_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_age)
    )

    application.add_handler(MessageHandler(filters.ALL, start_private_chat))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
