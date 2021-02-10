from telegram.ext import CommandHandler, Updater

from app.api.bot.account import register, remove_inactive_users, unregister
from app.api.bot.bolo import get_ranking, register_bolo, reset_database
from app.api.bot.help import show_help, show_version
from app.core.config import settings
from app.utils import exception_handling


def create_updater():
    updater = Updater(token=settings.token_bot, use_context=True)
    dispatcher = updater.dispatcher

    # Help callbacks
    dispatcher.add_handler(CommandHandler("help", show_help))  # type: ignore
    dispatcher.add_handler(CommandHandler("start", show_help))  # type: ignore
    dispatcher.add_handler(CommandHandler("version", show_version))  # type: ignore

    # Account callbacks
    dispatcher.add_handler(CommandHandler("unregister", unregister))

    # Bolo callbacks
    dispatcher.add_handler(CommandHandler("ranking", get_ranking))

    # Admin callbacks
    dispatcher.add_handler(CommandHandler("reset", reset_database))
    dispatcher.add_handler(CommandHandler("remove_inactive", remove_inactive_users))

    # Account callbacks
    dispatcher.add_handler(CommandHandler("register", register))

    # Bolo callbacks
    dispatcher.add_handler(CommandHandler("bolo", register_bolo))

    # Error handler callback
    dispatcher.add_error_handler(exception_handling)
    return updater
