from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from app.api.bot.account import (
    expecting_username_not_command,
    register,
    register_using_username,
    unregister,
)
from app.api.bot.bolo import get_ranking, register_bolo
from app.api.bot.help import send_welcome, show_version
from app.core.config import settings
from app.utils import exception_handling


def create_updater():
    updater = Updater(token=settings.token_bot, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", send_welcome))  # type: ignore
    dispatcher.add_handler(CommandHandler("start", send_welcome))  # type: ignore
    dispatcher.add_handler(CommandHandler("version", show_version))  # type: ignore
    dispatcher.add_handler(CommandHandler("unregister", unregister))

    dispatcher.add_handler(CommandHandler("ranking", get_ranking))

    if settings.autogenerate_username:
        dispatcher.add_handler(CommandHandler("register", register))
        dispatcher.add_handler(CommandHandler("bolo", register_bolo))
    else:
        dispatcher.add_handler(
            ConversationHandler(
                entry_points=[
                    CommandHandler("register", register),
                    CommandHandler("bolo", register_bolo),
                ],
                states={
                    "USERNAME": [
                        MessageHandler(
                            Filters.text & ~Filters.command, register_using_username
                        ),
                        MessageHandler(
                            Filters.text & Filters.command,
                            expecting_username_not_command,  # type:ignore
                        ),
                    ],
                },
                fallbacks=[],
            )
        )
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dispatcher.add_error_handler(exception_handling)
    return updater
