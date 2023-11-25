import typing
import uuid
from datetime import datetime

from sqlalchemy import func, UUID, String, ForeignKey, TypeDecorator, Float, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.api.base_classes.models import Base
from backend.api.collection.mixin import CollectionMixin, CollectionDownloadQueryHistoryMixin

if typing.TYPE_CHECKING:
    from backend.api.user.models import User


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

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)

    photos: Mapped[list['Photo']] = relationship(
        cascade='all,delete', lazy='subquery', back_populates='collection', order_by='desc(Photo.rate)'
    )


class FileSizeMBFloat(TypeDecorator):
    impl = Float

    def process_bind_param(self, value, dialect):
        if not isinstance(value, int):
            raise TypeError("FileSizeMBFloat columns support only int values.")
        return round(value / 1024 / 1024, 3)

    def process_result_value(self, value, dialect):
        return round(value * 1024 * 1024, 0) if value else None


class CollectionDownloadQueryHistory(Base, CollectionDownloadQueryHistoryMixin):
    __tablename__ = 'CollectionDownloadQueryHistoryTable'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )

    collection_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(Collection.id), nullable=False
    )
    collection: Mapped[Collection] = relationship(lazy='selectin')

    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(_user().id), nullable=False
    )
    sender: Mapped[_user()] = relationship(lazy='selectin')

    file_size: Mapped[float] = mapped_column(FileSizeMBFloat, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
