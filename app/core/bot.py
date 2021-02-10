from typing import Optional

from telegram.ext import CommandHandler, Updater
from telegram.ext.filters import Filters

from app.core.config import settings
from app.utils import exception_handling


class BotMemory:
    updater: Optional[Updater] = None


def bot_command(command_name: str = None, cls=CommandHandler, regex=False):
    def decorator(func):
        arg = command_name or func.__name__

        if not BotMemory.updater:
            create_bot()

        if regex:
            arg = Filters.regex(arg)

        BotMemory.updater.dispatcher.add_handler(cls(arg, func))
        return func

    return decorator


def create_bot():
    BotMemory.updater = Updater(token=settings.token_bot, use_context=True)
    BotMemory.updater.dispatcher.add_error_handler(exception_handling)


def create_updater():
    if BotMemory.updater is None:
        raise RuntimeError("No commands found")

    return BotMemory.updater
