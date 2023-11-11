import typing
import uuid

from sqlalchemy import func, UUID, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.api.base_classes.models import Base
from backend.api.photo.mixin import PhotoMixin

if typing.TYPE_CHECKING:
    from backend.api.user.models import User


def _user():
    from backend.api.user.models import User
    return User


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
    file: Mapped[str] = mapped_column(String, nullable=False)

    rating: Mapped[list["Rate"]] = relationship(
        secondary="Photo_Rate", back_populates="photos", viewonly=True
    )

    rating_associations: Mapped[list["PhotoRate"]] = relationship(
        back_populates="photo"
    )


class PhotoRate(Base):
    __tablename__ = "Photo_Rate"

    rate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("RateTable.id"), primary_key=True)

    photo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("PhotoTable.id"), primary_key=True)

    rate: Mapped["Rate"] = relationship(back_populates="photos_associations")

    photo: Mapped["Photo"] = relationship(back_populates="rating_associations")
