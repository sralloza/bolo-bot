from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from telegram.update import Update

from app import __version__, crud
from app.core.config import settings
from app.core.exceptions import AlreadyExistsError
from app.schemas.user import UserCreate
from app.utils import generate_username_from_tg_user, inject_db


def send_welcome(update: Update, context: CallbackContext):
    msg = "Bienvenido. Para registarte, ejecuta /register."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def show_version(update: Update, context: CallbackContext):
    msg = f"Versión actual: {__version__}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
