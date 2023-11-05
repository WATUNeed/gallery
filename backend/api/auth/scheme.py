from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from backend.api.base_classes.scheme import BaseScheme


class SignBody(BaseScheme):
    login: str
    password: str


class RefreshToken(BaseModel):
    sub: str | UUID
    exp: datetime


class SignResponse(BaseModel):
    token: str
