from pathlib import Path

from telegram import ParseMode
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from app import __version__
from app.core.bot import bot_command
from app.core.config import settings


@bot_command("start")
@bot_command("help")
def show_help(update: Update, context: CallbackContext):
    msg = Path(__file__).parent.parent.parent.with_name("commands.md").read_text("utf8")
    msg = msg.format(developer=settings.developer)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg, parse_mode=ParseMode.MARKDOWN
    )


@bot_command("version")
def show_version(update: Update, context: CallbackContext):
    msg = f"Versión actual: {__version__}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
