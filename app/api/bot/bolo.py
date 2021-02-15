from sqlalchemy.orm.session import Session
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update

from app import crud
from app.core.account import register_user
from app.core.bolo import reset_bolos, show_latest, show_ranking
from app.core.bot import bot_command
from app.utils import inject_db, require_admin


@bot_command("bolo")
@inject_db
def register_bolo(db: Session, update: Update, context: CallbackContext):
    if not crud.user.get(db, id=update.effective_user.id):
        register_user(db, update, context)

    user = crud.user.register_bolo(db, id=update.effective_user.id)
    pos = crud.user.get_user_position(db, id=user.id)
    msg = (
        f"Bolo registrado.\nTienes actualmente {user.bolos} "
        f"bolo{'s' if user.bolos > 1 else ''}.\nEstás en la posición {pos}."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@bot_command(r"/top([\s_]?\d+)?", cls=MessageHandler)
@inject_db
def ranking(db: Session, update: Update, context: CallbackContext):
    text = update.message.text.replace("top", "").strip("/_ ")
    text = text.replace(f"@{context.bot.username}", "")
    limit = 10

    if text:
        try:
            limit = int(text)
        except ValueError:
            return context.bot.send_message(
                chat_id=update.effective_chat.id, text="Número inválido: %r" % text
            )

    if limit > 50:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No se pueden mostrar tantos usuarios",
        )

    if limit <= 0:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No se pueden mostrar %s usuarios" % limit,
        )

    return show_ranking(db, update, context, limit)


@bot_command("reset")
@require_admin
@inject_db
def reset_database(db: Session, update: Update, context: CallbackContext):
    n = reset_bolos(db)
    msg = f"Eliminados {n} usuarios.\nBase de datos reiniciada correctamente"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


@bot_command(r"/ultimos([\s_]?\d+)?", cls=MessageHandler)
@inject_db
def latest(db: Session, update: Update, context: CallbackContext):
    print(context.args)
    text = update.message.text.replace("ultimos", "").strip("/_ ")
    limit = 10

    if text:
        try:
            limit = int(text)
        except ValueError:
            return context.bot.send_message(
                chat_id=update.effective_chat.id, text="Número inválido: %r" % text
            )

    if limit > 50:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No se pueden mostrar tantos usuarios",
        )

    if limit <= 0:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No se pueden mostrar %s usuarios" % limit,
        )

    return show_latest(db, update, context, limit)
