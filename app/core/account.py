from sqlalchemy.orm import Session
from telegram.ext.callbackcontext import CallbackContext, Update

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.utils import generate_username_from_tg_user


def register_user(db: Session, update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    existing_user = crud.user.get(db, id=user_id)
    if existing_user:
        return existing_user

    username = update.effective_user.username
    warn_custom_username = False
    if username is None:
        assert update.effective_user, "This is not supposed to happen"
        username = generate_username_from_tg_user(db, update.effective_user)
        warn_custom_username = True

    user = UserCreate(id=user_id, username=username)
    crud.user.create(db, obj_in=user)
    msg = f"Registrado correctamente como {username!r}"
    if warn_custom_username:
        msg += (
            "\nEl nombre de usuario ha sido generado automáticamente porque no"
            " tienes un nombre de usuario asociado a tu cuenta de telegram. Si quieres"
            f" cambiarlo contacta con el desarrollador del bot ({settings.developer})."
        )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
