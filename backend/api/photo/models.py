import typing
import uuid

from sqlalchemy import func, UUID, String, ForeignKey, Float, TypeDecorator
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.api.base_classes.models import Base
from backend.api.photo.mixin import PhotoMixin

if typing.TYPE_CHECKING:
    from backend.api.user.models import User


def _user():
    from backend.api.user.models import User
    return User


class HexByteString(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("HexByteString columns support only bytes values.")
        return value.hex()

    def process_result_value(self, value, dialect):
        return bytes.fromhex(value) if value else None


class Photo(Base, PhotoMixin):
    __tablename__ = 'PhotoTable'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )

    collection_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('CollectionTable.id'), nullable=False
    )
    collection: Mapped['Collection'] = relationship(
        cascade="save-update", lazy='subquery', back_populates='photos'
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(_user().id), nullable=False
    )
    author: Mapped[_user()] = relationship(cascade="save-update", lazy='subquery')

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)

    file: Mapped[bytes] = mapped_column(HexByteString, nullable=False)

    rate: Mapped[int] = mapped_column(Float, default=0, nullable=False)

    rating: Mapped[list["Rate"]] = relationship(
        back_populates="photos",
        secondary='Photo_Rate',
        lazy='select'
    )


class PhotoRate(Base):
    __tablename__ = "Photo_Rate"

    rate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("RateTable.id"), primary_key=True)
    photo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("PhotoTable.id"), primary_key=True)
