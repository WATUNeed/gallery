import typing
import uuid

from sqlalchemy import UUID, func, ForeignKey, Integer, event, Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from backend.api.base_classes.models import Base
from backend.api.rate.mixin import RateMixin

if typing.TYPE_CHECKING:
    from backend.api.user.models import User


def _user():
    from backend.api.user.models import User
    return User


class Rate(Base, RateMixin):
    __tablename__ = 'RateTable'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(_user().id), nullable=False
    )
    author: Mapped[_user()] = relationship(cascade="save-update", lazy='subquery')

    rate: Mapped[int] = mapped_column(Integer, nullable=False)

    photos: Mapped[list["Photo"]] = relationship(
        back_populates="rating",
        secondary='Photo_Rate',
        lazy='select'
    )
