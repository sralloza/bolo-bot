from pathlib import Path

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from app import __version__
from app.core.bot import bot_command


@bot_command("start")
@bot_command("help")
def show_help(update: Update, context: CallbackContext):
    msg = Path(__file__).parent.parent.parent.with_name("readme.md").read_text("utf8")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg, parse_mode="markdown"
    )


@bot_command("version")
def show_version(update: Update, context: CallbackContext):
    msg = f"Versión actual: {__version__}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
