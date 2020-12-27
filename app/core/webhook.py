import json

from telegram import Update

from .bot import dispatcher


def webhook(text: str):
    update = Update.de_json(json.loads(text), dispatcher.bot)
    assert update
    dispatcher.process_update(update)
