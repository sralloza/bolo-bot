from typing import Optional

from telegram.ext import CommandHandler, Updater

from app.core.config import settings
from app.utils import exception_handling


class BotMemory:
    updater: Optional[Updater] = None


def bot_command(command_name: str = None):
    def decorator(func):
        nonlocal command_name
        if not command_name:
            command_name = func.__name__

        if not BotMemory.updater:
            create_bot()

        BotMemory.updater.dispatcher.add_handler(CommandHandler(command_name, func))
        return func

    return decorator


def create_bot():
    BotMemory.updater = Updater(token=settings.token_bot, use_context=True)
    BotMemory.updater.dispatcher.add_error_handler(exception_handling)


def create_updater():
    if BotMemory.updater is None:
        raise RuntimeError("No commands found")

    return BotMemory.updater
