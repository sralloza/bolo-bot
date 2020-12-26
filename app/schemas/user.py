from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    id: Optional[int]
    username: str


class UserUpdate(BaseModel):
    id: Optional[int]
    username: Optional[str]
    bolos: Optional[int]
