import logging
import traceback
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.db.session import get_db

from .config import settings

logger = getLogger(__name__)


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
    def wrap_function(*args, **kwargs):
        with get_db() as db:
            return function(db, *args, **kwargs)

    return wrap_function


def exception_handling(update, context):
    exc = context.error
    tb = traceback.format_exc()
    msg = f"{exc!r}\n{tb}"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Error en el servidor. Reenvía este mensaje "
        f"al administrador del bot ({settings.admin})",
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    logger.exception(exc)
