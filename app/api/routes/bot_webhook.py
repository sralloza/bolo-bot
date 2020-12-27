from fastapi import APIRouter, Request

from app.core.webhook import webhook

router = APIRouter()


@router.post("/")
async def index(request: Request):
    data = await request.body()
    return webhook(data.decode("utf8"))
