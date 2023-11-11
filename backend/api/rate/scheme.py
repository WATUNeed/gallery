from uuid import UUID

from pydantic import Field

from backend.api.base_classes.scheme import BaseScheme


class RateScheme:
    class PostBody(BaseScheme):
        photo_id: UUID
        rate: int = Field(ge=0, le=5)

    class View(BaseScheme):
        id: UUID
        photo_id: UUID
        user_id: UUID
        rate: list[int] = Field(ge=0, le=5)
