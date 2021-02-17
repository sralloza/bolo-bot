from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext, Update

from app import crud
from app.core.bot import bot_command
from app.utils import get_remaining_text_after_command, inject_db, require_admin


@bot_command()
@require_admin
@inject_db
def unregister(db: Session, update: Update, context: CallbackContext):
    text = get_remaining_text_after_command(update, context, "unregister")
    if not text:
        msg = f"Tienes que especificar el id del usuario o su nombre de usuario"
        return context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    try:
        user_id = int(text)
        user = crud.user.get(db, id=user_id)

        if user is None:
            msg = f"No existe un usuario con id={user_id} en la base de datos"
            return context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    except ValueError:
        username = text.strip("@")
        user = crud.user.get_by_username(db, username=username)

        if user is None:
            msg = f"No existe el usuario con username={username!r} en la base de datos"
            return context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    crud.user.remove(db, id=user.id)
    msg = f"Registros eliminados para el usuario {user.username!r}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@bot_command("remove_inactive")
@require_admin
@inject_db
def remove_inactive_users(db: Session, update: Update, context: CallbackContext):
    crud.user.remove_inactive_users(db)
    msg = "Usuarios inactivos eliminados"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
