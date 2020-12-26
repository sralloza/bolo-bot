from platform import system

from app.core.bot import updater


def main():
    updater.start_polling()
    if system() == "Windows":
        updater.idle()
