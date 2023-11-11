import typing
import uuid

from sqlalchemy import func, UUID, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.api.base_classes.models import Base
from backend.api.photo.mixin import PhotoMixin

if typing.TYPE_CHECKING:
    from backend.api.user.models import User
    from backend.api.collection.models import Collection


def _user():
    from backend.api.user.models import User
    return User


def _collection():
    from backend.api.collection.models import Collection
    return Collection


class Photo(Base, PhotoMixin):
    __tablename__ = 'PhotoTable'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )

    collection_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(_collection().id), nullable=False
    )
    collection: Mapped[_collection()] = relationship(
        cascade="save-update", lazy='subquery', back_populates='photos'
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(_user().id), nullable=False
    )
    author: Mapped[_user()] = relationship(cascade="save-update", lazy='subquery')

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    file: Mapped[str] = mapped_column(String, nullable=False)
