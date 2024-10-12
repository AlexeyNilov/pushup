from conf.settings import BOT_TOKEN, AUTHORIZED_IDS
from telegram import Update
from telegram.ext import Application, CommandHandler


async def start(update: Update, context):
    # Check if the user ID matches your authorized ID
    if update.effective_user.id in AUTHORIZED_IDS:
        await update.message.reply_text("Hello! You are authorized.")
    else:
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )


# Main function to set up the bot
def main():

    # Set up the application (replaces Updater)
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
