from app.core.bot import updater


def main():
    updater.start_polling()
    updater.idle()
