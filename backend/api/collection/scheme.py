from uuid import UUID

from backend.api.base_classes.scheme import BaseScheme
from backend.api.photo.scheme import PhotoScheme
from backend.api.user.scheme import UserScheme


class CollectionScheme:
    class PostBody(BaseScheme):
        name: str
        description: str | None = None

    class PutBody(BaseScheme):
        id: UUID
        name: str | None = None
        description: str | None = None

    class View(BaseScheme):
        id: UUID
        author_id: UUID
        name: str
        description: str | None = None

    class WithRelated(BaseScheme):
        id: UUID
        author: UserScheme.ShareView
        name: str
        description: str | None = None
        photos: list[PhotoScheme.WithRelated] = []
