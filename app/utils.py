import logging
import re
import traceback
from functools import wraps
from hashlib import sha256
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from uuid import uuid4

from fastapi import Request
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse
from telegram import Update, User
from telegram.ext.callbackcontext import CallbackContext

from app import crud
from app.db.session import get_db

from .core.config import settings

logger = getLogger(__name__)


def generate_username_from_tg_user(db: Session, tg_user: User):
    username = tg_user.first_name

    if tg_user.last_name:
        username += f" {tg_user.last_name}"

    if crud.user.get_by_username(db, username=username):
        str_user = repr(vars(tg_user)).encode("utf8")
        username += "-" + sha256(str_user).hexdigest()[:6]

    return username


def setup_logging():
    fmt = "[%(asctime)s] %(levelname)s - %(name)s:%(lineno)s - %(message)s"

    Path(settings.log_path).parent.mkdir(parents=True, exist_ok=True)

    file_handler = TimedRotatingFileHandler(
        settings.log_path,
        when="midnight",
        encoding="utf-8",
        backupCount=settings.max_logs,
    )

    if file_handler.shouldRollover(None):  # type: ignore noqa
        file_handler.doRollover()

    logging.basicConfig(
        handlers=[file_handler],
        level=settings.logging_level.as_python_logging(),
        format=fmt,
    )


def inject_db(function):
    @wraps(function)
    def wrap_function(*args, **kwargs):
        with get_db() as db:
            setattr(wrap_function, "db", db)
            return function(db, *args, **kwargs)

    setattr(wrap_function, "db", None)
    return wrap_function


def require_admin(function):
    @wraps(function)
    def wrap_function(*args, **kwargs):
        update: Update = kwargs.get("update")  # type:ignore
        context: CallbackContext = kwargs.get("context")  # type:ignore

        if update is None or context is None:
            update, context = args

        user_id = update.effective_user.id

        if user_id not in settings.admin_ids and user_id != settings.developer_id:
            msg = "No tienes permisos para ejecutar este comando"
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
            return
        return function(*args, **kwargs)

    return wrap_function


def get_remaining_text_after_command(
    update: Update, context: CallbackContext, command: str
) -> str:
    text = update.message.text.replace(command, "").strip("/_ ")
    text = re.sub(f"@{context.bot.username}", "", text, flags=re.I)
    return text


def exception_handling(update, context):
    exc = context.error
    tb = traceback.format_exc()
    chat_id = update.effective_chat.id
    msg = f"Error detectado en el chat {chat_id}: {exc!r}\n{tb}"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Error en el servidor. Notificado el desarrollador del bot ({settings.developer})",
    )
    context.bot.send_message(chat_id=settings.developer_id, text=msg)
    logger.exception(exc)


def server_exception_handling(request: Request, exc: Exception):
    """Logs an error and returns 500 to the user."""
    error_id = uuid4()
    scope = request.scope
    request_info = (
        f"[{request.client.host}] {scope['scheme'].upper()}/{scope['http_version']} "
        f"{scope['method']} {scope['path']}"
    )

    exc_info = (exc.__class__, exc, exc.__traceback__)
    logger.critical(
        "Unhandled exception [id=%s] in request '%s':",
        error_id,
        request_info,
        exc_info=exc_info,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error, please contact the server administrator."
        },
        headers={"X-Error-ID": str(error_id)},
    )
