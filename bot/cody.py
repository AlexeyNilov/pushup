"""
This module contains the main bot logic.
"""

from conf.settings import BOT_TOKEN
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from data.logger import set_logging
from bot.common import error_handler
from bot.command import (
    info_command,
    help_command,
    complete_workout,
    stats_for_today,
    stats_all_time,
    stop_training_program,
    get_practice,
    set_timer,
    rating_command,
)
from bot.conversation import join_handler, change_age_handler, activate_handler
from bot.message import parse_message, start_private_chat


set_logging()


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(join_handler)
    application.add_handler(activate_handler)
    application.add_handler(change_age_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("done", complete_workout))
    application.add_handler(CommandHandler("stats", stats_for_today))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("rating", rating_command))
    application.add_handler(CommandHandler("record", stats_all_time))
    application.add_handler(CommandHandler("practice", get_practice))
    application.add_handler(CommandHandler("deactivate", stop_training_program))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, parse_message)
    )
    application.add_handler(MessageHandler(filters.ALL, start_private_chat))
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
