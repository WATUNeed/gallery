from uuid import UUID

from pydantic import Field

from backend.api.base_classes.scheme import BaseScheme


class PhotoScheme:
    class PostBody(BaseScheme):
        name: str
        description: str | None = None
        file: bytes
        collection_id: UUID

    class View(BaseScheme):
        id: UUID
        name: str
        description: str | None = None
        author_id: UUID
        collection_id: UUID
        rate: float = Field()

    class WithRelated(BaseScheme):
        id: UUID
        name: str
        description: str | None = None
        rate: float
