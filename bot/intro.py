"""Simple bot to greet users automatically in private chats."""

from conf.settings import BOT_TOKEN_TEST
from telegram import Update, ChatMember, Chat
from telegram.ext import (
    Application,
    ContextTypes,
    ChatMemberHandler,
)


async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user when they start a private chat with the bot."""
    chat_member = update.my_chat_member

    # Check if the chat is private and the user just started the conversation
    if (
        chat_member.chat.type == Chat.PRIVATE
        and chat_member.new_chat_member.status == ChatMember.MEMBER
    ):
        user = chat_member.from_user
        await context.bot.send_message(
            chat_id=chat_member.chat.id,
            text=f"Hello, {user.first_name}! 👋\nWelcome to the bot.",
        )


def main():
    """Main function to run the bot."""
    # Initialize the bot application
    application = Application.builder().token(BOT_TOKEN_TEST).build()

    # Add handlers for chat members and messages
    application.add_handler(
        ChatMemberHandler(greet_user, ChatMemberHandler.MY_CHAT_MEMBER)
    )

    # Start polling for updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
