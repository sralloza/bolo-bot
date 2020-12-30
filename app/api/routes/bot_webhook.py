import logging
from json import JSONDecodeError, loads

from fastapi import APIRouter, HTTPException, Request

from app.core.webhook import webhook

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/process-msg")
async def index(request: Request):
    data = await request.body()
    try:
        data = loads(data.decode("utf8"))
    except JSONDecodeError as exc:
        logger.exception(exc)
        raise HTTPException(500, str(exc))

    if not isinstance(data, dict):
        raise HTTPException(500, "Invalid payload")

    logger.info("Processing data: %s", data)
    try:
        return webhook(data)
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(500, "Error in webhook, check logs")
    finally:
        logger.info("Data processed")
