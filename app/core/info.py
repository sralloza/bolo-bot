from json import JSONDecodeError

import requests
from fastapi import HTTPException
from pydantic.error_wrappers import ValidationError

from app.schemas.info import SuccessWebHookInfo

from .config import settings


def get_webhook_info():
    url = "https://api.telegram.org/bot%s/getWebHookInfo" % settings.token_bot
    try:
        r = requests.get(url)
    except requests.ConnectionError as exc:
        raise HTTPException(500, detail=str(exc))

    exc = HTTPException(500, "Invalid telegram response: %r" % r.content)

    try:
        data = r.json()
    except JSONDecodeError:
        raise exc

    if data.get("ok", False) is not True:
        raise exc

    try:
        return SuccessWebHookInfo.parse_obj(data["result"])
    except ValidationError as exc:
        raise HTTPException(500, str(exc))
    except:
        raise exc
