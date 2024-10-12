from conf.settings import BOT_TOKEN, AUTHORIZED_IDS
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in AUTHORIZED_IDS:
        await update.message.reply_text("Hello! You are authorized.")
    else:
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
