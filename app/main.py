from platform import system
from warnings import warn

from fastapi import FastAPI

from app.api.routes import router
from app.core.bot import updater
from app.core.utils import server_exception_handling


def create_app():
    app = FastAPI()
    app.include_router(router)
    app.add_exception_handler(500, server_exception_handling)

    return app


def main():
    warn(
        "Do not user updater.start_polling()\nUse REST API webhook", DeprecationWarning
    )
    updater.start_polling()
    if system() == "Windows":
        updater.idle()
