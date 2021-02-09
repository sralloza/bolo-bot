from fastapi.routing import APIRouter

from app.core.info import get_webhook_info
from app.schemas.info import SuccessWebHookInfo

router = APIRouter(tags=["info"])


@router.get("/webhook-info", response_model=SuccessWebHookInfo)
def webhook_info_endpoint():
    return get_webhook_info()
