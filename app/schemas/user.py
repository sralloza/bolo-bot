from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    id: Optional[int]
    username: str


class UserUpdate(BaseModel):
    id: Optional[int]
    username: Optional[str]
    bolos: Optional[int]
    latest_bolo: datetime = Field(default_factory=datetime.now)
