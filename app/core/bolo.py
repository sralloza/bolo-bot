from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from app import crud

from .emoji import pos_to_emoji


def reset_bolos(db: Session):
    users = crud.user.get_multi(db, limit=100000)
    for user in users:
        crud.user.remove(db, id=user.id)


def show_ranking(
    db: Session, update: Update, context: CallbackContext, limit: int = 10
):
    users = crud.user.get_ranking(db, limit=limit)
    if not users:
        msg = "No hay datos"
    else:
        msg = "🎣 Ranking actual:\n"
        msg += "\n".join(
            f"{pos_to_emoji(i+1)}: {u.username} ({u.bolos})"
            for i, u in enumerate(users)
        )

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
