from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from app import __version__


def send_welcome(update: Update, context: CallbackContext):
    msg = "Bienvenido. Para registarte, ejecuta /register."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def show_version(update: Update, context: CallbackContext):
    msg = f"Versión actual: {__version__}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
