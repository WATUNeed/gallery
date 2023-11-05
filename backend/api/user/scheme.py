from typing import Optional
from uuid import UUID

from backend.api.base_classes.scheme import BaseScheme


class ShareUserScheme(BaseScheme):
    id: UUID
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    login: str


class UpdateUser(BaseScheme):
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
