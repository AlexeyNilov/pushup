from conf.settings import BOT_TOKEN
from telegram import Update
from telegram.ext import Application, CommandHandler


# Define the start command handler
async def start(update: Update):
    await update.message.reply_text("Hello!")


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
