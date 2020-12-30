from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext, Update
from telegram.ext.conversationhandler import ConversationHandler

from app import crud
from app.core.config import settings
from app.core.exceptions import AlreadyExistsError
from app.schemas.user import UserCreate
from app.utils import generate_username_from_tg_user, inject_db, require_admin


@inject_db
def register(db: Session, update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    existing_user = crud.user.get(db, id=user_id)
    if existing_user:
        msg = f"Ya estás registrado como {existing_user.username!r}.\n"
        msg += "Actualmente no está implementado el cambio del nombre de usuario."
        msg += "Si quieres cambiar tu nombre de usuario, espera a que se implemente "
        msg += f"o contacta con el desarrollador ({settings.developer})"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        return ConversationHandler.END

    username = update.effective_user.username
    if username is None:
        if not settings.autogenerate_username:
            msg = "No tienes un nombre de usuario. ¿Cómo te registro?"
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
            return "USERNAME"

        assert update.effective_user
        username = generate_username_from_tg_user(db, update.effective_user)

    user = UserCreate(id=user_id, username=username)
    crud.user.create(db, obj_in=user)
    msg = f"Registrado correctamente como {username!r}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    return ConversationHandler.END


@inject_db
def register_using_username(db: Session, update: Update, context: CallbackContext):
    username = update.message.text
    user_id = update.effective_user.id

    user = UserCreate(id=user_id, username=username)
    try:
        crud.user.create(db, obj_in=user)
    except AlreadyExistsError as exc:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(exc))
        return "USERNAME"

    msg = f"Registrado correctamente como {username!r}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    if context.user_data.get("bolo-pending", 0):
        from app.api.bot.bolo import register_bolo

        bolos_pending = context.user_data.get("bolo-pending", 0)
        register_bolo(update, context, bolos=bolos_pending)
        del context.user_data["bolo-pending"]

    return ConversationHandler.END


def expecting_username_not_command(update: Update, context: CallbackContext):
    if update.message.text == "/bolo":
        current = context.user_data.get("bolo-pending", 0)
        context.user_data["bolo-pending"] = current + 1

    msg = "¿Cómo quieres que te registre?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@inject_db
def unregister(db: Session, update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = crud.user.get(db, id=user_id)
    if user is None:
        msg = "No puedes darte de baja porque no estás registrado."
        return context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    crud.user.remove(db, id=user_id)
    msg = f"Registros eliminados para el usuario {user.username!r}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@require_admin
@inject_db
def remove_inactive_users(db: Session, update: Update, context: CallbackContext):
    crud.user.remove_inactive_users(db)
    msg = "Usuarios inactivos eliminados"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)