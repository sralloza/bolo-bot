from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from app import crud

from .emoji import pos_to_emoji


def reset_bolos(db: Session):
    return crud.user.reset_database(db)


def show_ranking(
    db: Session, update: Update, context: CallbackContext, limit: int = 10
):
    users = crud.user.get_ranking(db, limit=limit)
    if not users:
        msg = "No hay datos"
    else:
        msg = "🎣 Ranking actual:\n"
        msg += "\n".join(
            f"{pos_to_emoji(i)}: {u.username} ({u.bolos})"
            for i, u in enumerate(users, start=1)
        )

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def show_latest(db: Session, update: Update, context: CallbackContext, limit: int = 10):
    users = crud.user.get_latest(db, limit=limit)
    if not users:
        msg = "No hay datos"
    else:
        msg = "🎣 Últimos bolos:\n"
        msg += "\n".join(
            f"{pos_to_emoji(i, emoji_enabled=False)}: [{u.latest_bolo}] {u.username} ({u.bolos})"
            for i, u in enumerate(users, start=1)
        )

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
