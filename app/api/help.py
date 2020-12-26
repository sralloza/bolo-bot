from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from telegram.update import Update

from app import __version__, crud
from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.core.utils import inject_db
from app.schemas.user import UserCreate


def send_welcome(update: Update, context: CallbackContext):
    msg = "Bienvenido. Para registarte, ejecuta /register."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def show_version(update: Update, context: CallbackContext):
    msg = f"Versión actual: {__version__}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@inject_db
def register(db: Session, update: Update, context: CallbackContext):
    username = update.effective_user.username
    user_id = update.effective_user.id

    if crud.user.get(db, id=user_id):
        msg = f"Ya estás registrado como {username!r}.\n"
        msg += "Actualmente no está implementado el cambio del nombre de usuario."
        msg += "Si quieres cambiar tu nombre de usuario, espera a que se implemente "
        msg += f"o contacta con el administrador ({settings.admin})"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        return ConversationHandler.END

    if username is None:
        msg = "No tienes un nombre de usuario. ¿Cómo te registro?"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        return "USERNAME"

    user = UserCreate(id=user_id, username=username)
    crud.user.create(db, obj_in=user)
    msg = f"Registrado correctamente como {username!r}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    return ConversationHandler.END


@inject_db
def register_using_username(db: Session, update: Update, context: CallbackContext):
    username = update.message.text
    user_id = update.effective_user.id

    if crud.user.get_by_username(db, username=username):
        msg = f"{username!r} ya está registrado, elige otro nombre."
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        return "USERNAME"

    user = UserCreate(id=user_id, username=username)
    crud.user.create(db, obj_in=user)
    msg = f"Registrado correctamente como {username!r}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    return ConversationHandler.END


@inject_db
def unregister(db: Session, update: Update, context: CallbackContext):
    username = update.effective_user.username
    user_id = update.effective_user.id
    try:
        crud.user.remove(db, id=user_id)
    except NotFoundError:
        msg = "No puedes darte de baja porque no estás registrado."
        return context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    msg = f"Registros eliminados para el usuario {username!r}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
