import typing
import uuid

from sqlalchemy import func, UUID, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.api.base_classes.models import Base
from backend.api.collection.mixin import CollectionMixin

if typing.TYPE_CHECKING:
    from backend.api.user.models import User
    from backend.api.photo.models import Photo


def _user():
    from backend.api.user.models import User
    return User


class Collection(Base, CollectionMixin):
    __tablename__ = 'CollectionTable'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(_user().id), nullable=False
    )
    author: Mapped[_user()] = relationship(lazy='subquery')

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)

    photos: Mapped[list['Photo']] = relationship(
        cascade='all,delete', lazy='subquery', back_populates='collection')
