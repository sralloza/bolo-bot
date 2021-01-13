from app.schemas.info import SuccessWebHookInfo
from app.core.info import get_webhook_info
from fastapi.routing import APIRouter

router = APIRouter(tags=["info"])

@router.get("/webhook-info", response_model=SuccessWebHookInfo)
def webhook_info_endpoint():
    return get_webhook_info()
