from uuid import UUID

from backend.api.base_classes.scheme import BaseScheme


class PhotoScheme:
    class PostBody(BaseScheme):
        name: str
        description: str | None = None
        file: str
        collection_id: UUID

    class View(BaseScheme):
        id: UUID
        name: str
        description: str | None = None
        file: str

    class WithRelated(BaseScheme):
        id: UUID
        name: str
        description: str | None = None
        file: str
        collection_id: UUID
        author_id: UUID
