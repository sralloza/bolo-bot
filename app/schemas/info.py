from datetime import datetime
from ipaddress import IPv4Address
from typing import Optional

from pydantic import BaseModel, validator
from pydantic.networks import HttpUrl


class SuccessWebHookInfo(BaseModel):
    url: Optional[HttpUrl]
    has_custom_certificate: bool
    pending_update_count: int
    max_connections: Optional[int]
    last_error_date: Optional[datetime]
    last_error_message: Optional[str]
    ip_address: Optional[IPv4Address]

    @validator("url", pre=True)
    def check_url(cls, v):
        if isinstance(v, str) and len(v) == 0:
            return None
        return v

    @validator("last_error_date", pre=True)
    def check_last_error_date(cls, v):
        if isinstance(v, int):
            return datetime.fromtimestamp(v)
        return v
