from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from app import crud
from app.core.emoji import pos_to_emoji
from app.core.utils import inject_db


@inject_db
def register_bolo(db: Session, update: Update, context: CallbackContext):
    if not crud.user.get(db, id=update.effective_user.id):
        msg = "No estás registrado. Regístrate con el comando /register"
        return context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    user = crud.user.register_bolo(db, id=update.effective_user.id)
    pos = crud.user.get_user_position(db, id=user.id)
    msg = f"Bolo Registrado.\nTienes actualmente {user.bolos} bolos.\nEstás en la posición {pos}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@inject_db
def get_ranking(db: Session, update: Update, context: CallbackContext):
    users = crud.user.get_ranking(db)
    msg = "🎣 Ranking actual:\n"
    msg += "\n".join(
        f"{pos_to_emoji(i+1)}: {u.username} ({u.bolos})" for i, u in enumerate(users)
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
