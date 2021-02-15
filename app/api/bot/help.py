from pathlib import Path

from sqlalchemy.orm import Session
from telegram import ParseMode
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update

from app import __version__, crud
from app.core.bot import bot_command
from app.core.config import settings
from app.utils import inject_db


@bot_command("ayuda")
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


@bot_command(Filters.status_update.new_chat_members, cls=MessageHandler)
def welcome(update: Update, context: CallbackContext):
    msg = (
        "Bienvenido, preséntate y lee las normas. En este grupo se"
        " trata la pesca del _carpfishing_ y las locuras varias de sus"
        " participantes, ponte cómod@ y disfruta del show."
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg, parse_mode="markdown"
    )


@bot_command(Filters.status_update.left_chat_member, cls=MessageHandler)
@inject_db
def say_goodbye(db: Session, update: Update, context: CallbackContext):
    msg = "Fue un placer tu estancia, pero por abandonar esta secta te caerá la maldición del bolo"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    user_id = update.message.left_chat_member.id
    user = crud.user.get(db, id=user_id)
    if user is None:
        return

    crud.user.remove(db, id=user_id)
    msg = (
        f"Eliminados los bolos de {user.username}, ahora hay "
        "más espacio para los bolos del resto"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
