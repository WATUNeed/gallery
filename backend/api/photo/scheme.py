from uuid import UUID

from backend.api.base_classes.scheme import BaseScheme


class CreatePhoto(BaseScheme):
    name: str
    description: str | None = None
    file: str
    collection_id: UUID


class GetPhoto(BaseScheme):
    id: UUID
    name: str
    description: str | None = None
    file: str


class GetPhotoWithRelated(BaseScheme):
    id: UUID
    name: str
    description: str | None = None
    file: str
    collection_id: UUID
    author_id: UUID
