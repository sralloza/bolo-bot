from telegram.ext.filters import MessageFilter

from app.core.config import settings


class _AdminFilter(MessageFilter):
    def filter(self, message):
        return bool(message.from_user.id == settings.admin_user_id)


class CustomFilters:
    admin_filter = _AdminFilter()
