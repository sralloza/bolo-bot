from fastapi.routing import APIRouter

from . import bot_webhook, info

router = APIRouter()
router.include_router(bot_webhook.router)
router.include_router(info.router)
