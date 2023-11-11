from typing import Optional
from uuid import UUID

from pydantic import Field

from backend.api.base_classes.scheme import BaseScheme


class ShareUserScheme(BaseScheme):
    id: UUID
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    patronymic: Optional[str] = Field(default=None)
    login: str


class UpdateUser(BaseScheme):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    patronymic: Optional[str] = Field(default=None)
