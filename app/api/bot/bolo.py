from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from app import crud
from app.core.account import register_user
from app.core.bolo import reset_bolos
from app.core.bot import bot_command
from app.core.emoji import pos_to_emoji
from app.utils import inject_db, require_admin


@bot_command("bolo")
@inject_db
def register_bolo(
    db: Session, update: Update, context: CallbackContext, bolos: int = 1
):
    if not crud.user.get(db, id=update.effective_user.id):
        register_user(db, update, context)

    user = crud.user.register_bolos(db, id=update.effective_user.id, bolos=bolos)
    pos = crud.user.get_user_position(db, id=user.id)
    msg = (
        f"Bolo{'s' if bolos > 1 else ''} registrado{'s' if bolos > 1 else ''}.\n"
        f"Tienes actualmente {user.bolos} "
        f"bolo{'s' if user.bolos > 1 else ''}.\nEstás en la posición {pos}."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@bot_command("ranking")
@inject_db
def get_ranking(db: Session, update: Update, context: CallbackContext):
    users = crud.user.get_ranking(db)
    if not users:
        msg = "No hay datos"
    else:
        msg = "🎣 Ranking actual:\n"
        msg += "\n".join(
            f"{pos_to_emoji(i+1)}: {u.username} ({u.bolos})"
            for i, u in enumerate(users)
        )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@bot_command("reset")
@require_admin
@inject_db
def reset_database(db: Session, update: Update, context: CallbackContext):
    reset_bolos(db)
    msg = "Base de datos reiniciada correctamente"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
