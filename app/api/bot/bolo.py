from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from app import crud
from app.api.bot.help import register
from app.core.emoji import pos_to_emoji
from app.core.utils import inject_db


@inject_db
def register_bolo(
    db: Session, update: Update, context: CallbackContext, bolos: int = 1
):
    if not crud.user.get(db, id=update.effective_user.id):
        result = register(update, context)

        if isinstance(result, str):
            bolos_pending = context.user_data.get("bolo-pending", 0)
            context.user_data["bolo-pending"] = bolos_pending + 1
            return result

        assert register.db
        db = register.db

    user = crud.user.register_bolos(db, id=update.effective_user.id, bolos=bolos)
    pos = crud.user.get_user_position(db, id=user.id)
    msg = (
        f"Bolo{'s' if bolos > 1 else ''} registrado{'s' if bolos > 1 else ''}.\n"
        f"Tienes actualmente {user.bolos} "
        f"bolo{'s' if user.bolos > 1 else ''}.\nEstás en la posición {pos}."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@inject_db
def get_ranking(db: Session, update: Update, context: CallbackContext):
    users = crud.user.get_ranking(db)
    msg = "🎣 Ranking actual:\n"
    msg += "\n".join(
        f"{pos_to_emoji(i+1)}: {u.username} ({u.bolos})" for i, u in enumerate(users)
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
