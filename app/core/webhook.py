import json

from telegram import Update

from .bot import dispatcher


def webhook(data: dict):
    update = Update.de_json(data, dispatcher.bot)
    assert update
    dispatcher.process_update(update)
