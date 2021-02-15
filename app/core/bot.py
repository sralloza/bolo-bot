from typing import Any, Optional

from telegram.ext import CommandHandler, Updater
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

from app.core.config import settings
from app.utils import exception_handling


class BotMemory:
    updater: Optional[Updater] = None


def bot_command(command: str = None, cls=CommandHandler, allow_updates=False, **kwargs):
    def decorator(func):
        arg: Any

        if not BotMemory.updater:
            create_bot()

        if issubclass(cls, MessageHandler) and isinstance(command, str):
            filters = kwargs.pop("filters", None)
            arg = Filters.regex(command)
            if filters:
                arg = arg & filters
            if not allow_updates:
                arg = arg & ~Filters.update.edited_message
        else:
            arg = command or func.__name__

        if not allow_updates and not issubclass(cls, MessageHandler):
            filters = kwargs.pop("filters", None)

            if filters:
                filters = filters & ~Filters.update.edited_message
            else:
                filters = ~Filters.update.edited_message
            kwargs["filters"] = filters

        BotMemory.updater.dispatcher.add_handler(cls(arg, func, **kwargs))
        return func

    return decorator


def create_bot():
    BotMemory.updater = Updater(token=settings.token_bot, use_context=True)
    BotMemory.updater.dispatcher.add_error_handler(exception_handling)


def create_updater():
    if BotMemory.updater is None:
        raise RuntimeError("No commands found")

    return BotMemory.updater
