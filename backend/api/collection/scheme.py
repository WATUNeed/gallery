from uuid import UUID

from backend.api.base_classes.scheme import BaseScheme
from backend.api.photo.scheme import GetPhotoWithRelated
from backend.api.user.scheme import ShareUserScheme


class CreateCollection(BaseScheme):
    name: str
    description: str | None = None


class UpdateCollection(BaseScheme):
    id: UUID
    name: str | None = None
    description: str | None = None


class GetCollection(BaseScheme):
    id: UUID
    author_id: UUID
    name: str
    description: str | None = None


class GetCollectionWithRelated(BaseScheme):
    id: UUID
    author: ShareUserScheme
    name: str
    description: str | None = None
    photos: list[GetPhotoWithRelated] = []
