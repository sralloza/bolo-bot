from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update

from app.core.bot import bot_command


@bot_command(Filters.command, cls=MessageHandler)
def invalid_command(update: Update, context: CallbackContext):
    command_name = update.message.text
    if command_name.startswith("/"):
        command_name = command_name[1:]
    msg = "Comando inválido: %r" % command_name
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
