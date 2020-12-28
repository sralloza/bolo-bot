import json

from telegram import Update

from .bot import create_updater


def webhook(data: dict):
    updater = create_updater()
    update = Update.de_json(data, updater.bot)
    assert update
    updater.dispatcher.process_update(update)
