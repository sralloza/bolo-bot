from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext, Update

from app import crud
from app.core.bot import bot_command
from app.utils import inject_db, require_admin


@bot_command()
def register(update: Update, context: CallbackContext):
    msg = "_Comando eliminado_\nEn futuras versiones ni siquiera aparecerá "
    msg += "este mensaje.\nAl no ser necesario ejecutar /register antes de /bolo, el "
    msg += "comando /register ha sido eliminado."
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg, parse_mode="markdown"
    )


@bot_command()
@inject_db
def unregister(db: Session, update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = crud.user.get(db, id=user_id)
    if user is None:
        msg = "No puedes eliminar tus datos porque no tienes ningún bolo asociado."
        return context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    crud.user.remove(db, id=user_id)
    msg = f"Registros eliminados para el usuario {user.username!r}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@bot_command("remove_inactive")
@require_admin
@inject_db
def remove_inactive_users(db: Session, update: Update, context: CallbackContext):
    crud.user.remove_inactive_users(db)
    msg = "Usuarios inactivos eliminados"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
