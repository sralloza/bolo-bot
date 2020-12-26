from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from app.api.bot.bolo import get_ranking, register_bolo
from app.api.bot.help import (
    register,
    register_using_username,
    send_welcome,
    show_version,
    unregister,
)
from app.core.config import settings
from app.core.utils import exception_handling

updater = Updater(token=settings.token_bot, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("help", send_welcome))  # type: ignore
dispatcher.add_handler(CommandHandler("start", send_welcome))  # type: ignore
dispatcher.add_handler(CommandHandler("version", show_version))  # type: ignore
dispatcher.add_handler(CommandHandler("unregister", unregister))

dispatcher.add_handler(CommandHandler("ranking", get_ranking))

dispatcher.add_handler(
    ConversationHandler(
        entry_points=[
            CommandHandler("register", register),
            CommandHandler("bolo", register_bolo),
        ],
        states={
            "USERNAME": [
                MessageHandler(Filters.text & ~Filters.command, register_using_username)
            ],
        },
        fallbacks=[],
    )
)
# dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

dispatcher.add_error_handler(exception_handling)
